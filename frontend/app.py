import os
import requests
from flask import Flask, render_template, request
from azure.servicebus import ServiceBusClient, ServiceBusMessage
# from jinja2 import Template

app = Flask(__name__)


BACKEND_API_URL = "http://localhost:5001/table" # Replace with your backend API URL
CONNECTION_STR = os.environ["SERVICE_BUS_CONNECTION_STR"]
QUEUE_NAME = os.environ["SERVICE_BUS_QUEUE_NAME"]

def send_to_service_bus_queue(name, email):
    servicebus_client = ServiceBusClient.from_connection_string(CONNECTION_STR)
    with servicebus_client:
        sender = servicebus_client.get_queue_sender(queue_name=QUEUE_NAME)
        message = ServiceBusMessage(f"{name}, {email}")
        sender.send_messages(message)

def get_table():
    response = requests.get(BACKEND_API_URL)
    table = response.text
    return table


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name')
    email = request.form.get('email')
    send_to_service_bus_queue(name, email)
    result = f'Thank you for submitting your information, {name} ({email})!'
    return result

# table = {
#   "students": [
#     {
#       "name": "John Smith",
#       "email": "john.smith@example.com"
#     },
#     {
#       "name": "Jane Doe",
#       "email": "jane.doe@example.com"
#     },
#     {
#       "name": "Bob Johnson",
#       "email": "bob.johnson@example.com"
#     }
#   ]
# }

table = {"0":"Chenyang, chris.liu@theta.co.nz","1":"Chris Liu, chenyangliutele@gmail.com","2":"Chenyang Liu, chris.liu@theta.co.nz","3":"someone, 511878188@qq.com","4":"C Liu, chris.liu@theta.co.nz","5":"CCCCC, chris.liu@theta.co.nz","6":"Chris Liu, chenyangliutele@gmail.com","7":"Chris Liu, chenyangliutele@gmail.com","8":"Chenyang, chenyangliutele@gmail.com"}

@app.route('/table')
def table():
    # table = get_table()
    return render_template('table.html', students=table)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
