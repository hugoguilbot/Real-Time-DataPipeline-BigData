#!/bin/bash

# Nom du conteneur du script Kafka
CONTAINER_NAME=kafka-script

echo "Démarrage du conteneur Kafka: $CONTAINER_NAME"

# Démarrer le conteneur
docker start $CONTAINER_NAME

echo "Conteneur démarré."
