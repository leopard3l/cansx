Cansat project from the great team cansx from school INDA 2022

# Cansat

ssh cansx@cansx.local

Username = cansax
Password = cansax22

Configurer le WIFI

```
sudo nano /etc/wpa_supplicant/wpa_supplicant.conf
```

Plus d'infos sur la config WiFi [ICI](https://raspberrypihq.com/how-to-connect-your-raspberry-pi-to-wifi)

Le programme se lance automatiquement au démarrage du Raspberry

Editer le programme:
```
nano /home/cansx/cansx/cansx.py
```

Les photos sont dans 
/home/cansx/cansx/pictures

Les données sont dans 
/home/cansx/cansx/data/data.csv

Format des données:
time,temp,pressure,altitude,latitude,longitude

Voir les logs défiler:
```
sudo journalctl -u cansx -f
```

Gestion du service cansx:
```
sudo systemctl status cansx.service
sudo systemctl stop cansx.service
sudo systemctl start cansx.service
```

# Ground station

ssh grounds@grounds.local

Username = grounds
Password = grounds

Lancer le programme:
```
cd cansx
python3 -u receive_data.py
```

Les données sont dans
/home/grounds/cansx/database.csv

Format des données:
numéro,RSSI,time,temp,pressure,altitude,latitude,longitude
