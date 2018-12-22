from .functions import process_dict
from .functions import parse_template
from .functions import TEMPLATES_FOLDER
import random
from cli import functions
from copy import copy
import binascii
import os
import re
import time
import yaml
API_ENDPOINT = "http://localhost:5000"
RANDOM_TEMPLATE = {"product_type": "random",
                   "parameters": {"a": {"b": "1", "c": "2"}}}


try:
    conf = yaml.load(open("config.yml", "r"))
    API_ENDPOINT = conf["API_ENDPOINT"]
except KeyError:
    print("No such key")
except IOError:
    print("No such file")


def menu_options():
    opt = int(input("1. Create\n2. Update\n3. Delete\n4. Show\n"))
    return opt


def check_existance(data):
    data.pop("parameters", None)
    if on_read(opt=3, data=data) == 0:
        return False
    else:
        return True


def create_product_by_user():
    print("Specify\n")
    data = {}
    date = input("Specify date: ")
    product_type = input("Specify type: ")
    product_id = input("Specify id: ")
    parameters = {}
    mopt = "y"
    while not mopt == "n":
        master = input("Master key: ")
        subdict = {}
        subopt = "y"
        while not subopt == "n":
            subkey = input("Subkey: ")
            subvalue = input("SubValue: ")
            subdict[subkey] = subvalue
            subopt = input("Continue subkeys? y/n ")
        parameters[master] = subdict
        mopt = input("Continue master? y/n ")
    data["date"] = date
    data["product_type"] = product_type
    data["product_id"] = product_id
    data["parameters"] = parameters
    return data


def create_product_from_template(opt=0):
    templates = [i for i in os.listdir(TEMPLATES_FOLDER)
                 if re.match("[a-zA-Z0-9]+\.template", i) is not None]
    if opt == 0:
        opt = int(input("1. Random\n2. Specified\n"))
    if opt == 1:
        template = random.randint(0, len(templates) - 1)
        template = str(TEMPLATES_FOLDER + templates[template])
        return process_dict(parse_template(template))
    if opt == 2:
        for i in range(0, len(templates)):
            print("{:<2} {:<10}".format(i, templates[i]))
        template = int(input("Pick template: "))
        template = str(TEMPLATES_FOLDER + templates[template])
        return process_dict(parse_template(template))


def pick_any_object():
    obj = functions.get_request(API_ENDPOINT, "api/read/", None)
    obj = obj.json()
    if isinstance(obj, list):
        # TODO: randa tutaj
        obj = obj[random.randint(0, len(obj) - 1)]
    return {"date": obj["date"],
            "product_id": obj["product_id"],
            "product_type": obj["product_type"]}


def pick_specified_object():
    print("Pick the one to delete")
    objs = functions.get_request(API_ENDPOINT, "api/read/", None)
    objs = objs.json()
    for i in range(0, len(objs)):
        print("{:<2} {:<10} {:<8} {}". format(i, objs[i]["date"],
                                              objs[i]["product_type"],
                                              objs[i]["product_id"]))
    sub = int(input("Pick the one to delete: "))
    return {"date": objs[sub]["date"],
            "product_id": objs[sub]["product_id"],
            "product_type": objs[sub]["product_type"]}


def on_create(opt=0):
    if opt == 0:
        opt = int(input("1. Random\n2. Specified\n3. From template\n"))
    if opt == 1:
        print("Generating random")
        data = process_dict(copy(RANDOM_TEMPLATE))
    elif opt == 2:
        data = create_product_by_user()
    elif opt == 3:
        data = create_product_from_template()
    elif opt == 4:
        data = create_product_from_template(opt=1)
        start_creation = time.time()
        functions.post_json(API_ENDPOINT, "api/create/", data)
        end_creation = time.time()
        status = check_existance(data)
        end_check = time.time()
        return status, end_creation - start_creation, end_check - end_creation
    functions.post_json(API_ENDPOINT, "api/create/", data)
    return check_existance(data)


