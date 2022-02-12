#!/usr/bin/python

#from picamera import PiCamera
from RFM69 import Radio, FREQ_433MHZ
from time import sleep

import time
import board
import adafruit_bmp280

n = 0
node_id = 1
network_id = 100
recipient_id = 2
number = 0

def BMP():
	# Create sensor object, communicating over the board's default I2C bus
	i2c = board.I2C()   # uses board.SCL and board.SDA
	bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)

	# change this to match the location's pressure (hPa) at sea level
	bmp280.sea_level_pressure = 1036

	while True:
		print("\nTemperature: %0.1f C" % bmp280.temperature)
		print("Pressure: %0.1f hPa" % bmp280.pressure)
		print("Altitude = %0.2f meters" % bmp280.altitude)
		time.sleep(2)

#def Picture():
#	camera = PiCamera()
#	n = n + 1
#	camera.capture(f'/home/pi/cansx/picture{n}.jpg')
		
	
print ("Starting transmission program")

with Radio(FREQ_433MHZ, node_id, network_id, isHighPower=True, verbose=True, interruptPin=24, resetPin=25, spiDevice=0, autoAcknowledge=False, use_board_pin_numbers=False) as radio:
    print ("Starting sending loop...")

    radio.calibrate_radio()
    radio.set_power_level(100)
    #radio.set_frequency_in_kHz(434000000)

    BMP()

    while True:
        number += 1

        print ("Sending " + str(number) + " @ " + time.strftime("%H:%M:%S"))
        radio.send(recipient_id, "TEST " + str(number))
