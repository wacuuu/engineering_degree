#!/bin/bash
set -x
set -e
DOCTL=
KEY="22606951,18830428"
API_IMAGE=39234448
API_INIT=./inits/api.sh


doctl -t $DOCTL compute droplet create --image $API_IMAGE --size 512mb --ssh-keys $KEY --region lon1 --user-data-file $API_INIT api-prod 
