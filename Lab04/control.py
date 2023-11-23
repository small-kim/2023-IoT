import paho.mqtt.client as mqtt


def on_connect(client, userdata, flags, rc):
	print("Connected with result code " + str(rc))
	client.subscribe("sensor/distance")

def on_message(client, userdata, msg):
	print("Topic: " + msg.topic + ", Distance: " + msg.payload.decode("utf-8"))
	distance = int( msg.payload.decode("utf-8"))
	if distance == 10000:
		led_color = "Off"
	elif distance >= 40:
		led_color = "green"
	elif distance < 40 and distance >= 20:
		led_color = "yellow"
	else:
		led_color = "red"
	infot = pubClient.publish("control/led", led_color)

subClient = mqtt.Client()
subClient.on_connect = on_connect
subClient.on_message = on_message
subClient.connect("localhost")

pubClient = mqtt.Client()
pubClient.connect("localhost")
pubClient.loop_start()

try:
	subClient.loop_forever()

except KeyboardInterrupt:
	print("Finished!")
	subClient.unsubscribe("control/led")
	subClient.disconnect()
	pubClient.disconnect()
