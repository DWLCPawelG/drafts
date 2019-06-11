from qalibs.eapi_request import EapiRequests
from qalibs.eapi_request.airsync_api.assertions import AirSyncAssertion
from qalibs.eapi_request.airsync_api.devices import AirSyncDevice

tenant = 2  # ["prox_admin", "prox2_admin", "prox3_admin"]
# eapi = EapiRequests.file('geic-sandbox', tenant=tenant, user='prox2_admin', password='P@ssw0rd')
eapi = EapiRequests.file('geic-qa2', tenant=tenant)

# connect manually a node via isap/run.py
node = AirSyncDevice(eapi=eapi, asdid="geic_gwa_4_11D8AF50D2E3")

# single assertion: POST /assertions
assertion = AirSyncAssertion.create_assertion(eapi=eapi, subject=f"devices/{node.asdid}",
                                              predicate="attributes/longitude", object="19.0308559238844")

# mutlitple assertions:
subject = f"$devices/{node.asdid}"
assertions = AirSyncAssertion.create_assertions(eapi, assertions=[(subject, "attributes/lunch", "burgers"),
                                                                  (subject, "attributes/breakfast", "cereal")])
