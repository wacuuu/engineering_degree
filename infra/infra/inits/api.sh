#!/bin/bash
set -x
DB_ADDRESS=209.97.132.115
HC_PORT=9990
DROPLET_ID="$(curl -s http://169.254.169.254/metadata/v1/id)"
git clone git@gitlab.com:jwalecki-inz/db.git
cd db
chmod +x api_startup.sh
sed -i "s%DB_ADDRESS%$DB_ADDRESS%" config.yml.example
./api_startup.sh $DROPLET_ID
sleep 3
if [ $(ps aux | grep gunicorn | wc -l ) -lt 3 ]; then
    ./api_startup.sh $DROPLET_ID
fi
if [ $(ps aux | grep gunicorn | wc -l ) -gt 3 ]; then
    . /etc/credentials
    LOADBALANCER_ID=$(doctl -t $DOCTL_TOKEN compute load-balancer list | grep prod | awk '{print $1}')
    doctl -t $DOCTL_TOKEN compute load-balancer add-droplets --droplet-ids $DROPLET_ID $LOADBALANCER_ID
    if [ $? -ne 0 ]; then
        echo "failed to add to lb"
        exit 1
    fi
    python /root/publisher.py --port $HC_PORT
else
    #harakiri
    doctl -t $DOCTL_TOKEN compute droplet delete $DROPLET_ID  
fi
echo "ok" > /executed