#!/bin/bash

# Nom du conteneur du script Kafka
CONTAINER_NAME=real-time-datapipeline-bigdata-kafka-script-1

echo "Arrêt du conteneur Kafka: $CONTAINER_NAME"

# Arrêter le conteneur
docker stop $CONTAINER_NAME

echo "Conteneur arrêté."
