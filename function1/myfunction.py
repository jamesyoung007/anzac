import os
from azure.servicebus import ServiceBusClient, ServiceBusMessage
from azure.cosmos.cosmos_client import CosmosClient

SERVICE_BUS_CONNECTION_STR ="Endpoint=sb://studentattend.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=Yoa1WTBpGLx4tQWqHSdU7ALErw5Vc+GUz+ASbK75TLE="
SERVICE_BUS_QUEUE_NAME="students"
COSMOS_CONNECTION_STR="AccountEndpoint=https://chdbstudentdemo.documents.azure.com:443/;AccountKey=DtdKcjFjnFccc5ul9BAqQr4ZaZoxAcZQXm3bkPzltbC6O39uLKtrbXT4ajDpAwDtNWLfN3GCeduoACDb5WEDEg==;"
COSMOS_DB_NAME="students"
COSMOS_CONTAINER_NAME="students1"


# SERVICE_BUS_CONNECTION_STR = os.environ['SERVICE_BUS_CONNECTION_STR']
# SERVICE_BUS_QUEUE_NAME = os.environ['SERVICE_BUS_QUEUE_NAME']
# COSMOS_CONNECTION_STR = os.environ['COSMOS_CONNECTION_STR']
# COSMOS_DB_NAME = os.environ['COSMOS_DB_NAME']
# COSMOS_CONTAINER_NAME = os.environ['COSMOS_CONTAINER_NAME']

def receive_message_from_service_bus_and_save_to_cosmos_db():
    servicebus_client = ServiceBusClient.from_connection_string(SERVICE_BUS_CONNECTION_STR)
    #print("servicebus_client: ", servicebus_client)
    with servicebus_client:
        receiver = servicebus_client.get_queue_receiver(queue_name=SERVICE_BUS_QUEUE_NAME)
        #print("receiver: ", receiver)
        with receiver:
            received_msgs = receiver.receive_messages(max_message_count=10, max_wait_time=5)
            for msg in received_msgs:
                #print("msg: ", format(msg))
                #Create a Cosmos DB client and save the message to Cosmos DB
                cosmos_client = CosmosClient.from_connection_string(COSMOS_CONNECTION_STR)
                #print("cosmos_client: ", cosmos_client)
                db = cosmos_client.get_database_client(database=COSMOS_DB_NAME)
                #print("db: ", db)
                container = db.get_container_client(container=COSMOS_CONTAINER_NAME)
                #print("container: ", container)
                item = {"id": msg.message_id, "body": str(msg)}
                #print("item: ", item)
                container.create_item(body=item)
                # print("item created", item)
                # Delete the message from the Service Bus queue
                receiver.complete_message(msg)

receive_message_from_service_bus_and_save_to_cosmos_db()