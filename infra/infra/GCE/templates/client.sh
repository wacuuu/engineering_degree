#!/bin/bash
INSTANCE_IMAGE=packer-client-1540922688
INSTANCE_TYPE=n1-standard-4
INSTANCE_INIT=./inits/client.sh
TEMPLATE_NAME=client-latest


gcloud compute instance-templates create $TEMPLATE_NAME \
--boot-disk-auto-delete \
--can-ip-forward \
--machine-type=$INSTANCE_TYPE \
--maintenance-policy=TERMINATE \
--metadata-from-file=startup-script=$INSTANCE_INIT \
--network-tier=STANDARD \
--preemptible \
--image=$INSTANCE_IMAGE \
--scopes=default,compute-rw \
--tags=client-nodes
