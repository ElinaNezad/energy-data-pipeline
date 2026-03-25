import os
from azure.cosmos import CosmosClient, exceptions
from datetime import datetime, timezone

DATABASE_NAME = "energydb"
CONTAINER_NAME = "energydata"


def get_cosmos_container():
    endpoint = os.getenv("COSMOS_ENDPOINT")
    key = os.getenv("COSMOS_KEY")

    if not endpoint or not key:
        raise ValueError("COSMOS_ENDPOINT or COSMOS_KEY is missing.")

    client = CosmosClient(endpoint, key)
    database = client.get_database_client(DATABASE_NAME)
    container = database.get_container_client(CONTAINER_NAME)
    return container


def upsert_items_to_cosmos(items):
    try:
        container = get_cosmos_container()
        current_fetch_time = datetime.now(timezone.utc).isoformat()
        for item in items:
            record = {
                "id": f"{item['area']}_{item['timeStamp']}_{item['mtuStart']}",
                "timeStamp": item["timeStamp"],
                "mtuStart": item["mtuStart"],
                "area": item["area"],
                "value": item["value"],
                "fetchTime": current_fetch_time
            }
            container.upsert_item(record)

    except Exception as e:
        print(f"Error while saving data to Cosmos DB: {e}")
        raise


def read_all_items_from_cosmos():
    try:
        container = get_cosmos_container()
        query = "SELECT * FROM c"
        items = list(container.query_items(
            query=query,
            enable_cross_partition_query=True
        ))
        return items
    except Exception as e:
        print(f"Error while reading data from Cosmos DB: {e}")
        return []