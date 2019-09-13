
from qalibs.eapi_request import EapiRequests, utils
from qalibs.eapi_request.airsync_api.devices import AirSyncDevice
from qalibs.eapi_request.airsync_api.templates import AirSyncTemplate, AirSyncBlob

tenant = 1  # ["prox_admin", "prox2_admin", "prox3_admin"]
#eapi = EapiRequests.file('geic-sandbox', tenant=tenant, user='prox2_admin', password='P@ssw0rd')
eapi = EapiRequests.file('geic-qa3', tenant=tenant)

AirSyncTemplate.create_new_template(client=eapi, blob=AirSyncBlob.upload_new_blob_with_random_file(
                                                           client=eapi,
                                                           file_size=1024*1024*100 * 100, #this is 100MB
                                                           with_signature=False,
                                                           with_malformed_signature=False),
                                    template_type="CityIQ Software Update",
                                    template_description=f'100MB_upload')
