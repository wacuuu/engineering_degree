from time import sleep
import yaml
import digitalocean
import requests
import json
from statistics import mean
import paramiko

with open("config.yml", 'r') as config:
    cfg = yaml.load(config)


manager = digitalocean.Manager(token=cfg["token"])
keys = [manager.get_ssh_key(i) for i in cfg["keys"]]

WORK_DICT = {"token": cfg["token"],
             "region": cfg["region"],
             "ssh_keys": keys,
             "backups": False}


def add_api():
    print("Adding api")
    api_cfg = cfg["api"]
    api_cfg.update(WORK_DICT)
    api_cfg["user_data"] = open(api_cfg["user_data"]).read()
    api_cfg["name"] = "api-prod"
    api_droplet = digitalocean.Droplet(**api_cfg)
    api_droplet.create()
    print("Done")


def remove_api():
    print("Removing api")
    # get them
    droplets = manager.get_all_droplets()
    api_nodes = [i for i in droplets if i.name == "api-prod"]
    # at least 2
    if len(api_nodes) < 2:
        print("Not enough to remove")
        return
    # else ssh
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.client.AutoAddPolicy())
    client.connect(api_nodes[0].ip_address,
                   key_filename=cfg["ssh_key"],
                   username="root")
    # stop publisher
    sin, sout, serr = client.exec_command("kill $(ps aux | \
                                           grep publisher.py | \
                                           awk '{print $2}')")
    print("Stoped publisher {}".format(api_nodes[0].ip_address))
    # sleep 20 sec
    sleep(30)
    print("Proceeding")
    # remove
    api_nodes[0].destroy()
    print("Done")


def get_request(address, endpoint, data=None):
    if data is None:
        retval = requests.get(str(address + "/" + endpoint))
    else:
        retval = requests.get(str(address + "/" + endpoint), json=data)
    return retval


request_file = open("request.json", "r").read()
query = json.loads(request_file)
query["query"]["bool"]["must"][1]["wildcard"]["host.name"] = "api-*"
print("Getting data from elastic")
request = get_request("http://{}:9200".format(cfg["elastic_address"]),
                      "_search",
                      query)
data = request.json()["hits"]["hits"]
print("Got data")
api_cpu = [float(i["_source"]["system"]["cpu"]["total"]["pct"])
           for i in data if "cpu" in i["_source"]["metricset"]["name"]]
api_in_network = [float(i["_source"]["system"]["network"]["in"]["bytes"])
                  for i in data if "network" in i["_source"]
                                                 ["metricset"]["name"]]
api_out_network = [float(i["_source"]["system"]["network"]["out"]["bytes"])
                   for i in data if "network" in i["_source"]
                                                  ["metricset"]["name"]]

mean_api_cpu = mean(api_cpu)
print("Mean cpu {}".format(mean_api_cpu))
if mean_api_cpu >= 0.45:
    add_api()
elif mean_api_cpu <= 0.1:
    remove_api()
else:
    print("Doing nothing in api")
