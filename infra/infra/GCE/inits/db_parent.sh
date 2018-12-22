#!/bin/bash
DOCTL=

set -x
sed -i "s%LISTEN_ADDRESS%$(ifconfig eth0 |grep -E 'inet '|awk '{print $2}')%" /etc/cassandra/cassandra.yaml
sed -i "s%BROADCAST_RPC_ADDRESS%$(ifconfig eth0 |grep -E 'inet '|awk '{print $2}')%" /etc/cassandra/cassandra.yaml

# get monitoring setup
MONITORING_ADDRESS="$(doctl -t $DOCTL compute droplet list --format Name,PublicIPv4 | grep monitoring | awk '{print $2}')"
sed -i "s%KIBANA_ADDRESS%$MONITORING_ADDRESS:5601%" /etc/metricbeat/metricbeat.yml
sed -i "s%ES_ADDRESS%$MONITORING_ADDRESS:9200%" /etc/metricbeat/metricbeat.yml
hostname "db-$(ifconfig eth0 | grep 'inet '|awk '{print $2}'| sed "s%\.%-%g")"
service metricbeat start
service cassandra restart
echo "ok" > /executed