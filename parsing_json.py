import os
import json
from pprint import pprint


json_data = '{"a": 1, "b": 2, "c": 3, "d": 4, "e": 5}'
pprint(json.loads(json_data)) # loads - from json string to json

with open('../pdm-qa-tests/geic/device_mapping.json', 'r') as file:
    parsed_file = json.load(file) # load = from json file to dict
    pprint(json.dumps(parsed_file))  # dumps = from dict to json format
    pprint(parsed_file)