import logging
from turtle import down

import azure.functions as func
import os, uuid, sys
from azure.storage.filedatalake import DataLakeServiceClient
from azure.core._match_conditions import MatchConditions
from azure.storage.filedatalake._models import ContentSettings
from urllib import response
import requests
import json


def initialize_storage_account(storage_account_name, storage_account_key):
    
    try:  
        service_client = DataLakeServiceClient(account_url="{}://{}.dfs.core.windows.net".format(
            "https", storage_account_name), credential=storage_account_key)
        return service_client
    except Exception as e:
        print(e)

def download_file_from_directory(service_client, container_name, directory_name, file_name):
    try:
        file_system_client = service_client.get_file_system_client(file_system=container_name)

        directory_client = file_system_client.get_directory_client(directory_name)
        
        file_client = directory_client.get_file_client(file_name)

        download = file_client.download_file()

        download_bytes = download.readall()

        return download_bytes

    except Exception as e:
     print(e)

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        storage_account_name = 'tr0adls4rest0services'
        storage_account_key = 'GU+6EZ4U2xeEQi73UCNkoklfFyXn/Uew2kJn9pLfa9cl15DPtTqfa1fMFOPyY7R/NNck7z5or12cgGW3HB7HbA=='
        cont_name = 'input-container'
        dir_name = '/'
        file_name = name #'1bike-share.csv'
        service_client = initialize_storage_account(storage_account_name, storage_account_key)
        fileToPass = download_file_from_directory(service_client, cont_name, dir_name, file_name)
        url = 'https://tr-azure-func-rest-api.azurewebsites.net/api/restAPI' #os.environ['REST_API_SERVICE_URL']
        files = {'file': fileToPass}
        response = requests.post(url, files=files) #, data=data)
        logging.info(f"REST Api POST response: %s" %response.text)

        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )


