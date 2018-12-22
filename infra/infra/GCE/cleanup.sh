#!/bin/bash
set -x
ZONE=europe-west1-b
pids=""

echo -e "Y \n" | gcloud compute instance-groups managed delete db-nodes & 
pids="$pids $!"
echo -e "Y \n" | gcloud compute instance-groups managed delete client-nodes & 
pids="$pids $!"
echo -e "Y \n" | gcloud compute firewall-rules delete kibana-and-elastic & 
pids="$pids $!"
echo -e "Y \n" | gcloud compute firewall-rules delete srv-and-hc & 
pids="$pids $!"
echo "Y \n" | gcloud compute instance-groups managed delete monitoring-nodes & 
pids="$pids $!"
echo -e "Y \n" | gcloud beta compute forwarding-rules delete api-forwarding-rule --global
echo -e "Y \n" | gcloud compute addresses delete proxy-ipv4 --global 
echo -e "Y \n" | gcloud compute target-tcp-proxies delete api-proxy 
echo -e "Y \n" | gcloud compute backend-services delete api-lb --global 
echo -e "Y \n" | gcloud compute health-checks delete api-hc & 
pids="$pids $!"
echo -e "Y \n" | gcloud compute instance-groups managed delete api-nodes & 
pids="$pids $!" 
wait $pids
