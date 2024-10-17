import json
import random

from flask import Flask, render_template, request, jsonify
from paho.mqtt import client as mqtt_client
import time

from status import convert_to_json, get_data_sort_by_date
from waitress import serve


app = Flask(__name__)

received_messages = []
client_instance = None 

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


def on_connect(client, userdata, flags, rc, properties):
    if rc == 0:
        print("Connected to MQTT Broker")
        client.subscribe(topic)
    else:
        print("Failed to connect, return code: ", rc)


def connect_to_mqtt():
    global client_instance

    client_instance = mqtt_client.Client(client_id=client_id, callback_api_version=mqtt_client.CallbackAPIVersion.VERSION2)
    client_instance.on_connect = on_connect
    client_instance.on_message = on_message
    client_instance.connect(broker, port)

    client_instance.loop_start()

    try:
        print("No exception")
    except KeyboardInterrupt:
        print("Disconnect from Broker")
        client_instance.loop_stop()
        client_instance.disconnect()


@app.route('/shipping/mqtt-subscribe')
def connect_with_mqtt():
    if client_instance is None:
        connect_to_mqtt()

    return render_template('index.html')


@app.route('/shipping/messages')
def get_messages():
    return jsonify(received_messages)


if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8000)
    app.run(debug=True)
