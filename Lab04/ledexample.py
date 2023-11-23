import paho.mqtt.client as mqtt

led_color = "0"

def on_connect(client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        client.subscribe("control/led")

def on_message(client, userdata, msg):
	global led_color
	print("Topic: " + msg.topic + ", Led Color: " + msg.payload.decode("utf-8"))
	led_color = msg.payload.decode("utf-8")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("localhost")

try:
	print(led_color)
	client.loop_forever()

except KeyboardInterrupt:
	print("Finished")
	client.unsubscribe("control/led")
	client.disconnect()
