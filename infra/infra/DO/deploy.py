import digitalocean
from time import sleep
import yaml
import paramiko


def wait_for_droplet(droplet):
    action = droplet.get_actions()[0]
    action.load()
    while action.status == "in-progress":
        print("Waiting for droplet {}".format(droplet.name))
        action.load()
        sleep(5)
    print("Done")


with open("config.yml", 'r') as config:
    cfg = yaml.load(config)


manager = digitalocean.Manager(token=cfg["token"])
keys = [manager.get_ssh_key(i) for i in cfg["keys"]]

WORK_DICT = {"token": cfg["token"],
             "region": cfg["region"],
             "ssh_keys": keys,
             "backups": False}

monitoring_cfg = cfg["monitoring"]
monitoring_cfg.update(WORK_DICT)
monitoring_cfg["user_data"] = open(monitoring_cfg["user_data"]).read()
monitoring_cfg["name"] = "monitoring-prod"
monitoring = digitalocean.Droplet(**monitoring_cfg)
monitoring.create()
wait_for_droplet(monitoring)
print("Monitoring created")

db_cfg = cfg["db"]
db_cfg.update(WORK_DICT)
db_cfg["user_data"] = open(db_cfg["user_data"]).read()
db_cfg["name"] = "db-prod"

db_nodes = []
for i in range(0, cfg["db_number"]):
    db_droplet = digitalocean.Droplet(**db_cfg)
    db_droplet.create()
    db_nodes.append(db_droplet)
print("DB created")
for i in db_nodes:
    wait_for_droplet(i)

rule = digitalocean.ForwardingRule(
    entry_protocol=cfg["loadbalancer"]["entry_protocol"],
    entry_port=cfg["loadbalancer"]["entry_port"],
    target_protocol=cfg["loadbalancer"]["target_protocol"],
    target_port=cfg["loadbalancer"]["target_port"])
hc = digitalocean.HealthCheck(
    protocol="tcp", port=cfg["loadbalancer"]["hc_port"],
    check_interval_seconds=3,
    response_timeout_seconds=3,
    healthy_threshold=2,
    unhealthy_threshold=2,
    path=None)
rules = []
rules.append(rule)
balancer = digitalocean.LoadBalancer(name="prod",
                                     token=cfg["token"],
                                     region="lon1",
                                     forwarding_rules=rules,
                                     health_check=hc)
balancer.create(region="lon1",
                algorithm=cfg["loadbalancer"]["algorithm"],
                health_check=hc)
balancer.load()
print("creating balancer")
while balancer.status == "new":
    balancer.load()
    print(balancer.status)
    sleep(10)
print("Balancer created")
# get db nodes
droplets = manager.get_all_droplets()
db_nodes = [i.ip_address for i in droplets if i.name == "db-prod"]
addresses = ",".join(db_nodes)
print(addresses)
command = "sed -i \"s%SEEDS%{}%\" /etc/cassandra/cassandra.yaml && service \
           cassandra restart".format(addresses)

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.client.AutoAddPolicy())

for node in db_nodes:
    client.connect(node, key_filename=cfg["ssh_key"], username="root")
    stdin, stdout, stderr = client.exec_command(command)
print("DB configured")
sleep(60)

api_cfg = cfg["api"]
api_cfg.update(WORK_DICT)
api_cfg["user_data"] = open(api_cfg["user_data"]).read()
api_cfg["name"] = "api-prod"

api_nodes = []
for i in range(0, cfg["api_number"]):
    api_droplet = digitalocean.Droplet(**api_cfg)
    api_droplet.create()
    api_nodes.append(api_droplet)
print("API created")
client_cfg = cfg["client"]
client_cfg.update(WORK_DICT)
client_cfg["user_data"] = open(client_cfg["user_data"]).read()
client_cfg["name"] = "client-prod"

client_nodes = []
for i in range(0, cfg["client_number"]):
    client_droplet = digitalocean.Droplet(**client_cfg)
    client_droplet.create()
    client_nodes.append(client_droplet)
print("Client created")
merged_nodes = api_nodes + client_nodes

for i in merged_nodes:
    wait_for_droplet(i)

