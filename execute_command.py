from qalibs.eapi_request import EapiRequests
from qalibs.eapi_request import EapiRequests, utils
from qalibs.eapi_request.airsync_api.devices import AirSyncDevice
from qalibs.eapi_request.airsync_api.templates import AirSyncTemplate, AirSyncBlob
from qalibs.eapi_request.airsync_api.commands import AirSyncCommand

tenant = 1  # ["prox_admin", "prox2_admin", "prox3_admin"]
#eapi = EapiRequests.file('geic-sandbox', tenant=tenant, user='prox2_admin', password='P@ssw0rd')
eapi = EapiRequests.file('geic-support', tenant=tenant)

asdids = ["aaaagenty3_B9B56E781A37"]
print('creating AirSyncDevice objects')
devices = [AirSyncDevice(eapi=eapi, asdid=asdid) for asdid in asdids]
command = AirSyncCommand.send_command(device=devices[0], command_type='hello', parameters={"data": "something"})
print(command)