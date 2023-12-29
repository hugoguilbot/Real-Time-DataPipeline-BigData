#!/bin/bash
set -e

# Mise à jour de pip et installation des dépendances
if [ -e "/opt/airflow/requirements.txt" ]; then
    python -m pip install --upgrade pip
    pip install --user -r /opt/airflow/requirements.txt
fi

# Initialisation de la base de données Airflow si elle n'existe pas
if [ ! -f "/opt/airflow/airflow.db" ]; then
    airflow db init && \
    airflow users create \
        --username admin \
        --firstname admin \
        --lastname admin \
        --role Admin \
        --email admin@example.com \
        --password admin
fi

# Mise à jour de la base de données Airflow
airflow db upgrade

# Démarrage du serveur web Airflow
exec airflow webserver
