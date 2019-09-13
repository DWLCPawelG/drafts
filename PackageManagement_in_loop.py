import json
from contextlib import ExitStack

from interruptingboar import timeout
from qalibs.agent.common import AgentParameters
from qalibs.agent.geic import GeICGWAAgentController
from qalibs.agent.runtimes import create_dockerized_manager
from qalibs.eapi_request import EapiRequests
from qalibs.eapi_request.airsync_api.devices import AirSyncDevice
from qalibs.eapi_request.airsync_api.group_operations import CalculatedStatus, AirSyncGroupOperation
from qalibs.eapi_request.airsync_api.templates import AirSyncTemplate, AirSyncBlob

from time import sleep

tenant = 1  # ["prox_admin", "prox2_admin", "prox3_admin"]
# eapi = EapiRequests.file('geic-sandbox', tenant=tenant, user='prox2_admin', password='P@ssw0rd')
eapi = EapiRequests.file('geic-qa', tenant=tenant)

print('Searching or template:')
package_description = 'GGC_test'
# t = AirSyncTemplate.create_new_template(client=eapi, template_type='CityIQ Configuration Update', template_description=package_description, blob=AirSyncBlob.upload_new_blob_with_random_file(client=eapi, file_size=1000))

# asdids = ["geic_gwa_300_28539D015E45", "geic_gwa_301_62D311FC2153"]
print('creating AirSyncDevice objects')
# devices = [AirSyncDevice(eapi=eapi, asdid=asdid) for asdid in asdids]

# print('Applying template to devices:')

# o = t.apply(devices=devices)
# print('operation id: ', o.go_id)
# print('task_id: ', o.get_tasks()[0])
# print('task_id: ', o.get_tasks()[0].task_id)

manago = create_dockerized_manager(setup_name='geic-qa', tenant=1,
                                   docker_host='10.10.10.201'
                                   )
my_dids =  [
    # "geic_gwa_900"
    # ,

    "geic_gwa_901"
    ,

    "geic_gwa_902"
    # ,
    #
    # "geic_gwa_903"
    # ,
    #
    # "geic_gwa_904"
    # ,
    #
    # "geic_gwa_905"
    # ,
    #
    # "geic_gwa_906"
    # ,
    #
    # "geic_gwa_907"
    # ,
    #
    # "geic_gwa_908"
    # ,
    #
    # "geic_gwa_909"
    # ,
    #
    # "geic_gwa_910"
    # ,
    #
    # "geic_gwa_911"
    # ,
    #
    # "geic_gwa_912"
    # ,
    #
    # "geic_gwa_913"
    # ,
    #
    # "geic_gwa_914"
    # ,
    #
    # "geic_gwa_915"
    # ,
    #
    # "geic_gwa_916"
    # ,
    #
    # "geic_gwa_917"
    # ,
    #
    # "geic_gwa_918"
    # ,
    #
    # "geic_gwa_919"
]
component_interval = 120
pkg_result_file_timeout = 0
sync_msg_interval = 30
parameters = AgentParameters(component_interval=component_interval, pkg_result_file_timeout=pkg_result_file_timeout,
                             sync_msg_interval=sync_msg_interval)
runtimes_ctx = [manago.get_execution_runtime(
    agent_type='geicgwaagent',
    agent_version=1,
    agent_parameters=parameters,
    did=did,
    close_runtime=False) for did in my_dids]


def _wait_until_all_tasks_are_staged(group_operation: AirSyncGroupOperation,
                                     tasks_timeout: int,
                                     sync_message_interval: int):
    """
    method wait until all tasks in single operation are in STAGED state or timeout is reached

    :param group_operation: instance of single AirSyncGroupOperation
    :param tasks_timeout: time range how long tasks will be checked in seconds
    :param sync_message_interval: Agent reporting interval
    """
    print(f"Wait (timeout: {tasks_timeout}s) until all packages are downloaded "
          f"(all tasks in operation {group_operation.go_id} are in STAGING state)")
    tasks = group_operation.get_tasks()
    assert tasks, f'Received no tasks in group operation {group_operation}'
    with timeout(tasks_timeout, TimeoutError):
        try:
            while tasks:
                tasks = [task for task in tasks if
                         task.get_calculated_status() != str(CalculatedStatus.STAGED)]
                if not tasks:
                    break
                # check for possible errors, eq FUS communication timed out
                for task in tasks:
                    current_calculated_status = CalculatedStatus[task.get_calculated_status()]
                    final_status_list = CalculatedStatus.final_calculated_statuses()
                    if any(current_calculated_status == s for s in final_status_list):
                        print(f"Task {task.task_id} is in {current_calculated_status} state. "
                              f"Task detailed status:"
                              f" \n{json.dumps(task.get_detailed_status(), indent=4)}")
                        print(f"Task {task.task_id} is in {current_calculated_status} state")
                sleep(round(sync_message_interval / 2))

        except TimeoutError:
            print(f"Operation is not finished after expected {timeout}s time")
        print(f"Packages downloaded (all tasks in operation {group_operation.go_id} are in STAGING state)")


with ExitStack() as stack:
    count = 10
    runtimes = [stack.enter_context(runtime_ctx) for runtime_ctx in runtimes_ctx]
    controllers = [GeICGWAAgentController(runtime, agent_params=parameters) for runtime in runtimes]
    asdids = [

        # "geic_gwa_900_984016C68552"
        # ,

        "geic_gwa_901_3CDA2D4A55A1"
        ,

        "geic_gwa_902_6D6C7992C3E1"
        # ,
        #
        # "geic_gwa_903_843195755E61"
        # ,
        #
        # "geic_gwa_904_ECA3851488EA"
        # ,
        #
        # "geic_gwa_905_B00A36CC6499"
        # ,
        #
        # "geic_gwa_906_1D9E4CBB5650"
        # ,
        #
        # "geic_gwa_907_BCE8C2878412"
        # ,
        #
        # "geic_gwa_908_DCADCB4D56C3"
        # ,
        #
        # "geic_gwa_909_C95803F1353F"
        # ,
        #
        # "geic_gwa_910_8812EAE6005A"
        # ,
        #
        # "geic_gwa_911_823D0E55CC2C"
        # ,
        #
        # "geic_gwa_912_ACE2A7CFF8B4"
        # ,
        #
        # "geic_gwa_913_035639947F47"
        # ,
        #
        # "geic_gwa_914_BDF145EF52DD"
        # ,
        #
        # "geic_gwa_915_12855D165CF4"
        # ,
        #
        # "geic_gwa_916_C9D98846568A"
        # ,
        #
        # "geic_gwa_917_8DAB8B79D859"
        # ,
        #
        # "geic_gwa_918_749B32964DEA"
        # ,
        #
        # "geic_gwa_919_B956224E9857"
    ]
    devices = [AirSyncDevice(eapi=eapi, asdid=asdid) for asdid in asdids]

    for i in range(1, count + 1):
        print(f"Iteration {i}")
        template = AirSyncTemplate.create_new_template(
            client=eapi, template_type='CityIQ Configuration Update',
            template_description=package_description,
            blob=AirSyncBlob.upload_new_blob_with_random_file(client=eapi, file_size=1024 * 1024 * 10)
            # file_size=1024 == 1kB
        )
        print('Applying template to devices:')
        operation = template._apply(devices=devices)

        _wait_until_all_tasks_are_staged(
            group_operation=operation,
            tasks_timeout=90,
            sync_message_interval=sync_msg_interval
        )

        for j, controller in enumerate(controllers, 1):
            controller.upload_result_file(operation_id=operation.go_id)
            print(f"Upload finished for controller {j}")
