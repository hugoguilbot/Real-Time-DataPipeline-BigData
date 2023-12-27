import requests
import json
import time
import uuid
from kafka import KafkaProducer
import logging

# default_args = {
#     'owner': 'airscholar',
#     'start_date': datetime(2023, 9, 3, 10, 00)
# }

def get_company_data():

    res = requests.get("https://fakerapi.it/api/v1/companies?_quantity=1")
    res = res.json()

    return res['data'][0]


def format_data(res):
    # Vérifier si la réponse contient des données
    if not res or 'data' not in res or not res['data']:
        return None

    # Extraire la première entrée des données (supposant qu'il y a toujours au moins une entrée)
    company_data = get_company_data()

    # Création du dictionnaire de formatage
    formatted_data = {
        'id': str(uuid.uuid4()),  # Générer un UUID unique
        'original_id': company_data.get('id'),  # ID original de la réponse
        'name': company_data.get('name'),
        'email': company_data.get('email'),
        'vat': company_data.get('vat'),
        'phone': company_data.get('phone'),
        'country': company_data.get('country'),
        'website': company_data.get('website'),
        'image': company_data.get('image'),
        'addresses': company_data.get('addresses', []),  # Liste des adresses
        'contact': {
            'firstname': company_data['contact']['firstname'],
            'lastname': company_data['contact']['lastname'],
            'email': company_data['contact']['email'],
            'phone': company_data['contact']['phone'],
            'birthday': company_data['contact']['birthday'],
            'gender': company_data['contact']['gender'],
            'contact_address': company_data['contact']['address']
        }
    }

    return formatted_data


def stream_data():

    producer = KafkaProducer(bootstrap_servers=['broker:29092'], max_block_ms=5000)
    curr_time = time.time()

    while True:
        if time.time() > curr_time + 60: #1 minute
            break
        try:
            res = get_company_data()
            res = format_data(res)

            producer.send('users_created', json.dumps(res).encode('utf-8'))
        except Exception as e:
            logging.error(f'An error occured: {e}')
            continue

# with DAG('user_automation',
#          default_args=default_args,
#          schedule_interval='@daily',
#          catchup=False) as dag:

#     streaming_task = PythonOperator(
#         task_id='stream_data_from_api',
#         python_callable=stream_data
#     )