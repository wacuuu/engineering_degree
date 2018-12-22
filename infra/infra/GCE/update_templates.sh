#!/bin/bash
TEMPLATES="$@"

function run_worker (){
    OLD_TEMPLATE="$(gcloud compute instance-templates list | grep $1-latest | awk '{print $1}')"
    if [ -n "$OLD_TEMPLATE" ]; then
        echo "Y \n" | gcloud compute instance-templates delete $OLD_TEMPLATE
    fi
    ./templates/$1.sh
}

pids=""
for i in $TEMPLATES; do
    run_worker $i &
    pids="$pids $!"
    shift
done
wait $pids
