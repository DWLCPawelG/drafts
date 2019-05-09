from time import time

# Requires requests library. Install using pip
import requests


class EapiRequests(object):
    """Allows to make requests to EAPI on given setup."""

    def __init__(self, eapi_url, rui_url, user_name, user_password):
        """
        :param eapi_url: Eapi address on tested setup in following format: ^http[s]?:\/\/[a-z0-9\.-]+\.com$
        :type eapi_url: str
        :param rui_url: Rui address on tested setup in following format: ^http[s]?:\/\/[a-z0-9\.-]+\.com$
        :type rui_url: str
        :type user_name: str
        :type user_password: str
        """
        self.eapi_url = eapi_url + '/rest/'
        self.rui_url = rui_url + '/oauth/token'
        self.user_name = user_name
        self.user_password = user_password
        self.token = self._generate_token()

    def request(self, method, command, **kwargs):
        """Creates request to EAPI.
        See http://docs.python-requests.org/en/master/api/ for documentation on arguments.
        """
        response = requests.request(method.upper(), self.eapi_url + command, headers={
            'Authorization': self.token, 'Content-Type': 'application/json'}, verify=False,
                                    **kwargs)
        return response

    def _generate_token(self):
        """Returns token used for authentication"""
        return 'bearer ' + requests.post(url=self.rui_url,
                                         data={'grant_type': 'password',
                                               'password': self.user_password,
                                               'response_type': 'token',
                                               'username': self.user_name},
                                         verify=False
                                         ).json()['access_token']


# Example usage:


# Create EapiRequests object using given setup/user parameters
eapi_requests = EapiRequests(eapi_url='https://eapigeic-qa2.proximetry.com',
                             rui_url='https://geic-qa2.proximetry.com',
                             user_name='user05',
                             user_password='P@ssw0rd')
# Send request to retrieve details about first device from systems
systems_response = eapi_requests.request('GET', '1.9/systems', params={'limit': 1})
# Retrieve asdid from response
asdid = systems_response.json()[0]['asdid']
# Set alarm for device identified by asdid taken from system
set_alarm_response = eapi_requests.request('PATCH',
                                           '2.0/devices/{}/alarms'.format(asdid),
                                           json={
                                               "data": [
                                                   {
                                                       "alarm_id": "test_alarm_1",
                                                       "action": "SET",
                                                       "timestamp": int(time()) * 1000,
                                                       "severity": "EMERGENCY",
                                                       "description": "Device overheating",
                                                       "details": "Temperature is above safe levels",
                                                       "optional": {}
                                                   }
                                               ]
                                           }
                                           )

activation_codes = eapi_requests.request('GET', '2.0/activation_codes')
#print(activation_codes.json())
#print(systems_response.json())
#print(asdid)


def test_case_no1_get_all_devices(method, endpoint):
    response = eapi_requests.request(method, endpoint)
    if response.status_code != 200:
        print('Error')
    return response.json()


#print(test_case_no1_get_all_devices('GET', '2.0/devices'))

def test_case_no2_get_device_alarms_by_id(method, endpoint):
    response = eapi_requests.request(method, endpoint)
    if response.status_code != 200:
        return 'Error'
    return response.json()

#print(test_case_no2_get_device_alarms_by_id('GET', '2.0/devices/1482B5C22571/alarms'))

def test_case_no3_set_alarm_severity_to_emergency(method, endpoint):
    response = eapi_requests.request(method, endpoint, json={
                                               "data": [
                                                   {
                                                       "alarm_id": "string",
                                                       "action": "SET",
                                                       "timestamp": 1518556647391,
                                                       "severity": "EMERGENCY",
                                                       "description": "string",
                                                       "details": "string",
                                                       "optional": {}
                                                   }
                                               ]
                                           }
                                           )
    if response.status_code != 200:
        return 'Error'
    return response.json()


#print(test_case_no3_set_alarm_severity_to_emergency('PATCH', '2.0/devices/1482B5C22571/alarms'.format(asdid)))


def test_case_no4_set_alarm_severity_to_fatal(method, endpoint):
    response = eapi_requests.request(method, endpoint, json={
                                               "data": [
                                                   {
                                                       "alarm_id": "string",
                                                       "action": "SET",
                                                       "timestamp": 1518556647391,
                                                       "severity": "FATAL",
                                                       "description": "string",
                                                       "details": "string",
                                                       "optional": {}
                                                   }
                                               ]
                                           }
                                           )
    if response.status_code != 200:
        return 'Error'
    return response.json()


#print(test_case_no4_set_alarm_severity_to_fatal('PATCH', '2.0/devices/1482B5C22571/alarms'.format(asdid)))


def test_case_no5_set_alarm_state_to_clear(method, endpoint):
    response = eapi_requests.request(method, endpoint, json={
                                               "data": [
                                                   {
                                                       "alarm_id": "string",
                                                       "action": "CLEAR",
                                                       "timestamp": 1518556647392,
                                                       "severity": "FATAL",
                                                       "description": "string",
                                                       "details": "string",
                                                       "optional": {}
                                                   }
                                               ]
                                           }
                                           )
    if response.status_code != 200:
        return 'Error'
    return response.json()

#print(test_case_no5_set_alarm_state_to_clear('PATCH', '2.0/devices/1482B5C22571/alarms'.format(asdid)))


def test_case_no7_delete_alarm_of_device_by_id(method, endpoint):  # to niedokończone :(
    response = eapi_requests.request(method, endpoint)
    if response.status_code != 204:
        return 'Error'
    return response.status_code()

# print(test_case_no7_delete_alarm_of_device_by_id('DELETE', '2.0/devices/088FA67C5907/alarms'.format(asdid))) #niedokończone, nie działa


