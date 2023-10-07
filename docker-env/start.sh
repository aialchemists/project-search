#!/bin/bash 

rm -rf /docker
mkdir -p /docker
mkdir -p /docker/controlcenter/data

mkdir -p /docker/es01/data
mkdir -p /docker/es02/data

mkdir -p /docker/schemaregistry/data

mkdir -p /docker/jupyter/data

mkdir -p /docker/redis/data

mkdir -p /docker/zookeeper/data
mkdir -p /docker/zookeeper/log

mkdir -p /docker/postgresql/data
mkdir -p /docker/kibana/data
mkdir -p /docker/broker/data

mkdir -p /docker/rayworker
mkdir -p /docker/rayserve
mkdir -p /docker/rayhead

chown -R 1000.1000 /docker
chown -R 1000.1000 /docker/postgresql
chown -R 1000.1000 /docker/kibana
chown -R 1000.1000 /docker/redis
chown -R 1000.1000 /docker/zookeeper
chown -R 1000.1000 /docker/es01
chown -R 1000.1000 /docker/jupyter
chown -R 1000.1000 /docker/es02
chown -R 1000.1000 /docker/broker
chown -R 1000.1000 /docker/schemaregistry
chown -R 1000.1000 /docker/controlcenter
chown -R 1000.1000 /docker/rayworker
chown -R 1000.1000 /docker/rayserve
chown -R 1000.1000 /docker/rayhead

chmod a+w /docker/postgresql
chmod a+w /docker/kibana
chmod a+w /docker/redis
chmod a+w /docker/zookeeper
chmod a+w /docker/es01
chmod a+w /docker/jupyter
chmod a+w /docker/es02
chmod a+w /docker/broker
chmod a+w /docker/schemaregistry
chmod a+w /docker/controlcenter
chmod a+w /docker/rayworker
chmod a+w /docker/rayserve
chmod a+w /docker/rayhead
