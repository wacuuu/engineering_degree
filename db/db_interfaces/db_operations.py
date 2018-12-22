from .object_mappers import main
from .db_init import init_db
import os
import re
import json
import copy

TEMPLATES_FOLDER = "template_generation/"


def setup_connection():
    return init_db()


def validate_input(data, parent_name):
    if parent_name == "write":
        if data["product_type"] == "random":
            return True
        else:
            template = [i for i in os.listdir(TEMPLATES_FOLDER)
                        if re.match(str(data["product_type"] +
                                        ".template"), i) is not None]
            if len(template) == 0:
                print("No matching template")
                return False
            template_keys = json.load(open(str(TEMPLATES_FOLDER +
                                               template[0])))["parameters"]
            request_keys = data["parameters"]
            if not set(template_keys.keys()) == set(request_keys.keys()):
                print("Mismatch in master keys")
                return False
            for i in template_keys.keys():
                template_sub_keys = template_keys[i].keys()
                request_sub_keys = request_keys[i].keys()
                if not set(template_sub_keys) == set(request_sub_keys):
                    print("Mismatch in sub keys")
                    return False
            return True
    else:
        return True


def write(data):
    if validate_input(data, "write"):
        main.create(**data)
    else:
        print("Data not valid")


def read(filter_params=None):
    if filter_params is None or len(filter_params.keys()) == 0:
        objects = main.objects.limit(20)
    else:
        if "product_id" in filter_params.keys():
            filter_params["product_id"] = str(filter_params["product_id"])
        objects = main.objects.filter(**filter_params)
    return [dict(i) for i in objects]


def update(new_object):
    if validate_input(new_object, "update"):
        copied = copy.copy(new_object)
        copied.pop("parameters", "")
        entry = main.filter(**copied)
        entry.update(parameters=new_object["parameters"])
    else:
        print("Data not valid")


def delete(old_object):
    if validate_input(old_object, "delete"):
        old_object.pop("parameters", None)
        main.objects(**old_object).delete()
    else:
        print("Data not valid")


def test():
    TEST1 = {"date": "2018-04-04",
             "product_type": "hedphones",
             "product_id": "oimrfikfkfrikp",
             "parameters": {"a": {"a": "rrfsd"}}}
    TEST2 = {"date": "2018-04-04",
             "product_type": "hedphones",
             "product_id": "oimrfikfkfssssrikp",
             "parameters": {"a": {"a": "rrfsd"}}}
    TEST3 = {"date": "2018-04-03",
             "product_type": "hedphones",
             "product_id": "oimrfikfkfssssrikp",
             "parameters": {"a": {"a": "rrfsd"}}}
    TEST4 = {"date": "2018-04-03",
             "product_type": "hedphones",
             "product_id": "oimrfikfkfssssrikp",
             "parameters": {"b": {"a": "rrfsd"}}}
    setup_connection()
    print("TEST WRITE")
    write(TEST1)
    write(TEST2)
    write(TEST3)
    objects = read()
    for i in objects:
        print(i)
    print("==========================================")
    print("TEST UPDATE")
    update(TEST3, TEST4)
    objects = read()
    for i in objects:
        print(i)
    print("==========================================")
    print("TEST DELETE")
    delete(TEST4)
    objects = read()
    for i in objects:
        print(i)


if __name__ == "__main__":
    test()