def on_delete(opt=0):
    if opt == 0:
        opt = int(input("1. Random\n2. Specified\n"))
    if opt == 1:
        data = pick_any_object()
    elif opt == 2:
        data = pick_specified_object()
    if opt == 4:
        data = pick_any_object()
        start_delete = time.time()
        functions.post_json(API_ENDPOINT,
                            "api/delete/",
                            data=data)
        end_delete = time.time()
        status = check_existance(data)
        end_check = time.time()
        return not status, end_delete - start_delete, end_check - end_delete
    functions.post_json(API_ENDPOINT,
                        "api/delete/",
                        data=data)
    return check_existance(data)


def on_update(opt=0):
    if opt == 0:
        opt = int(input("1. Random\n2. Specified\n"))
    if opt == 1:
        obj = functions.get_request(API_ENDPOINT, "api/read/", None)
        obj = obj.json()
        if isinstance(obj, list):
            obj = obj[0]
        for i in obj["parameters"].keys():
            for j in obj["parameters"][i]:
                obj["parameters"][i][j] = binascii.hexlify(os.urandom(64)).decode("ascii")
        functions.post_json(API_ENDPOINT,
                            "api/update/",
                            data=obj)
    elif opt == 2:
        print("Pick the one update")
        objs = functions.get_request(API_ENDPOINT, "api/read/", None)
        objs = objs.json()
        for i in range(0, len(objs)):
            print("{:<2} {:<10} {:<8} {}". format(i, objs[i]["date"],
                                                  objs[i]["product_type"],
                                                  objs[i]["product_id"]))
        sub = int(input("Pick the one to update: "))
        parameters = {"updated": {"updated": str(binascii.
                                                 hexlify(os.
                                                         urandom(128)))}}
        functions.post_json(API_ENDPOINT,
                            "api/delete/",
                            data={"date": objs[sub]["date"],
                                  "product_id": objs[sub]["product_id"],
                                  "product_type": objs[sub]["product_type"],
                                  "parameters": parameters})
    if opt == 4:
        start_read = time.time()
        obj = functions.get_request(API_ENDPOINT, "api/read/", None)
        obj = obj.json()
        stop_read = time.time()
        if isinstance(obj, list):
            obj = obj[0]
        for i in obj["parameters"].keys():
            for j in obj["parameters"][i]:
                obj["parameters"][i][j] = binascii.hexlify(os.urandom(64)).decode("ascii")
        start_update = time.time()
        functions.post_json(API_ENDPOINT,
                            "api/update/",
                            data=obj)
        stop_update = time.time()
        return True, stop_update - start_update, stop_read - start_read


def on_read(opt=0, data=None):
    if opt == 0:
        opt = int(input("1. Random\n2. Specified\n"))
    if opt == 1:
        objs = functions.get_request(API_ENDPOINT, "api/read/", None)
        objs = objs.json()
        for i in range(0, len(objs)):
            print("{:<2} {:<10} {:<8} {}". format(i, objs[i]["date"],
                                                  objs[i]["product_type"],
                                                  objs[i]["product_id"]))
    elif opt == 2:
        product_type = str(input("Product type: "))
        date = str(input("Date: "))
        product_id = str(input("Product id: "))
        objs = functions.get_request(API_ENDPOINT,
                                     "api/read/",
                                     data={"date": date,
                                           "product_id": product_id,
                                           "product_type": product_type})
        objs = objs.json()
        for i in range(0, len(objs)):
            print("{:<2} {:<10} {:<8} {}". format(i, objs[i]["date"],
                                                  objs[i]["product_type"],
                                                  objs[i]["product_id"]))
    elif opt == 3:
        objs = functions.get_request(API_ENDPOINT,
                                     "api/read/",
                                     data=data)
        return len(objs.json())
    if opt == 4:
        start_reading = time.time()
        objs = functions.get_request(API_ENDPOINT, "api/read/", None)
        stop_reading = time.time()
        return True, stop_reading - start_reading, 0
    if opt == 5:
        start_read = time.time()
        objs = functions.get_request(API_ENDPOINT,
                                     "api/read/",
                                     data=data)
        stop_read = time.time()
        return objs.json(), stop_read - start_read
