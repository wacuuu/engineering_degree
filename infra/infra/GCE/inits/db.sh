#!/bin/bash

set -x
iface="$(ifconfig | head -n1 | cut -d':' -f1)"
sed -i "s%LISTEN_ADDRESS%$(ifconfig $iface |grep -E 'inet '|awk '{print $2}')%" /etc/cassandra/cassandra.yaml
sed -i "s%BROADCAST_RPC_ADDRESS%$(ifconfig $iface |grep -E 'inet '|awk '{print $2}')%" /etc/cassandra/cassandra.yaml
DB_ADDRESS="$(gcloud compute instances list | grep db | awk '{print $5}' | tr '\n' ',')"
DB_ADDRESS=${DB_ADDRESS::-1}
sed -i "s%SEEDS%$DB_ADDRESS%" /etc/cassandra/cassandra.yaml
# get monitoring setup
MONITORING_ADDRESS="$(gcloud compute instances list | grep monitoring | awk '{print $5}')"
sed -i "s%KIBANA_ADDRESS%$MONITORING_ADDRESS:5601%" /etc/metricbeat/metricbeat.yml
sed -i "s%ES_ADDRESS%$MONITORING_ADDRESS:9200%" /etc/metricbeat/metricbeat.yml
hostname "db-$(ifconfig $iface | grep 'inet '|awk '{print $2}'| sed "s%\.%-%g")"
service metricbeat start
service cassandra restart
echo "ok" > /executeds
