# Realtime Data Data Pipeline Big Data

## Table of Contents
- [Introduction](#introduction)
- [System Architecture](#system-architecture)
- [Technologies](#technologies)
- [Getting Started](#getting-started)
- [Apache Kafka](#apache-kafka)
- [Spark](#spark)
- [Cassandra](#cassandra)
- [Dashboard with grafana](#dashboard-with-grafana) 


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
- **Grafana**: We use to visualise our dashboard.

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
- Grafana

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
    docker-compose up -d
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
    ./start_kafka_streaming.sh
    ```
    or
   ```bash
    ./stop_kafka_streaming.sh
    ```

## Spark

To access the Spark container, open a new terminal :


```bash
docker exec -it spark-master /bin/bash
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


## Dashboard with grafana

The initial phase of this project involves retrieving data from an API. This data is then processed using Spark, which establishes a connection between Kafka and Spark for this purpose. After processing, the data is sent to Cassandra via a dedicated connection. Grafana is utilized as the visualization tool for creating dashboards, enabling the real-time analysis of the incoming data.

## Process

To begin, access Grafana at http://localhost:3000/.

In the dashboard section, you might notice that the dashboards appear empty. This is due to the Cassandra and Grafana connection not being correctly established yet. To rectify this, you need to navigate through the menu by clicking on 'Open Menu', then go to 'Configuration', and select 'Data Sources'. Click on 'Cassandra', and at the bottom of the page, click on 'Save & Test'.

![image](https://github.com/Laguilbee/Real-Time-DataPipeline-BigData/assets/78367566/881d3278-29a4-4c38-b47a-ca02b46402f5)

If the connection is successful, you can return to the dashboard, and you should be able to see the graphs.

There is an alternative method, but it is not recommended.

![grafana_1](https://github.com/Laguilbee/Real-Time-DataPipeline-BigData/assets/48654943/e22c74b0-b21c-4243-b431-1da7f5fca020)


## Importing dashboard

It's possible to import the dashboard we've created using the 'New dashboard-1707216913330.json' file. 


![grafana_16](https://github.com/Laguilbee/Real-Time-DataPipeline-BigData/assets/48654943/550e7f03-d9b2-4c57-b5cc-1b87628bd804)

You can now upload your dashboard via your json file. If you already have data inside your Cassandra table, you will be able to visualize your dashboard where you will find your cql queries. 

![grafana_17](https://github.com/Laguilbee/Real-Time-DataPipeline-BigData/assets/48654943/a3402bc8-bf0b-48b0-9b60-6062094ea92d)

Note that after importing your dashboard, it's important to refresh every panel in the dashboard so that you can visualize your graphic. Otherwise, nothing will be visible. 






## First visualization: Selecting investment received by all companies

As a first visualization, you can choose to execute the following query using the CQL language:

```bash
select timestamp_column, investment_received from spark_streams.companies_created;
```

![grafana_8](https://github.com/Laguilbee/Real-Time-DataPipeline-BigData/assets/48654943/30c71f6b-0514-4126-9e49-db4384fc4e62)

This graph shows a time series display of all investments received for the range of data collected.

## Second visualization: Average investement per country

A second visualization shows the average investment for several selected countries: France, Egypt, Australia, Morocco, Singapore and Luxembourg. Here is an example of the query used, you can change the country according to the visualization you want:

```bash
select timestamp_column, country, AVG(investment_received) AS average_investment from spark_streams.companies_created WHERE country='France' ALLOW FILTERING;
```

![grafana_9](https://github.com/Laguilbee/Real-Time-DataPipeline-BigData/assets/48654943/96f0d1c2-5b5c-4e44-886d-219d067a9e56)

## Third visualization: Average revenue per country

A third visualization shows the average revenue for the same countries selected.

```bash
select timestamp_column, country, AVG(revenue) AS average_revenue from spark_streams.companies_created WHERE country='France' ALLOW FILTERING;
```

![grafana_10](https://github.com/Laguilbee/Real-Time-DataPipeline-BigData/assets/48654943/f72bc6d9-5cfe-4389-b26b-2cd407911c67)

## Fourth visualization: Average number of employees per country

A fourth visualization shows the average number of employees for the same countries selected.

```bash
select timestamp_column, country, AVG(number_of_employees) AS average_employees from spark_streams.companies_created WHERE country='France' ALLOW FILTERING;
```

![grafana_11](https://github.com/Laguilbee/Real-Time-DataPipeline-BigData/assets/48654943/836439c8-d24b-4248-86f9-fbdf6fd63b6c)

## Fifth visualization: Proportion of revenue according to the investment received

A next visualization shows the proportion of revenue to investment rates for the same selected countries. 

```bash
SELECT timestamp_column, country, SUM(revenue) / SUM(investment_received) * 100 AS investment_percentage FROM spark_streams.companies_created WHERE country='France' ALLOW FILTERING;
```

![grafana_12](https://github.com/Laguilbee/Real-Time-DataPipeline-BigData/assets/48654943/d203c6b7-fb61-41af-a50b-363102daf1b6)

## Visualization : Company size according to the number of employees

A next visualization shows the company size according to the number of employees. 

```bash
SELECT timestamp_column, COUNT(name) FROM spark_streams.companies_created WHERE number_of_employees >= 10 AND number_of_employees < 49 ALLOW FILTERING;;
```
![grafana_13](https://github.com/Laguilbee/Real-Time-DataPipeline-BigData/assets/48654943/4b7a3997-5ce0-4523-8ba7-f8d0de0d1601)

## Visualization : Number of companies per sector

To visualize the number of companies per sector, we execute the following query:

```bash
SELECT timestamp_column, COUNT(name) FROM spark_streams.companies_created WHERE sector='Technology' ALLOW FILTERING; 
```
We do the same for other sectors.

![grafana_14](https://github.com/Laguilbee/Real-Time-DataPipeline-BigData/assets/48654943/dd3bb062-5302-4b90-ac92-963f1b088d5c)

## Visualization : Number of employees per sector

To visualize the number of employees per sector, we execute the following query:

```bash
SELECT timestamp_column, SUM(number_of_employees) FROM spark_streams.companies_created WHERE sector='Technology' ALLOW FILTERING;
```

We do it for all the other sectors. 

![grafana_15](https://github.com/Laguilbee/Real-Time-DataPipeline-BigData/assets/48654943/a86875b4-d8ed-46cc-a289-8546631c9a33)


