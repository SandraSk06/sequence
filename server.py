import json
import random

from flask import Flask, render_template, request, jsonify
from paho.mqtt import client as mqtt_client
import time

from status import convert_to_json, get_data_sort_by_date
from waitress import serve


app = Flask(__name__)

received_messages = []

# MQTT connection details
broker = 'broker.emqx.io'
port = 1883
topic = "test"
client_id = f'python-mqtt-{random.randint(0, 1000)}'


def on_message(client, userdata, msg):
    try:
        message = json.loads(msg.payload.decode())
        print(f"Received `{message}` from `{msg.topic}` topic")
        received_messages.append(message)
    except json.JSONDecodeError:
        print("Failed to decode JSON ", msg.payload.decode())


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker")
        client.subscribe(topic)
    else:
        print("Failed to connect, return code: ", rc)


@app.route('/shipping/mqtt-subscribe')
def connect_with_mqtt():
    client = mqtt_client.Client(client_id=client_id, callback_api_version=mqtt_client.CallbackAPIVersion.VERSION2)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(broker, port)

    client.loop_start()

    try:
        print("No exception")
    except KeyboardInterrupt:
        print("Disconnect from Broker")
        client.loop_stop()
        client.disconnect()

    # mqtt_thread = threading.Thread(target=client.loop_forever)
    # mqtt_thread.start()
    #
    # # Subscribe
    # subscribe(client, topic)

    return render_template('index.html')


@app.route('/shipping/messages')
def get_messages():
    # publish()
    return jsonify(received_messages)














def connect_mqtt() -> mqtt_client:
    client = mqtt_client.Client(client_id=client_id, callback_api_version=mqtt_client.CallbackAPIVersion.VERSION2)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(broker, port)

    client.loop_start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("Disconnect from Broker")
        client.loop_stop()
        client.disconnect()



    # For paho-mqtt 2.0.0, you need to add the properties parameter.
    # def on_connect(client, userdata, flags, rc, properties):
    #     if rc == 0:
    #         print("Connected to MQTT Broker!")
    #     else:
    #         print("Failed to connect, return code %d\n", rc)
    #
    # # Set Connecting Client ID
    # # client = mqtt_client.Client(client_id)
    #
    # # For paho-mqtt 2.0.0, you need to set callback_api_version.
    # client = mqtt_client.Client(client_id=client_id, callback_api_version=mqtt_client.CallbackAPIVersion.VERSION2)
    #
    # client.on_connect = on_connect
    # client.connect(broker, port)
    #
    # return client


# def subscribe(client: mqtt_client, topic):
#     def on_message(client, userdata, msg):
#         try:
#             message = json.loads(msg.payload.decode())
#             print(f"Received `{message}` from `{msg.topic}` topic")
#             received_messages.append(message)
#         except json.JSONDecodeError:
#             print("Failed to decode JSON")
#
#
#     client.subscribe(topic)
#     client.on_message = on_message
#     client.loop_start()

def publish():
    broker = 'broker.emqx.io'
    port = 1883
    topic = "test"
    client_id = f'python-mqtt-{random.randint(0, 1000)}'

    client = mqtt_client.Client(client_id=client_id, callback_api_version=mqtt_client.CallbackAPIVersion.VERSION2)
    client.connect(broker, port)
    client.loop_start()

    while True:
        message = {'id': 1, 'msg': 'Hello from Python!!'}
        client.publish(topic, json.dumps(message))
        print(f'Published: {message}')
        time.sleep(5)

def load_shipping_data():
    csv_file_path = r'ShippingLogs.csv'
    json_file_path = r'ShippingJson.json'
    convert_to_json(csv_file_path, json_file_path)

    return render_template('index.html')


@app.route('/shipping/get-data-by-date', methods=['POST'])
def get_shipping_data_by_date():
    # Get parameters from the request body (JSON)
    data = request.get_json()
    start_date = data.get('start_date')
    end_date = data.get('end_date')

    filtered_data = get_data_sort_by_date(start_date, end_date)
    return jsonify(filtered_data)


if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8000)
    app.run(debug=True)



