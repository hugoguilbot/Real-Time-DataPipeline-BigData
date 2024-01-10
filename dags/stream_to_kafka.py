import requests
import json
import time
import uuid
from kafka import KafkaProducer
import random
import logging

# default_args = {
#     'owner': 'airscholar',
#     'start_date': datetime(2023, 9, 3, 10, 00)
# }

def get_company_data():

    res = requests.get("https://fakerapi.it/api/v1/companies?_quantity=1")
    res = res.json()

    return res['data'][0]


def create_final_json(res):
    if not res:
        return None

    # Création du dictionnaire de formatage
    formatted_data = {}
    
    formatted_data['id'] = str(uuid.uuid4())  # Générer un UUID unique
    # Assurez-vous que ces champs existent dans 'res' avant de les décommenter
    formatted_data['name'] = res.get('name')
    formatted_data['email'] = res.get('email')
    formatted_data['vat'] = res.get('vat')
    formatted_data['phone'] = res.get('phone')
    formatted_data['country'] = res.get('country')
    formatted_data['website'] = res.get('website')
    formatted_data['image'] = res.get('image')
    formatted_data['addresses'] = res.get('addresses', [])  # Liste des adresses

    # Extraction des informations de contact
    contact = res.get('contact', {})
    formatted_data['contact'] = {
        'firstname': contact.get('firstname'),
        'lastname': contact.get('lastname'),
        'email': contact.get('email'),
        'phone': contact.get('phone'),
        'birthday': contact.get('birthday'),
        'gender': contact.get('gender'),
        'contact_address': contact.get('address')
    }

    # Données ajoutées
    formatted_data['revenue'] = random.uniform(10000, 1000000)  # Chiffre d'affaires simulé
    formatted_data['number_of_employees'] = random.randint(10, 5000)  # Nombre d'employés
    formatted_data['sector'] = random.choice(['Technology', 'Healthcare', 'Finance', 'Retail', 'Agriculture'])  # Secteur d'activité
    formatted_data['founded_date'] = f"19{random.randint(70, 99)}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}"  # Date de fondation simulée
    formatted_data['valuation'] = random.uniform(1000000, 10000000)  # Évaluation de l'entreprise
    formatted_data['investment_received'] = random.uniform(100000, 5000000)  # Investissements reçus

    return formatted_data

def create_kafka_producer():
    """
    Creates the Kafka producer object
    """

    return KafkaProducer(bootstrap_servers=['broker:29092'])


def start_streaming():
    """
    Writes the API data every 10 seconds to Kafka topic companies_created
    """
    producer = create_kafka_producer()
    #end_time = time.time() + 60  # the script will run for 5 minutes
    while True:
        companies = get_company_data()
        if companies:
            kafka_data = create_final_json(companies)
            producer.send("companies_created", json.dumps(kafka_data).encode('utf-8'))
            logging.info("Data sent to Kafka")
        time.sleep(10)


if __name__ == "__main__":
    start_streaming()