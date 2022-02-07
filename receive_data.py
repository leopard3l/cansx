#!/usr/bin/python

import time
from RFM69 import Radio, FREQ_433MHZ

node_id = 2
network_id = 100
recipient_id = 1
number = 0

print ("Starting reception program")

with Radio(FREQ_433MHZ, node_id, network_id, isHighPower=True, verbose=False, interruptPin=18, resetPin=22, spiDevice=0, autoAcknowledge=False) as radio:
    print ("Starting receiving loop...")

    radio.calibrate_radio()
    radio.set_power_level(100)
    radio.set_frequency_in_kHz(434000000)

    while True:
        number += 1

        packet = radio.get_packet()

        # If radio.get_packet times out, it will return None
        if packet is not None:
            datas = packet.to_dict()
            print("Message %s, RSSI %s= %s" % (str(number), datas['rssi'], packet.data_string))
