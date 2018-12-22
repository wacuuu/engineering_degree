#!/bin/bash
set -x
systemctl enable elasticsearch
systemctl enable kibana
free -h
sleep 15
service elasticsearch start
sleep 15
free -h
service kibana start
sleep 13
free -h
service elasticsearch restart
sed -i "s%KIBANA_ADDRESS%localhost:5601%" /etc/metricbeat/metricbeat.yml
sed -i "s%ES_ADDRESS%localhost:9200%" /etc/metricbeat/metricbeat.yml

# prepare to be used as control node
git clone git@gitlab.com:jwalecki-inz/infra.git /root/infra



sleep 120
metricbeat setup --dashboards
while(true); do
    date
    set +x
    source /root/venv/bin/activate
    set -x
    cd /root/infra/infra/DO
    python runner.py
    sleep 150
done &
