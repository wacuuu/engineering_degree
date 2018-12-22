import yaml
from queue import Queue
from cli.client import *
import threading
from random import shuffle
import os
from random import randint
import time
import argparse
import csv

TERRORIST_CONFIG = "config.yml"
QUEUE = Queue()
OUTPUT = []
WRITE_QUEUE = Queue()


def read_config():
    config = open(TERRORIST_CONFIG, 'r')
    cfg = yaml.load(config)
    return cfg


def worker_thread():
    name = threading.currentThread().getName()
    while getattr(threading.currentThread(), "do_run", True):
        start_time = time.time()
        if QUEUE.qsize() == 0:
            break
        operation = QUEUE.get()
        if len(operation) == 0:
            continue
        # print("{:<15} {}".format(operation, QUEUE.qsize()))
        if operation == "create":
            try:
                result = on_create(4)
                WRITE_QUEUE.put({"thread": name,
                                 "operation": "create",
                                 "status": result[0],
                                 "o_time": result[1],
                                 "r_time": result[2],
                                 "start_time": start_time})
            except Exception:
                WRITE_QUEUE.put({"thread": name,
                                 "operation": "create",
                                 "status": True,
                                 "o_time": -1,
                                 "r_time": -1,
                                 "start_time": start_time})
        elif operation == "delete":
            try:
                result = on_delete(4)
                WRITE_QUEUE.put({"thread": name,
                                 "operation": "delete",
                                 "status": result[0],
                                 "o_time": result[1],
                                 "r_time": result[2],
                                 "start_time": start_time})
            except Exception:
                WRITE_QUEUE.put({"thread": name,
                                 "operation": "delete",
                                 "status": True,
                                 "o_time": -1,
                                 "r_time": -1,
                                 "start_time": start_time})
        elif operation == "update":
            try:
                result = on_update(4)
                WRITE_QUEUE.put({"thread": name,
                                 "operation": "update",
                                 "status": result[0],
                                 "o_time": result[1],
                                 "r_time": result[2],
                                 "start_time": start_time})
            except Exception:
                WRITE_QUEUE.put({"thread": name,
                                 "operation": "update",
                                 "status": True,
                                 "o_time": -1,
                                 "r_time": -1,
                                 "start_time": start_time})
        elif operation == "full_read":
            try:
                result = on_read(4)
                WRITE_QUEUE.put({"thread": name,
                                 "operation": "f_read",
                                 "status": result[0],
                                 "o_time": result[1],
                                 "r_time": result[2],
                                 "start_time": start_time})
            except Exception:
                WRITE_QUEUE.put({"thread": name,
                                 "operation": "f_read",
                                 "status": True,
                                 "o_time": -1,
                                 "r_time": -1,
                                 "start_time": start_time})
        elif operation == "targeted_read":
            try:
                targets, read_time = on_read(5)
                target = targets[randint(0, len(targets) - 1)]
                target.pop("parameters", "")
                result, op_time = on_read(opt=5, data=target)
                WRITE_QUEUE.put({"thread": name,
                                 "operation": "t_read",
                                 "status": True,
                                 "o_time": op_time,
                                 "r_time": read_time,
                                 "start_time": start_time})
            except Exception:
                WRITE_QUEUE.put({"thread": name,
                                 "operation": "t_read",
                                 "status": True,
                                 "o_time": -1,
                                 "r_time": -1,
                                 "start_time": start_time})
        else:
            print("FAIL")
        QUEUE.task_done()


def writer_wrapper(writer, served_writer):
    counter = 0
    while True:
        if WRITE_QUEUE.qsize() == 0:
            time.sleep(10)
            print("Writer is leaving sleep state. {} left. {} to write. {} threads active.".format(QUEUE.qsize(), WRITE_QUEUE.qsize(), threading.active_count()))
            served_writer.writerow({"timestamp": counter * 10,"served": WRITE_QUEUE.qsize()})
            counter = counter + 1
        writer.writerow(WRITE_QUEUE.get())
        WRITE_QUEUE.task_done()


def rate():
    while True:
        pre = QUEUE.qsize()
        time.sleep(5)
        post = QUEUE.qsize()
        print("\nTasks served in 5 seconds: {}\n".format(pre - post))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output', default="output.csv")
    args = parser.parse_args()
    config = read_config()
    value = binascii.hexlify(os.urandom(8)).decode("ascii")
    host_id = os.getenv("HOST_ID", default=value)
    for i in range(0, config["preheat_db"]):
        QUEUE.put("create")
    threads = []
    csvfile = open(args.output, 'w', newline='')
    fieldnames = ["thread", "operation", "status",
                  "o_time", "r_time", "start_time"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    served_file = open("served.csv", 'w', newline='')
    fieldnames = ["timestamp", "served"]
    served_writer = csv.DictWriter(served_file, fieldnames=fieldnames)
    writer.writeheader()
    served_writer.writeheader()
    for i in range(0, config["threads"]):
        name = "{}-preheat-{}".format(host_id, i)
        t = threading.Thread(target=worker_thread, name=name)
        t.daemon = True
        t.start()
        threads.append(t)
    t = threading.Thread(target=writer_wrapper, args=(writer, served_writer))
    t.daemon = True
    t.start()
    QUEUE.join()
    for i in threads:
        i.do_run = False
    time.sleep(1)
    operations = config["operations"]
    operations_list = []
    for key in operations.keys():
        for i in range(0, operations[key]):
            operations_list.append(key)
    shuffle(operations_list)
    for i in operations_list:
        QUEUE.put(i)
    for i in range(0, config["threads"]):
        name = "{}-running-{}".format(host_id, i)
        t = threading.Thread(target=worker_thread, name=name)
        t.daemon = True
        t.start()
    QUEUE.join()
    for i in threads:
        i.do_run = False
    time.sleep(1)
    WRITE_QUEUE.join()
    csvfile.close()
    served_file.close()
    print(threading.active_count())
