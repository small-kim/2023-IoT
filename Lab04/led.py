import RPi.GPIO as gpio
import paho.mqtt.client as mqtt

gpio.setmode(gpio.BCM)
led = [23, 24, 25]
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
	if led_color == "Off":
		gpio.output(led, False)
	elif led_color == "green":
		gpio.output(led, False)
		gpio.output(25, True)
	elif led_color == "yellow":
		gpio.output(led, False)
		gpio.output(24, True)
	elif led_color == "red":
		gpio.output(led, False)
		gpio.output(23, True)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("localhost")

try:
	client.loop_forever()

except KeyboardInterrupt:
	print("Finished")
	client.unsubscribe("control/led")
	client.disconnect()
	gpio.cleanup()
