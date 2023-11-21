import RPi.GPIO as gpio
import paho.mqtt.client as mqtt

gpio.setmode(gpio.BCM)
led = [5, 6, 7]
for i in led:
	gpio.setup(i, gpio.OUT)

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
	if led_color == "Off":
		for i in led:
			gpio.output(i, False)
	elif led_color == "green":
		for i in led:
			gpio.output(i, False)
		gpio.output(5, True)
	elif led_color == "yellow":
		for i in led:
			gpio.output(i, False)
		gpio.output(6, True)
	elif led_color == "red":
		for i in led:
			gpio.output(i, False)
		gpio.output(7, True)

	client.loop_forever()

except KeyboardInterrupt:
	print("Finished")
	client.unsubscribe("control/led")
	client.disconnect()
	gpio.cleanup()
