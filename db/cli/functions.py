import requests
import os
import binascii
import json
from datetime import date
import random

TERRORIST_CONFIG = "config.yml"
TEMPLATES_FOLDER = "template_generation/"


def get_request(address, endpoint, data=None):
    if data is None:
        retval = requests.get(str(address + "/" + endpoint))
    else:
        retval = requests.get(str(address + "/" + endpoint), json=data)
    return retval


def post_json(address, endpoint, data=None):
    retval = requests.post(str(address + "/" + endpoint),
                           json=data,
                           headers={"Content-Type": "application/json"})
    return retval


def parse_template(template_location):
    file = open(template_location, "r")
    return json.load(file)


def process_dict(parsed_dict):
    year = random.randint(1978, 2018)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    production_date = str(date(year, month, day))
    parsed_dict["date"] = production_date
    product_id = binascii.hexlify(os.urandom(64)).decode("ascii")
    parsed_dict["product_id"] = product_id
    for key in parsed_dict["parameters"].keys():
        for subkey in parsed_dict["parameters"][key].keys():
            tmp = binascii.hexlify(os.urandom(64)).decode("ascii")
            parsed_dict["parameters"][key][subkey] = tmp
    return parsed_dict
