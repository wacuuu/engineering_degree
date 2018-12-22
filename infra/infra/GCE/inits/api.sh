#!/bin/bash
set -x
# echo "lel"
# touch ~/jajeczko
# sudo touch /done
# sudo echo "$(whoami)" >> /var/log/user
# sudo su root
# sudo echo "$(whoami)" >> /var/log/root
HC_PORT=9990
HOST_ID="$(hostname)"
git clone git@gitlab.com:jwalecki-inz/db.git
cd db
chmod +x api_startup.sh
DB_ADDRESS="$(gcloud compute instances list | grep db | awk '{print $5}' | head -n1)"
if [ -z "$DB_ADDRESS" ]; then
    sleep 60
    DB_ADDRESS="$(gcloud compute instances list | grep db | awk '{print $5}' | head -n1)"
fi
sed -i "s%DB_ADDRESS%$DB_ADDRESS%" config.yml.example
./api_startup.sh $HOST_ID
if [ $(ps aux | grep gunicorn | wc -l ) -lt 1 ]; then
    ./api_startup.sh $HOST_ID
fi
python /root/publisher.py --port $HC_PORT &

MONITORING_ADDRESS="$(gcloud compute instances list | grep monitoring | awk '{print $5}')"

sed -i "s%KIBANA_ADDRESS%$MONITORING_ADDRESS:5601%" /etc/metricbeat/metricbeat.yml
sed -i "s%ES_ADDRESS%$MONITORING_ADDRESS:9200%" /etc/metricbeat/metricbeat.yml
metricbeat modules enable nginx

service metricbeat start
echo "ok" > /executed
