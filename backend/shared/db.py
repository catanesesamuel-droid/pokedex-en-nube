import os
from azure.cosmos import CosmosClient, PartitionKey

def get_container(container_name: str):
    client = CosmosClient(
        url=os.environ["COSMOS_ENDPOINT"],
        credential=os.environ["COSMOS_KEY"]
    )
    database = client.get_database_client(os.environ["COSMOS_DATABASE"])
    return database.get_container_client(container_name)