from array import ArrayType
import logging
import json
from cassandra.cluster import Cluster
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, IntegerType, ArrayType
from pyspark.sql.functions import from_json, col


def create_keyspace(session):
    session.execute("""
        CREATE KEYSPACE IF NOT EXISTS spark_streams
        WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '1'};
    """)

    print("Keyspace created successfully!")


def create_table(session):
    session.execute("""
    CREATE TABLE IF NOT EXISTS spark_streams.companies_created (
        id UUID PRIMARY KEY,
        name TEXT,
        email TEXT,
        vat TEXT,
        phone TEXT,
        country TEXT,
        website TEXT,
        image TEXT,
        addresses TEXT,  -- stocker comme une chaîne de caractères JSON
        contact TEXT,    -- stocker comme une chaîne de caractères JSON
        revenue DOUBLE,
        number_of_employees INT,
        sector TEXT,
        founded_date TEXT,
        valuation DOUBLE,
        investment_received DOUBLE);
        """)

    print("Table created successfully!")


def insert_data(session, **kwargs):
    print("inserting data...")

    company_id = kwargs.get('id')
    name = kwargs.get('name')
    email = kwargs.get('email')
    vat = kwargs.get('vat')
    phone = kwargs.get('phone')
    country = kwargs.get('country')
    website = kwargs.get('website')
    image = kwargs.get('image')
    addresses = json.dumps(kwargs.get('addresses'))
    # Convertir les informations de contact en chaîne de caractères JSON
    contact = json.dumps(kwargs.get('contact'))
    revenue = kwargs.get('revenue')
    picture = kwargs.get('picture')
    number_of_employees = kwargs.get('number_of_employees')
    sector = kwargs.get('sector')
    founded_date = kwargs.get('founded_date')
    valuation = kwargs.get('valuation')
    investment_received = kwargs.get('investment_received')

    try:
        session.execute("""
            INSERT INTO spark_streams.companies_created(id, name, email, vat, phone, country, website, 
                        image, addresses, contact, revenue, number_of_employees, sector, founded_date, valuation, investment_received)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (company_id, name, email, vat, phone, country,
              website, image, addresses, contact, revenue, number_of_employees, sector, founded_date, valuation,
              investment_received))
        logging.info(f"Data inserted for company {name}")
    except Exception as e:
        logging.error(f'Could not insert data due to {e}')


def create_spark_connection():
    try:
        s_conn = SparkSession.builder \
            .appName("CassandraConnectionTest") \
            .config("spark.cassandra.connection.host", "cassandra") \
            .config("spark.cassandra.connection.port", "9042") \
            .config("spark.cassandra.auth.username", "cassandra") \
            .config("spark.cassandra.auth.password", "cassandra") \
            .getOrCreate()

        s_conn.sparkContext.setLogLevel("ERROR")
        print("-------------------------------------------------------------------------------------")
        print("Spark connection created successfully!")
        return s_conn
    except Exception as e:
        logging.error(f"Couldn't create the spark session due to exception {e}")
        return None


def connect_to_kafka(spark_conn):
    print("passage")
    spark_df = None
    try:
        spark_df = spark_conn.readStream \
            .format('kafka') \
            .option('kafka.bootstrap.servers', 'broker:29092') \
            .option('subscribe', 'companies_created') \
            .option('startingOffsets', 'earliest') \
            .option("failOnDataLoss", "false") \
            .load()
        logging.info("kafka dataframe created successfully")
    except Exception as e:
        logging.warning(f"kafka dataframe could not be created because: {e}")

    return spark_df


def create_cassandra_connection():
    try:
        # connecting to the cassandra cluster
        cluster = Cluster(['cassandra'])

        cas_session = cluster.connect()

        return cas_session
    except Exception as e:
        logging.error(f"Could not create cassandra connection due to {e}")
        return None


def create_selection_df_from_kafka(spark_df):
    # Définition du schéma pour les données d'entreprise
    schema = StructType([
        StructField("id", StringType(), True),
        StructField("name", StringType(), True),
        StructField("email", StringType(), True),
        StructField("vat", StringType(), True),
        StructField("phone", StringType(), True),
        StructField("country", StringType(), True),
        StructField("website", StringType(), True),
        StructField("image", StringType(), True),
        StructField("addresses", ArrayType(StringType()), True),  # Une liste d'adresses
        StructField("contact", StringType(), True),  # Contact comme chaîne JSON
        StructField("revenue", DoubleType(), True),
        StructField("number_of_employees", IntegerType(), True),
        StructField("sector", StringType(), True),
        StructField("founded_date", StringType(), True),
        StructField("valuation", DoubleType(), True),
        StructField("investment_received", DoubleType(), True)
    ])

    # Sélection et transformation des données
    sel = spark_df.selectExpr("CAST(value AS STRING)") \
        .select(from_json(col('value'), schema).alias('data')).select("data.*")

    print(sel)

    return sel


if __name__ == "__main__":
    # create spark connection
    spark_conn = create_spark_connection()

    if spark_conn is not None:
        #     # connect to kafka with spark connection
        spark_df = connect_to_kafka(spark_conn)
        print(spark_df)
        selection_df = create_selection_df_from_kafka(spark_df)
        session = create_cassandra_connection()

        if session is not None:
            create_keyspace(session)
            create_table(session)

        logging.info("Streaming is being started...")

        streaming_query = (selection_df.writeStream.format("org.apache.spark.sql.cassandra")
                           .option('checkpointLocation', '/tmp/checkpoint')
                           .option('keyspace', 'spark_streams')
                           .option('table', 'companies_created')
                           .start())

        streaming_query.awaitTermination()
