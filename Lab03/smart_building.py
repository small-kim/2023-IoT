import paho.mqtt.client as mqtt

total = 0

def on_connect(client, userdata, flags, rc):
	print("Connected with result code " + str(rc))
	client.subscribe("building/person")

def on_message(client, userdata, msg):
	global total
	print("Topic: " + msg.topic + ", Message: " + msg.payload.decode("utf-8"))

	entry = int(msg.payload.decode("utf-8"))

	if entry == 1:
		total += 1
	elif entry == 0:
		if total <= 0:
			total == 0
		elif total > 0:
			total -= 1

	print("Person inside", total)
	if total == 0:
		light = pubClient.publish("building/light", "off")
		airpurifier = pubClient.publish("building/airpurifier", "off")

	elif total == 1:
		light = pubClient.publish("building/light", "on")
		airpurifier = pubClient.publish("building/airpurifier", "off")

	elif total >= 2:
		light = pubClient.publish("building/light", "on")
		airpurifier = pubClient.publish("building/airpurifier", "on")

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
	subClient.unsubscribe("building/person")
	subClient.disconnect()
	pubClient.disconnect()
