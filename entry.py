import paho.mqtt.client as mqtt
import random
import time

person_entry = 1
total = 0

mqttc = mqtt.Client()

def on_connect(client, userdata, flags, rc):
	print("Connected with result code " + str(rc))


mqttc.connect("localhost")

mqttc.loop_start()

try:
	while True:
		entry = random.choice([0,1])

		print("Entry :  ", entry)

		infot = mqttc.publish("building/person", entry)
		infot.wait_for_publish()

		time.sleep(2)

except KeyboardInterrupt:
	print("Finished!")
	mqttc.loop_stop()
	mqttc.disconnect()
