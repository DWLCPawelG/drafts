import logging
import random
import pprint
from contextlib import ExitStack
from distutils.command.config import config
import string
import pytest
from interruptingcow import timeout
from time import sleep, time
from operator import itemgetter

from geic.helpers.containers_manager import GeICAgentContainers
from geic.helpers.geic_helper import get_config_from_agent
from qalibs.eapi_request.utils import find_asdid_by_did
from qalibs.test_utils.testrail import tr_case_id
from common.statistics_common import check_raw_for_specific_statistic

"""Exemplary file test_environment.ini

[Setup]
setup = geic-qa3         ; setup name as defined in qalibs/eapi_request/oauth.cfg
tenant = 1               ; tenant id based on oauth.cfg (default set to 1).

[AgentDevice]
device_type = GeICGWADocker
prefix = PM_smoke        ; node did and container name will be: geic_gwa_<prefix>_<id>
agent_type = geicgwaagent
image = relayr/geicagent ; docker image name with GeIC Agent
image_tag = 1            ; GeIC Agent version (docker image with such tag must exist)
pkg_result_file_timeout = 90
component_interval = 30
sync_msg_interval = 30
log_path =               ; absolute path to agent logs on host (eg. /root/pdm-qa-isap-gwa/logs on GEIC VM) ; remove this 
                           key so that it does not log

[ServerDevice]
asdid = create           ; either proper ASDID of node connected to setup or word 'create'
                         ; with 'create' a container with configuration from AgentDevice section will be used

[Docker]
host = localhost         ; host on which the containers with GeIC will be run
port = 2376              ; 
expected_registration_time = 40
expected_container_startup_time = 60

[TestRail]
report_test_run = false  ; whether a new test run should be created in TestRail
close_test_run = false   ; whether test run should be closed after finishing tests
milestone = 30
project = 4
suite = 240
test_run_id = 0
"""

logger = logging.getLogger(__name__)


