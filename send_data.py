#!/usr/bin/python

import time

from RFM69 import Radio, FREQ_433MHZ

node_id = 1
network_id = 100
recipient_id = 2
number = 0

print ("Starting transmission program")

# The following are for an Adafruit RFM69HCW Transceiver Radio
# Bonnet https://www.adafruit.com/product/4072
# You should adjust them to whatever matches your radio
with Radio(FREQ_433MHZ, node_id, network_id, isHighPower=True, verbose=False, interruptPin=18, resetPin=22, spiDevice=0, autoAcknowledge=False) as radio:
    print ("Starting sending loop...")

    radio.calibrate_radio()
    radio.set_power_level(100)
    #radio.set_frequency_in_kHz(434000000)

    while True:
        number += 1

        print ("Sending " + str(number) + " @ " + time.strftime("%H:%M:%S"))
        radio.send(recipient_id, "TEST " + str(number))
