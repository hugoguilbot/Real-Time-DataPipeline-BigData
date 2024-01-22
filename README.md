# Realtime Data Data Pipeline Big Data

## Table of Contents
- [Introduction](#introduction)
- [System Architecture](#system-architecture)
- [Technologies](#technologies)
- [Getting Started](#getting-started)
- [Apache Kafka](#apache-kafka)
- [Spark](#spark)
- [Cassandra](#cassandra)


## Introduction
In the context of a Big Data course at INP Toulouse, our project aims to build a robust and efficient real-time data pipeline using Kafka, Spark, Grafana, and Cassandra. The goal of this pipeline is to stream and process data from a dynamic source, specifically generating and collecting information about companies in real-time. This data is then visualized on Grafana dashboards, allowing us to monitor and analyze key metrics and insights as they unfold.

## System Architecture

![Architecture data pipeline](https://github.com/Laguilbee/Real-Time-DataPipeline-BigData/assets/78367566/fd6010ad-a7e4-4d22-aa30-794c1387eff5)

An API generates random company data, which we retrieve every 10 seconds. Each message is read by a Kafka consumer using Spark Structured Streaming and written to a Cassandra table at regular intervals.

- **Data Source**: We use `fakerapi.it` API to generate random companies data for our pipeline.
- **Apache Kafka and Zookeeper**: Used for streaming data.
- **Control Center and Schema Registry**: Helps in monitoring and schema management of our Kafka streams.
- **Apache Spark**: For data processing with its master and worker nodes.
- **Cassandra**: Where the processed data will be stored.

Scripts:
- `stream_to_kafka.py`: Retrieves data from the API and sends it to a Kafka topic.
- `spark_stream.py`: Consumes data from the Kafka topic using Spark Structured Streaming.
- `start_kafka_streaming.sh`: Starts the Kafka streaming.
- `stop_kafka_streaming.sh`: Stops the Kafka streaming.

## Technologies

- Python
- Apache Kafka
- Apache Zookeeper
- Apache Spark
- Cassandra
- Docker

## Getting Started

1. Clone the repository:
    ```bash
    https://github.com/Laguilbee/Real-Time-DataPipeline-BigData.git
    ```
2. Navigate to the project directory:
    ```bash
    cd Real-Time-DataPipeline-BigData
    ```
3. Run Docker Compose to spin up the services:
    ```bash
    docker-compose up
    ```
## Apache Kafka

Once all the services are started, the Kafka streaming is running, and data is flowing into the Kafka topic. You can access the Kafka UI via the Control Center at `localhost:9021`.

<img width="1297" alt="confluent_UI" src="https://github.com/Laguilbee/Real-Time-DataPipeline-BigData/assets/78367566/c233db4a-65bd-47ac-a7f8-c0c39a9cfc88">


If you want to stop or start the streaming kafka :

1. Navigate to the project directory:
    ```bash
    cd Real-Time-DataPipeline-BigData
    ```
2. Run the scripts start_kakfka_streaming.sh ou stop_kakfka_streaming.sh:
    ```bash
    ./start_kakfka_streaming.sh
    ```
    or
   ```bash
    ./stop_kakfka_streaming.sh
    ```

## Spark

To access the Spark container:


```bash
docker exec -it real-time-datapipeline-bigdata-spark-master-1 /bin/bash
```
Run the following commands to install the Cassandra driver:

```bash
pip install cassandra-driver
```

Run the following command to submit the job to Spark with the necessary packages for Spark version 3.5.0 (latest version) and send the data to Cassandra:

```bash
cd /home
```
```bash
spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0,com.datastax.spark:spark-cassandra-connector_2.12:3.4.1 --master spark://spark-master:7077 spark_stream.py
```

You can monitor the process in the Spark UI at http://localhost:9090/.

<img width="1297" alt="UI_Spark" src="https://github.com/Laguilbee/Real-Time-DataPipeline-BigData/assets/78367566/107aaece-f3b9-42e3-806f-03d082f94753">

After these commands, the data should start being sent to Cassandra. To verify, you can follow the next section.

## Cassandra

In another terminal, access the Cassandra container:

```bash
docker exec -it cassandra cqlsh -u cassandra -p cassandra localhost 9042
```

To view the new data, you can execute: 
```bash
select * from spark_streams.companies_created;
```
Or to get the row count: 
```bash
select count(*) from spark_streams.companies_created;
```

Table cassandra : 

![table_cassandra](https://github.com/Laguilbee/Real-Time-DataPipeline-BigData/assets/78367566/14c6db67-294c-4862-a0fd-2c218286c49c)