class TestGeICGWASmokeAgent:
    """Agent Smoke Tests on GEIC GWA Agent"""

    device_model_names = ['clock', 'wifi', 'cell-modem', 'ethernet', 'wifi-ap', 'camera-1', 'camera-2',
                          'microphone-1', 'microphone-2', 'gps', 'aux-board', 'env-board', 'pwrm-board',
                          'sbc-board', 'heaters', 'vpn', 'private-vpn', 'mqtt', 'sstlink', 'data', 'log',
                          'rootfs', 'sense-ioboardctrl', 'sense-envboardcontroller', 'sense-metering',
                          'sense-msg_proxy', 'ai_vehicledetection-1', 'vidpro', 'ai_pedestriantraffic-1',
                          'sense-noise_service', 'watchdog', 'vidpro_rtsp_server', 'ai_sst_sensapp',
                          'sense-audio_service', 'os', 'ai_vehicledetection-2', 'ai_vehicledetection-3',
                          'sense-app-data-on-demand', 'ai_vehicletraffic-1', 'sense-healthmonitor',
                          'sense-proximhealthiface', 'sense-config_mgr', 'proximetry-relayr-agent']

    @pytest.fixture(scope='module')
    def controller_agent_with_components(self, agent_controller):
        agent_controller.add_all_agent_components(instance=0)
        yield agent_controller
        logger.info('All 1st instance components was added to Node')

    @staticmethod
    def get_systems_endpoint_filtered_by_asdid(eapi, asdid):
        params = {'filter': f'asdid+eq+"{asdid}"'}
        response = eapi.send(method="GET", path='systems', params=params)
        logger.debug(f'GET on URL: {response.url}')
        assert response.status_code == 200, f'Unexpected HTTP code: {response.status_code}. Expected: 200'
        response.raise_for_status()
        return response.json()[0]

    @staticmethod
    def get_on_defined_endpoint(eapi, endpoint_path):
        response = eapi.send(method="GET", path=endpoint_path)
        logger.debug(f'GET on URL: {response.url}')
        response.raise_for_status()
        return response.json()[0]

    @staticmethod
    def find_component_asdid_by_name(eapi_device, component_name):
        components_list = list(eapi_device.get_sub_devices())
        for component_id, component in enumerate(components_list, start=0):
            component = components_list[component_id]
            while component['systemROAttributes'].get('geic_device_model_name') == component_name:
                component_asdid = component.get('asdid')
        return component_asdid

    def _check_all_components_availability(self, timeout_time, eapi_device):
        actual_amount_of_components = len(list(eapi_device.get_components()))
        with timeout(timeout_time, TimeoutError):
            try:
                while not actual_amount_of_components == len(self.device_model_names):
                    sleep(10)
                    actual_amount_of_components = len(list(eapi_device.get_components()))
                logger.info("Expected amount of device model names (43) is equal to length of actual components "
                            "list")
            except TimeoutError:
                pytest.fail(f"Actual amount ({len(list(eapi_device.get_components()))}) of device model names "
                            f"didn't reach expected value (43)")

    def _check_all_components_overall_status(self, eapi_device, timeout_time, eapi, expected_overall_status: int):
        components_asdids = []
        components_list = list(eapi_device.get_sub_devices())
        for component in components_list:
            component_asdid = component.get('asdid')
            components_asdids.append(component_asdid)

        with timeout(timeout_time, TimeoutError):
            try:
                for asdid in components_asdids:
                    response = self.get_systems_endpoint_filtered_by_asdid(eapi=eapi, asdid=asdid)
                    while not response['customization'].get('operational_status') == expected_overall_status:
                        sleep(5)
                        response = self.get_systems_endpoint_filtered_by_asdid(eapi=eapi, asdid=asdid)
                    logger.debug('Component %s has reached "Operational - no alert" state', asdid)
            except TimeoutError:
                pytest.fail(
                    f"Device with asdid: {asdid} didn't become reachable in {timeout_time} seconds")

    @tr_case_id(49862)
    def test_connect_node_to_cloud(self, eapi, eapi_device, agent_runtime):
        assert eapi_device.is_valid(), 'Connected Node has incorrect "asdid", "did", ' \
                                       '"device_model_id" or "device_model_version"'
        logger.info('Successfully validated GeIC node %s', str(eapi_device))

        # checking reachability of Node
        logger.info('Checking for Reachability of Node with did %s', agent_runtime.did)
        asdid = find_asdid_by_did(eapi_client=eapi, did=agent_runtime.did)
        response = self.get_systems_endpoint_filtered_by_asdid(eapi=eapi, asdid=asdid)
        timeout_time = 300
        with timeout(timeout_time, TimeoutError):
            try:
                while not response['status'].get('device_status') == "REACHABLE":
                    sleep(10)
                    response = self.get_systems_endpoint_filtered_by_asdid(eapi=eapi, asdid=asdid)
                logger.info('Node with did: %s has become Reachable"', agent_runtime.did)
            except TimeoutError:
                pytest.fail(f"Device with did {agent_runtime.did} didn't become reachable in {timeout_time} seconds")

    @pytest.mark.production
    @tr_case_id(52459)
    def test_node_overall_operational_status(self, eapi, agent_runtime):
        logger.info('Checking for "Operational - no alerts" state on Node with did %s', agent_runtime.did)
        asdid = find_asdid_by_did(eapi_client=eapi, did=agent_runtime.did)
        response = self.get_systems_endpoint_filtered_by_asdid(eapi=eapi, asdid=asdid)
        timeout_time = 300
        with timeout(timeout_time, TimeoutError):
            try:
                while not response.get('operational_status') == 5:
                    sleep(10)
                    response = self.get_systems_endpoint_filtered_by_asdid(eapi=eapi, asdid=asdid)
                logger.info('Node with did: %s has "Operational status - no alert"', agent_runtime.did)
            except TimeoutError:
                pytest.fail(f"Device with did {agent_runtime.did} didn't change status to "
                            f"'Operational - no alerts' in {timeout_time} seconds")

    @tr_case_id(49854)
    def test_connect_components_to_node(self, agent_runtime, eapi_device, controller_agent_with_components):

        timeout_time = 300
        self._check_all_components_availability(timeout_time=timeout_time, eapi_device=eapi_device)

        # check reachability of all components
        components_list = list(eapi_device.get_sub_devices())
        with timeout(timeout_time, TimeoutError):
            try:
                for component_id, component in enumerate(components_list, start=0):
                    component = components_list[component_id]
                    component_model_name = component['systemROAttributes'].get('geic_device_model_name')
                    while not component['status']['device_status'] == 'REACHABLE':
                        sleep(5)
                        components_list = list(eapi_device.get_sub_devices())
                        component = components_list[component_id]
                    logger.info('Component %s has become reachable', component_model_name)
            except TimeoutError:
                pytest.fail(f"Components didn't become Reachable in {timeout_time} seconds")

    @pytest.mark.production
    @tr_case_id(52460)
    def test_components_overall_operational_status(self, eapi, agent_runtime, eapi_device,
                                                   controller_agent_with_components):
        timeout_time = 300
        self._check_all_components_availability(timeout_time=timeout_time, eapi_device=eapi_device)

        self._check_all_components_overall_status(eapi_device=eapi_device, timeout_time=timeout_time, eapi=eapi,
                                                  expected_overall_status=5)

    # # NOT FINISHED, it will be useful to have option (in qalib) to connect node without sending statisitcs and alert_state_response
    # @tr_case_id(33638)
    # def test_alert_on_component(self, eapi, eapi_device, controller_agent_with_components, agent_parameters):
    #     # check preconditions
    #     timeout_time = 60
    #     self._check_all_components_availability(timeout_time=timeout_time, eapi_device=eapi_device)
    #     self._check_all_components_overall_status(eapi_device=eapi_device, timeout_time=timeout_time, eapi=eapi,
    #                                               expected_overall_status=5)
    #
    #     # set INFORMATIONAL alert on GPS
    #     # TO DO: random component from list ?
    #     component_name = 'gps'
    #     component_asdid = self.find_component_asdid_by_name(eapi_device=eapi_device, component_name=component_name)
    #
    #     controller_agent_with_components.send_alert(component_name=component_name, instance=0,
    #                                                 alert_type='informational_alert', state='set')
    #     sleep(agent_parameters.sync_msg_interval)
    #q
    #     # validation on /devices/{components_asdid} endpoint
    #     response = self.get_on_defined_endpoint(eapi=eapi, endpoint_path=f'/devices/{component_asdid}')

    @tr_case_id(33649)
    def test_check_agent_version(self, eapi, eapi_device, agent_controller):
        """Checks if agent_version reported by Agent corresponds with the one in Cloud """
        agent_side_result = agent_controller.check_agent_version().decode('ascii').replace('\n', '')
        logger.info('Agent reported agent_version %s during registration', agent_side_result)
        server_side_result = self.get_on_defined_endpoint(eapi=eapi,
                                                          endpoint_path=f'/devices/{eapi_device.asdid}/parameters')
        logger.info('agent_version parameter for %s is %s in Cloud', eapi_device.asdid, server_side_result['value'])
        assert server_side_result['value'] == agent_side_result, 'Incorrect agent_version parameter'

    @tr_case_id(49855)
    def test_check_raw_statistics_on_two_components(self,
                                                       eapi,
                                                       config,
                                                       agent_parameters,
                                                       ssh_client_geic):
        """Connect node with two components - camera-1 and gps, send 3 points for every statistic available for component and check if they reached the Cloud"""
        with ExitStack() as stack:
            agent_runtimes = stack.enter_context(GeICAgentContainers.create_agents_runtimes(count=1,
                                                                                            config=config,
                                                                                            eapi=eapi,
                                                                                            additional_env_variables={'SEND_STATISTICS': 'disabled'}))
            agent_controllers = stack.enter_context(GeICAgentContainers.
                                                    create_agent_controllers(config=config,
                                                                             agent_runtimes=agent_runtimes))
            eapi_nodes = stack.enter_context(GeICAgentContainers.
                                             create_eapi_nodes_for_agent_runtimes(eapi=eapi,
                                                                                  agent_runtimes=agent_runtimes,
                                                                                  agent_controllers=agent_controllers))
            test_components = ['camera-1', 'gps']
            # load device_mapping.json from running agent:
            mapping = get_config_from_agent(ssh_request=ssh_client_geic, geic_node=eapi_nodes[0], file_path='/root/geic-gwa/device_mapping.json')
            gps_stats = [component['statuses'] for component in mapping['device_mapping'] if component['device_model_name'] == 'gps']
            camera_stats = [component['statuses'] for component in mapping['device_mapping'] if component['device_model_name'] == 'camera-1']
            # register compoonents by sending statistics - they will be discarded
            for component in test_components:
                agent_controllers[0].send_statistic(component_name=component, instance=0, stats_to_value={'overall_operational_status': 5})
            sleep(agent_parameters.sync_msg_interval)
            for x in range(3):
                for component in test_components:
                    if component == 'camera-1':
                        for stat in camera_stats[0]:
                            agent_controllers[0].send_statistic(component_name=component, instance=0,
                                                stats_to_value={stat['id']: random.randint(1, 100)})
                    else:
                        for stat in gps_stats[0]:
                            agent_controllers[0].send_statistic(component_name=component, instance=0, stats_to_value={stat['id']: random.randint(1, 100)})
                sleep(agent_parameters.sync_msg_interval)
            components = eapi_nodes[0].get_components()
            for component in components:
                statistics = component.get_raw_statistics(time_range_seconds=5 * agent_parameters.sync_msg_interval).json()
                for i in statistics:
                    if i['stat_name'] != 'operational_status':
                        pprint.pprint(i)
                        assert len(i['points']) >= 3, 'Incorrect number of statistic points'



        # """Connect Node with all components, choose 2 random statistics from 2 random components
        # and check if they are sent to Cloud"""
        # timeout_time = 4 * agent_parameters.sync_msg_interval
        # self._check_all_components_availability(timeout_time=timeout_time, eapi_device=eapi_device)
        # self._check_all_components_overall_status(eapi_device=eapi_device, timeout_time=timeout_time, eapi=eapi,
        #                                           expected_overall_status=5)
        # random_components = [component['asdid'] for component in random.sample(eapi_device.get_sub_devices(), k=2)]
        # logger.info('Checking stats for devices: %s', random_components)
        # for component in random_components:
        #     definition = eapi.send(method='GET', path=f'devices/{component}/definition').json()
        #     random_stats = [stat['id'] for stat in
        #                     random.sample(definition['definition']['statistic_groups'][0]['statistics'], k=2)]
        #     for stat_id in random_stats:
        #         current_ts = int(time() * 1000)
        #         hour_before = int(current_ts - 3600 * 1000)
        #         path = f'devices/{component}/statistics/raw?from={hour_before}&to={current_ts}&stat_ids={stat_id}'
        #         result = self.get_on_defined_endpoint(eapi=eapi, endpoint_path=path)
        #         points = result['points']
        #         logger.info('Statistics points for stat_id %s: %s', stat_id, points)
        #         assert len(points) >= 2, \
        #             f"After three sync_message_interval agent should have sent at least 2 sets of statistics to cloud," \
        #             f" but there are only {len(points)} points for stat_id: {stat_id} available."

    @tr_case_id(41480) # this will fail until GEIC-1664 is fixed
    def test_check_uptime_statistic_on_os_component(self, eapi, eapi_device, agent_runtime,
                                                    controller_agent_with_components, agent_parameters):
        timeout_time = 4 * agent_parameters.sync_msg_interval
        self._check_all_components_availability(timeout_time=timeout_time, eapi_device=eapi_device)
        self._check_all_components_overall_status(eapi_device=eapi_device, timeout_time=timeout_time, eapi=eapi,
                                                  expected_overall_status=5)
        os_asdid = [device['asdid'] for device in eapi_device.get_subdevices_info() if
                    device['device_name'].startswith('os')]
        stats = eapi.send(method='GET', path=f'devices/{os_asdid[0]}/definition').json()['definition']['statistic_groups'][0]['statistics']
        uptime_api_name = [api_name['api_name'] for api_name in stats if api_name['api_name'] == 'uptime']
        current_ts = int(time() * 1000)
        hour_before = int(current_ts - 3600 * 1000)
        path = f'devices/{os_asdid[0]}/statistics/raw?from={hour_before}&to={current_ts}&stat_names={uptime_api_name[0]}'
        result = self.get_on_defined_endpoint(eapi=eapi, endpoint_path=path)['points']
        logger.info('Statistics points for Uptime: %s', result)
        assert len(result) > 0
        assert result == sorted(result, key=itemgetter('timestamp'))


    @tr_case_id(33650)
    def test_set_parameters_on_two_components(self, eapi, eapi_device, agent_controller, agent_parameters):
        parameter = {'random_parameter': "".join(random.choices(string.ascii_uppercase + string.digits, k=10))}
        agent_controller.set_parameters(component_name='ethernet', instance=0, parameter_config=parameter)
        sleep(agent_parameters.sync_msg_interval)
        ethernet_asdid = [device['asdid'] for device in eapi_device.get_subdevices_info() if
                    device['device_name'].startswith('ethernet')]
        print(ethernet_asdid)
        response1 = self.get_on_defined_endpoint(eapi=eapi, endpoint_path=f'/devices/{ethernet_asdid[0]}/parameters')
        pprint.pprint(response1)
        print(response1['value'])
        # assert response1.value[0
        assert eapi_device