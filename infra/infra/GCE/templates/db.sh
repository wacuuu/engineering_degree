#!/bin/bash
INSTANCE_IMAGE=packer-db-1540922685
INSTANCE_TYPE=n1-standard-2
INSTANCE_INIT=./inits/db.sh
TEMPLATE_NAME=db-latest
DISC_SIZE=50


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
--boot-disk-size=$DISC_SIZE \
--tags=db-nodes

