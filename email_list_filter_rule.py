from qalibs.test_utils.geic_objects_factories import GEICUserFactory, GEICEmailListFactory, \
    GEICEmailRuleFactory
from qalibs.eapi_request import EapiRequests
from qalibs.eapi_request import EapiRequests, utils
from qalibs.eapi_request.airsync_api.devices import AirSyncDevice
from qalibs.eapi_request.airsync_api.templates import AirSyncTemplate, AirSyncBlob

tenant = 1  # ["prox_admin", "prox2_admin", "prox3_admin"]
#eapi = EapiRequests.file('geic-sandbox', tenant=tenant, user='prox2_admin', password='P@ssw0rd')
eapi = EapiRequests.file('geic-qa3', tenant=tenant)

email = GEICEmailListFactory()
email_list = email.create_or_update(eapi=eapi)

filter = GEICEmailRuleFactory()
filter_rule = filter.create_or_update(eapi=eapi, appenders=[email])
