from qalibs.eapi_request import EapiRequests
from qalibs.eapi_request import EapiRequests, utils
from qalibs.eapi_request.airsync_api.devices import AirSyncDevice
from qalibs.eapi_request.airsync_api.templates import AirSyncTemplate, AirSyncBlob

tenant = 1  # ["prox_admin", "prox2_admin", "prox3_admin"]
#eapi = EapiRequests.file('geic-sandbox', tenant=tenant, user='prox2_admin', password='P@ssw0rd')
eapi = EapiRequests.file('geic-qa4', tenant=tenant)


asdids = ["geic_gwa_8_BE536B009317"]

devices = [AirSyncDevice(eapi=eapi, asdid=asdid) for asdid in asdids]

print('')

for device in devices:
    o = AirSyncDevice.delete(device)
    print('operation id: ', o.go_id)
    print('task_id: ', o.get_tasks()[0])
    print('task_id: ', o.get_tasks()[0].task_id)


