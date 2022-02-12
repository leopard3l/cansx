# Set WIFI using "sudo raspi-config" command then run the script below in a terminal

sudo apt-get update
sudo apt-get upgrade -y

sudo timedatectl set-timezone Europe/Luxembourg

sudo raspi-config nonint do_camera 1
sudo raspi-config nonint do_ssh 1
sudo raspi-config nonint do_vnc 1
sudo raspi-config nonint do_spi 1
sudo raspi-config nonint do_i2c 1

sudo apt install samba
sudo apt install python3 idle3
sudo update-alternatives --install /usr/bin/python python /usr/bin/python2.7 1
sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.7 2

python -m pip install -U pip

pip install rpi-rfm69
