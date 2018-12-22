#!/bin/bash
set -x
DOCTL=
HC_PORT=9990
DROPLET_ID="$(curl -s http://169.254.169.254/metadata/v1/id)"
DB_ADDRESS="$(doctl -t $DOCTL compute droplet list --format Name,PublicIPv4 | grep db-prod | awk '{print $2}' | tr '\n' ' ' | awk '{print $1}')"
git clone git@gitlab.com:jwalecki-inz/db.git
cd db
chmod +x api_startup.sh
sed -i "s%DB_ADDRESS%$DB_ADDRESS%" config.yml.example
./api_startup.sh $DROPLET_ID
if [ $(ps aux | grep gunicorn | wc -l ) -lt 1 ]; then
    ./api_startup.sh $DROPLET_ID
fi
if [ $(ps aux | grep gunicorn | wc -l ) -gt 0 ]; then
    . /etc/credentials
    LOADBALANCER_ID=$(doctl -t $DOCTL_TOKEN compute load-balancer list | grep prod | awk '{print $1}')
    doctl -t $DOCTL_TOKEN compute load-balancer add-droplets --droplet-ids $DROPLET_ID $LOADBALANCER_ID
    if [ $? -ne 0 ]; then
        echo "failed to add to lb"
        exit 1
    fi
    python /root/publisher.py --port $HC_PORT &
else
    #harakiri
    doctl -t $DOCTL_TOKEN compute droplet delete $DROPLET_ID  
fi
MONITORING_ADDRESS="$(doctl -t $DOCTL compute droplet list --format Name,PublicIPv4 | grep monitoring | awk '{print $2}')"
sed -i "s%KIBANA_ADDRESS%$MONITORING_ADDRESS:5601%" /etc/metricbeat/metricbeat.yml
sed -i "s%ES_ADDRESS%$MONITORING_ADDRESS:9200%" /etc/metricbeat/metricbeat.yml
hostname "api-$(ifconfig eth0 | grep 'inet '|awk '{print $2}'| sed "s%\.%-%g")"
metricbeat modules enable nginx 

service metricbeat start
echo "ok" > /executed