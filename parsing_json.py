import os
import json
from pprint import pprint


json_data = '{"a": 1, "b": 2, "c": 3, "d": 4, "e": 5}'
pprint(json.loads(json_data)) # loads - from json string to json

with open('../pdm-qa-tests/geic/device_mapping.json', 'r') as file:
    parsed_file = json.load(file) # load = from json file to dict
    pprint(json.dumps(parsed_file))  # dumps = from dict to json format
    pprint(parsed_file)
    pprint([device['device_model_name'] for device in parsed_file['device_mapping']])


# dic = {'random': 'component'}
# for key, value in dic.items():
#     parameter_key = key
#     parameter_value = value
# parameter_key = [key for key, value in dic.items()]
# parameter_value = [value for key, value in dic.items()]
#
# print(str(parameter_key))
# print(parameter_value)
#
# aux_board_events = [component['events'] for component in parsed_file['device_mapping'] if
#                     component["device_model_name"] == 'aux-board'][0]
#
# pprint(aux_board_events)
# for event in aux_board_events:
#     pprint(event['id'])