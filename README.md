# HoneyLocker
A simple python script that is a honeypot screen locker. It locks the screen and takes a picture on keypresses.

## setup

```
sudo apt install python3 python3-pip ffmpeg
pip3 install pyxhook
cd /usr/local/bin
sudo wget https://raw.githubusercontent.com/ChillerDragon/HoneyLocker/master/honeylocker.py
sudo chmod +x honeylocker.py
```

Then go to settings and set a shortcut that executes ``python /usr/local/bin/honeylocker.py`` or open a terminal and type ``honeylocker.py``.
