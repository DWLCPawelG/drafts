from qalibs.eapi_request import EapiRequests
from qalibs.eapi_request import EapiRequests, utils
from qalibs.eapi_request.airsync_api.devices import AirSyncDevice
from qalibs.eapi_request.airsync_api.templates import AirSyncTemplate, AirSyncBlob

tenant = 1  # ["prox_admin", "prox2_admin", "prox3_admin"]
#eapi = EapiRequests.file('geic-sandbox', tenant=tenant, user='prox2_admin', password='P@ssw0rd')
eapi = EapiRequests.file('geic-qa2', tenant=tenant)


print('Searching or template:')
t = AirSyncTemplate.get_existing_template(client=eapi, description="LOCUST", number=19, version=1, template_type='CityIQ Configuration Update')

asdids = ["geicnode_pablo_0_B6ZBJFE_2154F2D8BAA0"]
print('creating AirSyncDevice objects')
devices = [AirSyncDevice(eapi=eapi, asdid=asdid) for asdid in asdids]

print('Applaying template to devices:')

o = t.apply(devices=devices)
print('operation id: ', o.go_id)
print('task_id: ', o.get_tasks()[0])
print('task_id: ', o.get_tasks()[0].task_id)
