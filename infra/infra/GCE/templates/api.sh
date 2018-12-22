#!/bin/bash
INSTANCE_IMAGE=packer-api-1541287183
INSTANCE_TYPE=n1-standard-1
INSTANCE_INIT=./inits/api.sh
TEMPLATE_NAME=api-latest


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
--tags=api-nodes
