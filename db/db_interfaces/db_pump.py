import os
import binascii
import argparse
import json
from datetime import date
import random
from .db_operations import init_db, write
from queue import Queue
import threading


QUEUE = Queue()


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


def put_to_db(object_dict):
    init_db()
    write(object_dict)


def worker_thread():
    while True:
        processed_dict = process_dict(QUEUE.get())
        write(processed_dict)
        QUEUE.task_done()


def producer(quantities):
    init_db()
    for key in quantities.keys():
        parsed_dict = parse_template(key)
        for i in range(0, quantities[key]):
            QUEUE.put(parsed_dict)

    for i in range(0, os.cpu_count()):
        t = threading.Thread(target=worker_thread)
        t.daemon = True
        t.start()
    QUEUE.join()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Perhaps \
    you want to run for i in $(ll ../template_generation/*template|awk \
    '{print $NF}'); do python db_pump.py -t $i -o $(echo $i |awk -F'/' \
    '{print $NF}'| sed 's/template/out/'); done")
    parser.add_argument('-t', '--template', type=str)
    parser.add_argument('-o', '--output', type=str, default="0")
    args = parser.parse_args()
    parsed_dict = parse_template(args.template)
    processed_dict = process_dict(parsed_dict)
    if args.output is not "0":
        out = open(args.output, "w")
        json.dump(processed_dict, out)
    elif args.output is not "1":
        put_to_db(processed_dict)
    else:
        print("Are you aware the output is not set?")
