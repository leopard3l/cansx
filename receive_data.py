#!/usr/bin/python

import time
import RPi.GPIO as GPIO  
from RFM69 import Radio, FREQ_433MHZ

frequency = 434000000 
myEncryptionKey = "cansxINDA"
number = 0

print ("Starting reception program")

try:
    with Radio(FREQ_433MHZ, nodeID=2, networkID=100, isHighPower=True, verbose=False, interruptPin=18, resetPin=22, spiDevice=0, autoAcknowledge=False, encryptionKey=myEncryptionKey) as radio, open('database.csv', 'a+') as output:
        print ("Starting receiving data...")
    
        radio.calibrate_radio()
        radio.set_power_level(100)
        radio.set_frequency_in_Hz(frequency)
    
        while True:
            number += 1
    
            packet = radio.get_packet(timeout=1)
    
            if packet is not None:
                datas = packet.to_dict()
                print("Message %s, RSSI %s= %s" % (str(number), datas['rssi'], packet.data_string))
                print("%s,%s,%s" % (str(number), datas['rssi'], packet.data_string), file=output)
finally:
    GPIO.cleanup()
