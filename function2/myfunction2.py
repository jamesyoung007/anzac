import os
import json
from azure.cosmos import CosmosClient
import pandas as pd
from prettytable import PrettyTable

# Initialize Cosmos DB client
url = "https://chdbstudentdemo.documents.azure.com:443/"
key = "DtdKcjFjnFccc5ul9BAqQr4ZaZoxAcZQXm3bkPzltbC6O39uLKtrbXT4ajDpAwDtNWLfN3GCeduoACDb5WEDEg=="
client = CosmosClient(url, credential=key)

query = "SELECT * FROM c"
# Select database and container
database_name = "students"
container_name = "students1"
database = client.get_database_client(database_name)
container = database.get_container_client(container_name)

items = list(container.query_items(query=query, enable_cross_partition_query=True))

df = pd.DataFrame.from_records(items)

# Convert the body field to a dictionary with name and email keys

response = df.loc[:, 'body'].to_json()

def returnresponse():
    return response

returnresponse()

print(returnresponse())








