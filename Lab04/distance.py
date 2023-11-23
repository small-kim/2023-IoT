import RPi.GPIO as gpio
import paho.mqtt.client as mqtt
import time

motion = 12
trig =  20
echo = 21

gpio.setwarnings(False)
gpio.setmode(gpio.BCM)

gpio.setup(motion, gpio.IN)
gpio.setup(trig, gpio.OUT)
gpio.setup(echo, gpio.IN)

mqttc = mqtt.Client()
mqttc.connect("localhost")

mqttc.loop_start()

try:
	while True:
		if gpio.input(motion):
			gpio.output(trig, False)
			time.sleep(1)

			gpio.output(trig, True)
			time.sleep(0.000001)
			gpio.output(trig, False)

			while gpio.input(echo) == 0:
				pulse_start = time.time()
			while gpio.input(echo) == 1:
				pulse_end = time.time()

			pulse_duration = pulse_end - pulse_start
			distance = pulse_duration * 34000 / 2
			distance = round(distance, 2)
		else:
			distance = 10000

		print(distance)
		infot = mqttc.publish("sensor/distance", distance)
		infot.wait_for_publish()

		time.sleep(2)

except KeyboardInterrupt:
	print("Finished!")
	mqttc.loop_stop()
	mqttc.disconnect()
	gpio.cleanup()
