from qalibs.eapi_request import EapiRequests
from qalibs.eapi_request import EapiRequests, utils
from qalibs.eapi_request.airsync_api.devices import AirSyncDevice
from qalibs.eapi_request.airsync_api.templates import AirSyncTemplate, AirSyncBlob

tenant = 1  # ["prox_admin", "prox2_admin", "prox3_admin"]
#eapi = EapiRequests.file('geic-sandbox', tenant=tenant, user='prox2_admin', password='P@ssw0rd')
eapi = EapiRequests.file('geic-support', tenant=tenant)


asdids = ["geic_gwa_pablo0_5GH6S1E-ai_pedestriantraffic-1-0_ACA963FEAE30"]

devices = [AirSyncDevice(eapi=eapi, asdid=asdid) for asdid in asdids]

print('')

for device in devices:
    o = AirSyncDevice.delete(device)
    print('operation id: ', o.go_id)
    print('task_id: ', o.get_tasks()[0])
    print('task_id: ', o.get_tasks()[0].task_id)


