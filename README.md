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
    ./start_kafka_streaming.sh
    ```
    or
   ```bash
    ./stop_kafka_streaming.sh
    ```

## Spark

To access the Spark container:


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

The initial phase involved fetching data from an API. The data was processed using Spark by establishing a connection between Kafka and Spark. Following the processing, the data was transmitted to Cassandra through a connection. Grafana serves as the visualization tool for creating dashboards, facilitating real-time analysis of incoming information.

## Process
The first step is to access grafana at http://localhost:3000/.

![grafana_1](https://github.com/Laguilbee/Real-Time-DataPipeline-BigData/assets/48654943/e22c74b0-b21c-4243-b431-1da7f5fca020)

As you can see, you can add data sources and dashboards once your data source is configured. Now we'll start by adding our Cassandra data source, installing it first on grafana if no such source exists. 

![grafana_3](https://github.com/Laguilbee/Real-Time-DataPipeline-BigData/assets/48654943/75e94938-5bb0-4b14-a6d0-99322f38ea75)

After installing it, now you need to add it as a data source.

![grafana_2](https://github.com/Laguilbee/Real-Time-DataPipeline-BigData/assets/48654943/cf0ce1ac-1edd-43f1-844e-fbe641666527)

You need to link to cassandra by specifying the cassandra port and other information that is not mandatory, such as keyspace. If you don't specify the keyspace, it will automatically detect all existing keyspaces on your cassandra. 

![grafana_4](https://github.com/Laguilbee/Real-Time-DataPipeline-BigData/assets/48654943/ff5c8e7f-78d7-4410-9fdb-78dc7d5e563a)

once the connection between cassandra and grafana has been established, we can start creating our dashboards. To create your first dashboard, go to 'create your first dashboard' on the grafana home page. You can access the list of dashboards you've created at any time by clicking on Dashboards. 
to start creating your first dashboard, you'll need to add a visualization by clicking on 'add visualization'. 

![grafana_5](https://github.com/Laguilbee/Real-Time-DataPipeline-BigData/assets/48654943/a84df548-6ed5-4fe6-ad8f-62dc6acf1584)

Here, you select the data source you've already added and add your dashboard, which we've named 'New dashboard'. 

![grafana_6](https://github.com/Laguilbee/Real-Time-DataPipeline-BigData/assets/48654943/4c8e7345-d2ae-470e-8226-eebab0f8639e)

Now we'll access our created dashboard to create several visualizations of the created 'companies_created' table. 

We obtain the interaction interface with our dashboard. this interface contains several key elements to be defined: time range (last 6 hours, last 2 days, last 3 months...) to take into account the data range of your choice from the cassandra table.


![grafana_7](https://github.com/Laguilbee/Real-Time-DataPipeline-BigData/assets/48654943/69646c91-0615-4cc1-9805-813e6d0a1c4b)

As you can see, there are several types of visualization you can use: time series, bar chart, histogram, stat, trend... For each type of visualization, there are several types of parameters to be defined in the graph. 

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
