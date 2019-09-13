from qalibs.eapi_request import EapiRequests


tenant = 1  # ["prox_admin", "prox2_admin", "prox3_admin"]
#eapi = EapiRequests.file('geic-sandbox', tenant=tenant, user='prox2_admin', password='P@ssw0rd')
eapi = EapiRequests.file('geic-qa4', tenant=tenant)

body = [83699, 0, -1]

for i in body:
    put_request = eapi.send('PUT',
                            f'/system_settings?topic=/settings/nodes_and_components/remove_inactive_node_and_its_components/value',
                            body=i)
    print(put_request)
    get_request = eapi.send('GET',
                            f'/system_settings?topic=/settings/nodes_and_components/remove_inactive_node_and_its_components/value')

    print(get_request.json())


put_request = eapi.send('PUT', f'/system_settings?topic=/settings/nodes_and_components/remove_inactive_node_and_its_components/value', body=body)
get_request = eapi.send('GET', f'/system_settings?topic=/settings/nodes_and_components/remove_inactive_components/value')