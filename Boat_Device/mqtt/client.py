import paho.mqtt.client as mqtt
import uuid, re, json

from mqtt.functions import *


class Client:
    def __init__(self):
        self.name: str = ':'.join(re.findall('..', '%012x' % uuid.getnode()))  # computer's mac address
        self.instance: mqtt.Client = mqtt.Client(self.name)
        self.currentJourney: int = 0

    def _config(self):
        self.instance.on_connect = on_connect
        self.instance.on_message = on_message
        self.instance.on_disconnect = on_disconnect

    def connect(self, host: str):
        self.instance.connect(host)
        self.instance.loop_start()

        self.instance.subscribe(f"DEVICE/{self.name}/START")
        self.instance.subscribe(f"DEVICE/{self.name}/END")
        self.instance.subscribe(f"DEVICE/{self.name}/CLEAR")

        self._config()

    def publish(self, topic: str, payload: str):
        self.instance.publish(f"DEVICE/{self.name}/{topic}", payload)


def on_message(client, userdata, message):
    raw_data = str(message.payload.decode("utf-8"))
    #print("received message: ", raw_data)

    data = json.loads(raw_data)

    processMessage(data)


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))


def on_disconnect():
    print("Disconnected from MQTT BROKER")
