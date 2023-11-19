import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        client.subscribe("building/airpurifier")

def on_message(client, userdata, msg):
        print("Topic: " + msg.topic + ", Message: " + msg.payload.decode("utf-8"))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("localhost")

try:
        client.loop_forever()

except KeyboardInterrupt:
        print("Finished")
        client.unsubscribe("building/airpurifier")
        client.disconnect()
