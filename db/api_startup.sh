#!/bin/bash
VIRTUALENV=/root/venv/bin/activate
SERVER_NAME="$1"
cp config.yml.example config.yml
#prepare db
source $VIRTUALENV && python db_interfaces/db_init.py
sleep 5
#run api
source $VIRTUALENV && gunicorn --log-file /var/log/gunicorn.log --log-level debug --env CQLENG_ALLOW_SCHEMA_MANAGEMENT=1 -w 1 -b unix:/dev/shm/gunicorn --pythonpath=$PWD --daemon api.app:app 
