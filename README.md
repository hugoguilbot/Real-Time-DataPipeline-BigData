# Realtime Data Data Pipeline Big Data

## Table of Contents
- [Introduction]
- [System Architecture]

## Introduction
Dans le cadre d'un cours de BigData à L'inp Toulouse, nous devons créer un pipeline de données avec Kafka, Spark et Grafana.


## System Architecture

![Architecture data pipeline](https://github.com/Laguilbee/Real-Time-DataPipeline-BigData/assets/78367566/fd6010ad-a7e4-4d22-aa30-794c1387eff5)

Une API génère des entreprises aléatoirement, que nous venons récupérer toutes les 10 secondes. Every message is read by Kafka consumer using Spark Structured Streaming and written to Cassandra table on a regular interval.

- **Data Source**: We use `fakerapi.it` API to generate random companies data for our pipeline.
- **Apache Kafka and Zookeeper**: Used for streaming data.
- **Control Center and Schema Registry**: Helps in monitoring and schema management of our Kafka streams.
- **Apache Spark**: For data processing with its master and worker nodes.
- **Cassandra**: Where the processed data will be stored.

`stream_to_kafka.py` -> The script that gets the data from API and sends it to Kafka topic

`spark_stream.py` -> The script that consumes the data from Kafka topic with Spark Structured Streaming

`start_kakfka_streaming.sh` -> This script start the kafka streaming

`stop_kakfka_streaming.sh` -> This script stop the kafka streaming

## Technologies

- Python
- Apache Kafka
- Apache Zookeeper
- Apache Spark
- Cassandra
- Docker

## Getting Started

. Clone the repository:
    ```bash

    ```


