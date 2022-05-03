#!/usr/bin/python3 -u

from datetime import datetime
from RFM69 import Radio, FREQ_433MHZ

import time, board, adafruit_bmp280, picamera, serial, time, string, pynmea2, csv, os, io

#############################
#### Initialize variables ###
#############################

# Change frequency on cansat AND ground station BEFORE launch
frequency = 434000000 

# Change this to match the location's pressure (hPa) at sea level
# https://meteo.vlaanderen/en/station/butgenbach-elsenborn
seaLevelPressure = 1036

# Altitude difference before taking the first picture (meters)
altitudeDiffBeforePictures = 0

# Time between pictures (seconds)
picturesSecondsInterval = 2

########################
#### Initialize data ###
########################
database = {"time": "", "temp":0, "pressure":0, "altitude":0, "latitude":0, "longitude":0}
myEncryptionKey = "cansxINDA"
rocketIsLaunched = False

##################
#### Functions ###
##################
def read_BMP(): # temperature, pressure, altitude
    print("Collecting BMP data...")
    database['temp']     = str(round(bmp280.temperature, 1))
    database['pressure'] = str(round(bmp280.pressure, 1))
    database['altitude'] = str(round(bmp280.altitude, 1))

def read_gps():
    print("Collecting GPS data...")
    found = False
    while found == False:
        try:
            newgpsdata=sio.readline()
        except UnicodeDecodeError as e:
            continue

        # Only lines starting with GPRMC contain GPS data
        if newgpsdata[0:6] == "$GPRMC":
            found = True 
            newmsg = pynmea2.parse(newgpsdata)
            database['latitude']  = str(round(newmsg.latitude, 6))  + newmsg.lat_dir
            database['longitude'] = str(round(newmsg.longitude, 6)) + newmsg.lon_dir

#
# Store data in /home/cansx/cansx/data/data.csv file using comma separated values format
# https://fr.wikipedia.org/wiki/Comma-separated_values#Exemple
# 
def store_data(csvwriter):
    print("Storing data...")
    csvwriter.writerow(database)

# Send data over radio
def send_data(recipient_id):
    message = ','.join(database.values())
    print ("Sending radio message " + message)
    radio.send(recipient_id, message)

# Take a picture and save it to /home/cansx/cansx/pictures/ folder
def take_picture(lastPictureTime):
    difference = currentTime - lastPictureTime
    secondsSinceLastPicture = difference.total_seconds()
    currentAltitude = round(bmp280.altitude,0)
    rocketIsLaunched = (currentAltitude - initialAltitude >= altitudeDiffBeforePictures)
    #print("current altitude=" + str(currentAltitude))
    #print("initial altitude=" + str(initialAltitude))
    #GPRMCprint("secondsSinceLastPicture=" + str(secondsSinceLastPicture))
    #print("rocketIsLaunched=" + str(rocketIsLaunched))
    if (rocketIsLaunched and (secondsSinceLastPicture > picturesSecondsInterval)):
        print("Taking picture...")
        timestamp = database["time"]
        camera.capture(f'/home/cansx/cansx/pictures/{timestamp}.jpg')
        return datetime.now()
    else:
        return lastPictureTime

########################    
# Start of the program #
########################

with Radio(FREQ_433MHZ, nodeID=1, networkID=100, isHighPower=True, verbose=True, interruptPin=24, resetPin=25, spiDevice=0, autoAcknowledge=False, use_board_pin_numbers=False, encryptionKey=myEncryptionKey) as radio, open('/home/cansx/cansx/data/data.csv', 'a', newline='', buffering=1) as csvfile, serial.Serial('/dev/ttyAMA0', 9600, timeout=0.5) as serial4gps:

    sio = io.TextIOWrapper(io.BufferedRWPair(serial4gps, serial4gps))

    # Initialize BMP sensor
    i2c = board.I2C()
    bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)
    bmp280.sea_level_pressure = seaLevelPressure

    # Save the initial altitude to trigger pictures only when the rocket has launched
    initialAltitude = round(bmp280.altitude,0)

    # Initialize camera
    camera = picamera.PiCamera()
    lastPictureTime = datetime.now()

    # Configure radio
    radio.calibrate_radio()
    radio.set_power_level(100)
    radio.set_frequency_in_Hz(frequency)
    recipient_id = 2

    # Configure csv writer
    fieldnames = ['time', 'temp', 'pressure', 'altitude', 'latitude', 'longitude']
    csvwriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
    csvwriter.writeheader()
    
    try:
        while True:
            currentTime = datetime.now()
            database['time'] = currentTime.strftime("%d%H%M%S")  
        
            read_BMP()
            read_gps()
            store_data(csvwriter)
            send_data(recipient_id)
            lastPictureTime = take_picture(lastPictureTime)
    finally:
        serial4gps.close()
