from qalibs.eapi_request import EapiRequests
from qalibs.eapi_request import EapiRequests, utils
from qalibs.eapi_request.airsync_api.devices import AirSyncDevice
from qalibs.eapi_request.airsync_api.templates import AirSyncTemplate, AirSyncBlob

tenant = 1  # ["prox_admin", "prox2_admin", "prox3_admin"]
#eapi = EapiRequests.file('geic-sandbox', tenant=tenant, user='prox2_admin', password='P@ssw0rd')
eapi = EapiRequests.file('geic-qa4', tenant=tenant)


print('Searching or template:')
t = AirSyncTemplate.get_existing_template(client=eapi, description="LOCUST", number=24, version=1, template_type='CityIQ Software Update')

asdids = ["geicnode_pablo_8I6RT15_5C12569CFBE0"]
print('creating AirSyncDevice objects')
devices = [AirSyncDevice(eapi=eapi, asdid=asdid) for asdid in asdids]

print('Applaying template to devices:')

o = t.apply(devices=devices)
print('operation id: ', o.go_id)