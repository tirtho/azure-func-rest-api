from io import BytesIO
import logging
from urllib import response

import azure.functions as func
import json
import requests
import os

def main(myblob: func.InputStream):
    logging.info(f"Python blob trigger function processed blob \n"
                 f"Name: {myblob.name}\n"
                 f"Blob Size: {myblob.length} bytes")

    #blobBytes = myblob.read()
    #blobToRead = BytesIO(blobBytes)
    #outFile = open("someFile", "r+b")
    #outFile.write(blobBytes)

    url = os.environ['REST_API_SERVICE_URL']
    #headers = {'Host': 'tr-azure-func-rest-api.azurewebsites.net'}
    #fileMetadata = {'key1': 'value1', 'key2': 'value2'}
    #data = {'name': 'someFile.csv', 'data': json.dumps(fileMetadata)}
    files = {'file': myblob}
    response = requests.post(url, files=files) #, data=data)
    
    logging.info(f"REST Api POST response: %s" %response.text)




