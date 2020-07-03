from qalibs.eapi_request import EapiRequests
import qalibs
from qalibs.eapi_request import EapiRequests, utils
from qalibs.eapi_request.airsync_api.devices import AirSyncDevice
from qalibs.eapi_request.airsync_api.templates import AirSyncTemplate, AirSyncBlob
from qalibs.eapi_request.airsync_api.commands import AirSyncCommand


body_create = [
    {
        "parameters": [],
        "name": "Open SSH",
        "description": "Open SSH channel",
        "api_name": "ssh_tunnel_open",
    },
    {
        "parameters": [],
        "name": "Close SSH",
        "description": "Close SSH channel",
        "api_name": "ssh_tunnel_close",
    },
]

body_add = {
    "api_name": "reboot_after",
    "name": "Reboot device",
    "description": "Reboot device after given timeout.",
    "parameters": [
        {
            "api_name": "timeout",
            "name": "Time in seconds after which the device is rebooted.",
            "type": "integer",
            "required": False,
        }
    ],
}
tenant = 1  # ["prox_admin", "prox2_admin", "prox3_admin"]
#eapi = EapiRequests.file('geic-sandbox', tenant=tenant, user='prox2_admin', password='P@ssw0rd')
eapi = EapiRequests.file('geic-qa3', tenant=tenant)

create_command_definitions = AirSyncCommand.send_command(device=) # not finished