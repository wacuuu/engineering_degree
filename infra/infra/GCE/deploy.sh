#!/bin/bash
set -xe
# deploy db
ZONE=europe-west1-b
DB_NODES=2
API_NODES=1
CLIENT_NODES=1
pids=""

gcloud compute instance-groups managed create monitoring-nodes --size 1 --template monitoring-latest --base-instance-name monitoring --zone=$ZONE >> /dev/null 2>&1 &
pids="$pids $!"
gcloud compute firewall-rules create srv-and-hc --allow tcp:8098,tcp:9990 --target-tags api-nodes >> /dev/null 2>&1 &
pids="$pids $!"
gcloud compute firewall-rules create kibana-and-elastic --allow tcp:5601,tcp:9200 --target-tags monitoring-nodes >> /dev/null 2>&1 &
pids="$pids $!"
gcloud compute instance-groups managed create client-nodes --size $CLIENT_NODES --template client-latest --base-instance-name client --zone=$ZONE >> /dev/null 2>&1 &
pids="$pids $!"
gcloud compute health-checks create tcp api-hc --port=9990 &
pids="$pids $!"
gcloud compute addresses create proxy-ipv4 --ip-version=IPV4 --global &
pids="$pids $!"

wait $pids

gcloud compute instance-groups managed create db-nodes --size $DB_NODES --template db-latest --base-instance-name db --zone=$ZONE
sleep 60
gcloud compute instance-groups managed create api-nodes --size $API_NODES --template api-latest --base-instance-name api --zone=$ZONE
gcloud compute instance-groups set-named-ports api-nodes --named-ports tcp8098:8098,tcp9990:9990 --zone $ZONE
gcloud compute instance-groups managed set-autoscaling api-nodes --max-num-replicas 7 --min-num-replicas 1 --scale-based-on-cpu --target-cpu-utilization 0.45 --cool-down-period 120
gcloud compute backend-services create api-lb --global --protocol TCP --health-checks api-hc --timeout 5m --port-name tcp8098
gcloud compute backend-services add-backend api-lb --global --instance-group api-nodes --instance-group-zone europe-west1-b --balancing-mode CONNECTION --max-connections=100
gcloud compute target-tcp-proxies create api-proxy --backend-service api-lb --proxy-header NONE
gcloud beta compute forwarding-rules create api-forwarding-rule --global --target-tcp-proxy api-proxy --address proxy-ipv4 --ports 110
