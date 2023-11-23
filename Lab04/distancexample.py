import paho.mqtt.client as mqtt
import random
import time

mqttc = mqtt.Client()
mqttc.connect("localhost")

mqttc.loop_start()

try:
	while True:
		distance = random.randint(2, 100001)
		print(distance)

		infot = mqttc.publish("sensor/distance", distance)
		infot.wait_for_publish()

		time.sleep(2)

except KeyboardInterrupt:
	print("Finished!")
	mqttc.loop_stop()
	mqttc.disconnect()
