# Dashboard with grafana

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

As a first visualization, you can choose to execute the following query using the CQL language:

```bash
select timestamp_column, investment_received from spark_streams.companies_created;
```

![grafana_8](https://github.com/Laguilbee/Real-Time-DataPipeline-BigData/assets/48654943/30c71f6b-0514-4126-9e49-db4384fc4e62)

This graph shows a time series display of all investments received for the range of data collected over the last 2 days. 
