#!/bin/bash

for i in "$@"; do
case $i in
    -p|--platform)
        PLATFORM=$2
        shift
        shift
        ;;
esac
done
IMAGES="$@"

function run_worker (){
    packer build -machine-readable -only=$PLATFORM -var-file=services/$1.json packer.json 2>&1 > logs/$PLATFORM-$1.log
		echo "Done" >> logs/$PLATFORM-$1.log
}

pids=""
for i in $IMAGES; do
    run_worker $i &
    pids="$pids $!"
    sleep 1
    shift
done
wait $pids



