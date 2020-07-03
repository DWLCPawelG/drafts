"""Example of using new architecture for Agent orchestration."""

from time import sleep
from qalibs.agent.geic import GeICAgentController, GeICGWAAgentController
from qalibs.agent.common import AgentParameters
from qalibs.agent.runtimes import create_dockerized_manager
from qalibs.eapi_request.utils import find_did_by_asdid
from qalibs.eapi_request import EapiRequests

# like in test_environment.ini
setup = "geic-qa3"
tenant = 1
device_type = "GeICGWADocker"
prefix = "pablo"
agent_type = "geicgwaagent"  # or "geicagent"
image_tag = '1'  # or 1.0.34; 1 for GEIC_GWA
pkg_result_file_timeout = 60
component_interval = 30
sync_msg_interval = 30

asdid = "create"  # or asdid of existing node

host = "localhost"  # if IP Address than as string
port = 2375
expected_registration_time = 40
expected_container_startup_time = 60


def main():
    eapi = EapiRequests.file(name=setup, tenant=tenant, rest_version=2.0)

    manager = create_dockerized_manager(setup_name=setup, tenant=tenant, docker_host=host, docker_port=port)

    params = AgentParameters(
        component_interval=component_interval,
        pkg_result_file_timeout=pkg_result_file_timeout,
        sync_msg_interval=sync_msg_interval)

    if not asdid or asdid == 'create':
        suffix = prefix
        did = None
    else:
        suffix = None
        did = find_did_by_asdid(eapi_client=eapi, asdid=asdid)

    runtime = manager.create_execution_runtime(agent_type=agent_type, agent_version=image_tag, agent_parameters=params,
                                          suffix=suffix, did=did)
    if agent_type == 'geicagent':
        controller = GeICAgentController(runtime=runtime)
    else:
        controller = GeICGWAAgentController(runtime=runtime)
    sleep(40)
    controller.add_all_agent_components(instance=1)
    sleep(30)
    for _ in range(10):
        controller.send_all_alerts(state='set')
        sleep((40))
        controller.send_all_alerts(state='clear')
        sleep(40)

    runtime.close()


if __name__ == '__main__':
    main()
