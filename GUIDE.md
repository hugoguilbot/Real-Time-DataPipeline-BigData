# Dashboard with grafana

The initial phase involved fetching data from an API. The data was processed using Spark by establishing a connection between Kafka and Spark. Following the processing, the data was transmitted to Cassandra through a connection. Grafana serves as the visualization tool for creating dashboards, facilitating real-time analysis of incoming information.

## Process
The first step is to access grafana via the localhost:3000 address.

![grafana_1](https://github.com/Laguilbee/Real-Time-DataPipeline-BigData/assets/48654943/e22c74b0-b21c-4243-b431-1da7f5fca020)

As you can see, you can add data sources and dashboards once your data source is configured. Now we'll start by adding our Cassandra data source, installing it first on grafana if no such source exists. 

![grafana_3](https://github.com/Laguilbee/Real-Time-DataPipeline-BigData/assets/48654943/75e94938-5bb0-4b14-a6d0-99322f38ea75)

After installing it, now you need to add it as a data source.

![grafana_2](https://github.com/Laguilbee/Real-Time-DataPipeline-BigData/assets/48654943/cf0ce1ac-1edd-43f1-844e-fbe641666527)

You need to link to cassandra by specifying the cassandra port and other information that is not mandatory, such as keyspace. If you don't specify the keyspace, it will automatically detect all existing keyspaces on your cassandra. 

![grafana_4](https://github.com/Laguilbee/Real-Time-DataPipeline-BigData/assets/48654943/ff5c8e7f-78d7-4410-9fdb-78dc7d5e563a)
