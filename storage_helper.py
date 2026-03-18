import os
import json
import logging
from azure.storage.blob import BlobServiceClient

CONTAINER_NAME = "energy-data"
BLOB_NAME = "latest_data.json"


def get_connection_string():
    connection_string = os.getenv("AzureWebJobsStorage")
    if connection_string:
        return connection_string
    
    with open("local.settings.json", "r") as file: 
        settings = json.load(file)

    return settings["Values"]["AzureWebJobsStorage"]  
 


def upload_data_to_blob(data):
    try:
        connection_string = get_connection_string()
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        container_client = blob_service_client.get_container_client(CONTAINER_NAME)

        try:
            container_client.create_container()
        except Exception:
            pass

        blob_client = container_client.get_blob_client(BLOB_NAME)
        json_data = json.dumps(data, indent=2)
        blob_client.upload_blob(json_data, overwrite=True)

    except Exception as e:
        print(f"Error while uploading data to blob: {e}")
        raise


def download_data_from_blob():
    
    # connection_string = os.getenv("AzureWebJobsStorage")
    try:
        connection_string = get_connection_string()

        blob_service_client = BlobServiceClient.from_connection_string(connection_string)

        blob_client = blob_service_client.get_blob_client(container=CONTAINER_NAME, blob=BLOB_NAME)

        blob_data = blob_client.download_blob().readall()

        return json.loads(blob_data)
    except Exception as e:
         logging.error("error while downloading data from blob:{e}") 
         return []   

def get_blob_last_modified(): 

    # connection_string = os.getenv("AzureWebJobsStorage") 
    try:

        connection_string = get_connection_string()

        blob_service_client = BlobServiceClient.from_connection_string(connection_string) 

        blob_client = blob_service_client.get_blob_client( container=CONTAINER_NAME, blob=BLOB_NAME ) 

        properties = blob_client.get_blob_properties() 

        return properties.last_modified
    except Exception as e:
        logging.warning("error while getting last update:{e}")
        return None