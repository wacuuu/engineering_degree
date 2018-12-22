#!/bin/bash
#set -x
set -e
DOCTL=
KEY="22606951,18830428"
KEY_PATH=../../images/keys/prod.pem
SERVICE_PORT=8098
HC_PORT=9990
DB_IMAGE=39234350
DB_INIT=./inits/db_parent.sh
API_IMAGE=39234448
API_INIT=./inits/api.sh
CLIENT_IMAGE=39234415
CLIENT_NUMBER=1
pids=""
MONITORING_IMAGE=39234374
MONITORING_INIT=./inits/monitoring.sh
# DB_SIZE=s-2vcpu-4gb
# API_SIZE=512mb
# CLIENT_SIZE=512mb
# MONITORING_SIZE=s-4vcpu-8gb
DB_SIZE=s-2vcpu-4gb
API_SIZE=512mb
CLIENT_SIZE=s-6vcpu-16gb
MONITORING_SIZE=s-1vcpu-3gb
sleep_for () {
    for i in $(seq 1 $1); do
        echo "Sleeping $i out of $1 for $2"
        sleep $2
    done
}

doctl -t $DOCTL compute droplet create --image $MONITORING_IMAGE --size $MONITORING_SIZE --ssh-keys $KEY --region lon1 --user-data-file $MONITORING_INIT monitoring-prod
sleep_for 6 10
#make loadbalancer
doctl compute load-balancer create -t $DOCTL --forwarding-rules entry_protocol:tcp,entry_port:$SERVICE_PORT,target_protocol:tcp,target_port:$SERVICE_PORT --health-check protocol:tcp,port:$HC_PORT,check_interval_seconds:3,response_timeout_seconds:5,healthy_threshold:2,unhealthy_threshold:2 --name prod --region lon1
#start db
for i in $(seq 1 3); do
    doctl -t $DOCTL compute droplet create --image $DB_IMAGE --size $DB_SIZE --ssh-keys $KEY --region lon1 --user-data-file $DB_INIT db-prod
done
#wait for them to bootup
sleep_for 18 10
#stich togeteher
DB_NODES="$(doctl -t $DOCTL compute droplet list | grep db-prod| awk '{print $3}'| tr '\n' ' ')"
# echo $DB_NODES
NEW_SEEDS="$(echo $DB_NODES| sed 's% %,%g')"
# also fix db init
# sed -i ""./inits/db.sh
set -x
for i in $DB_NODES; do
    ssh -i $KEY_PATH root@$i "sed -i "s%SEEDS%$NEW_SEEDS%" /etc/cassandra/cassandra.yaml && service cassandra restart"
done
set +x
doctl -t $DOCTL compute droplet list --format Name,PublicIPv4
#wait for nodetool to show 2 nodes
sleep_for 6 10
#fix api init
# sed -i "s%^DB_ADDRESS.*%DB_ADDRESS=$(echo $NEW_SEEDS | awk -F',' '{print $1}')%" ../inits/api.sh
#start api
doctl -t $DOCTL compute droplet create --image $API_IMAGE --size $API_SIZE --ssh-keys $KEY --region lon1 --user-data-file $API_INIT api-prod &
pids="$pids $!"
#start client
for i in $(seq 1 $CLIENT_NUMBER); do
    doctl -t $DOCTL compute droplet create --image $CLIENT_IMAGE --size $CLIENT_SIZE --ssh-keys $KEY --region lon1 client-prod &
    pids="$pids $!"
done
sleep_for 1 5
wait $pids
echo "Loadbalancer $(doctl compute load-balancer list | grep -v ID | awk '{print $2}')"
doctl -t $DOCTL compute droplet list --format "Name,PublicIPv4"
