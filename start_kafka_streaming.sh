#!/bin/bash

# Nom du conteneur du script Kafka
CONTAINER_NAME=real-time-datapipeline-bigdata-kafka-script-1

echo "Démarrage du conteneur Kafka: $CONTAINER_NAME"

# Démarrer le conteneur
docker start $CONTAINER_NAME

echo "Conteneur démarré."
