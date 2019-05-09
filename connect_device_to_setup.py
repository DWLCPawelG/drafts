import logging
from configparser import ConfigParser
from time import sleep

import pytest
from interruptingcow import timeout
from qalibs.eapi_request import EapiRequests
from qalibs.eapi_request.airsync_api.devices import GeICNode
from qalibs.eapi_request.utils import find_asdid_by_did
from qalibs.ssh_request import GeICDocker

from .helpers.containers_manager import GeICAgentContainers

pytest_plugins = ['qalibs.pytest_plugins.common_logger.testcase_logging',
                  'qalibs.pytest_plugins.common_logger.class_logging']
logger = logging.getLogger(__name__)


# @pytest.fixture(scope='session')
def config_parser():
    config = ConfigParser()
    config.read('test_environment.ini')
    return config


# @pytest.fixture(scope='session')
def config(config_parser):
    sections_dict = {}
    # get sections and iterate over each
    sections = config_parser.sections()

    for section in sections:
        options = config_parser.options(section)
        temp_dict = {}
        for option in options:
            temp_dict[option] = config_parser.get(section, option)

        sections_dict[section] = temp_dict

    return sections_dict


# @pytest.fixture(scope='session')
def eapi(config):
    eapi = EapiRequests.file(name=config['Setup']['setup'], tenant=int(config['Setup'].get('tenant', 1)),
                             rest_version=config['Setup'].get('eapi_rest_version'))
    return eapi


# @pytest.fixture(scope='module')
def docker_node(config, eapi):
    device_asdid = config['ServerDevice']['asdid']
    docker_config = config['Docker']
    device_config = config['AgentDevice']
    docker_node = GeICDocker.create_with_random_did(
        docker_host=docker_config['host'],
        docker_port=docker_config['port'],
        image=device_config['image'], image_tag=device_config['image_tag'],
        agent_prefix=device_config['prefix'], setup=config['Setup']['setup'],
        tenant=int(config['Setup']['tenant']))
    if not device_asdid or device_asdid == 'create':
        logger.info('No ASDID specified, starting a new Agent container with components.')
        sleep(int(docker_config['expected_container_startup_time']))
        docker_node.container.reload()
        assert ('running' == docker_node.container.status), \
            f"Node container status should be running: {docker_node.container.status}"
        logger.info(
            f"Created container {docker_node}. Waiting for"
            f" {docker_config['expected_registration_time']}s.")
        sleep(int(docker_config['expected_registration_time']))
        docker_node.asdid = find_asdid_by_did(eapi, docker_node.did)
        logger.info(f'New node registered with asdid {docker_node.asdid}')
        docker_node.add_all_components(suffix=1)
    else:
        docker_node.asdid = device_asdid
        logger.info(f'Using node with given asdid {docker_node.asdid}')
    return docker_node


# @pytest.fixture(scope='module')
def eapi_node(request, config, eapi, docker_node):
    eapi_node = GeICNode(eapi, docker_node.asdid)
    sleep(int(config['Docker']['expected_registration_time']))

    def clean_containers():
        docker_node.end()
        eapi_node.delete(with_components=True)
        response = eapi.send(method="GET", path='devices/{}'.format(docker_node.asdid))
        logger.info(f"Checking for existence of {docker_node.asdid}...")
        logger.info(f'GET /devices/{docker_node.asdid} response was {response.status_code}')
        if response.status_code == 404:
            logger.info(f'{docker_node.asdid} was deleted correctly')
        else:
            try:
                with timeout(120, exception=RuntimeError):
                    while response.status_code != 404:
                        logger.info(f"Retrying checking for Node {docker_node.asdid} until status code is equal to 404")
                        response = eapi.send(method="GET",
                                             path='devices/{}'.format(docker_node.asdid))
                        sleep(5)
            except RuntimeError:
                pytest.fail(f"Device with asdid {docker_node.asdid} can't be deleted")
            else:
                logger.info(f"Device {docker_node.asdid} was deleted correctly")

    request.addfinalizer(clean_containers)
    assert eapi_node.is_valid(), f"Precondition failed, eapi_node is not valid"
    return eapi_node


container = docker_node(config=config_parser(), eapi=eapi(config_parser()))


# OR
def device_for_group_operations_unregistrations(eapi, config):
    with GeICAgentContainers.create_containers(count=1, eapi=eapi, config=config) as node:
        with GeICAgentContainers.create_eapi_nodes(eapi=eapi, nodes=node) as eapi_node:
            print(eapi_node)
            return eapi_node
