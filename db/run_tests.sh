#!/bin/bash
KEY=../infra/images/keys/prod.pem
COMMAND='./remote_exec.sh http://206.189.246.19:8098'

function run_worker (){
    LOCATION="$(ssh -i $KEY root@$1 "$COMMAND")"
    wget http://$1:8099/$LOCATION -O $1-$LOCATION
}

pids=""
while [ "$1" != "" ]; do
    run_worker $1 &
    pids="$pids $!"
    shift
done
wait $pids
