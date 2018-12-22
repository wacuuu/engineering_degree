#!/bin/bash
set -x
sed -i "s%LISTEN_ADDRESS%$(ifconfig eth0 |grep -E 'inet '|awk '{print $2}')%" /etc/cassandra/cassandra.yaml
sed -i "s%BROADCAST_RPC_ADDRESS%$(ifconfig eth0 |grep -E 'inet '|awk '{print $2}')%" /etc/cassandra/cassandra.yaml

service cassandra restart
echo "ok" > /executed