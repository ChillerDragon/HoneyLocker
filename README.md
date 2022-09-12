# HoneyLocker
A simple python script that is a honeypot screen locker. It locks the screen and takes a picture on keypresses. I use this at work to not get caked.

## what is "caking" ?

Its a common security policy in IT companies that tries to reduce unlocked screens that are unattended. If you do not lock your screen and someone manages to write a message in slack on your behalf with text along the lines of "I BRING CAKE" you are forced to do so.

## setup

No additional pip packages are needed. It is using the library pyxhook but it is included in this repo.

It is only tested on gnome X11 tho. You need ``ffmpeg`` installed for the webcam image. Also make sure that the command ``xdg-screensaver lock`` does lock your screen.

```
sudo apt install python3 python3-pip ffmpeg
git clone --recursive https://github.com/ChillerDragon/HoneyLocker.git
cd HoneyLocker
./honeylocker.py
```

Then go to settings and set a shortcut that executes ``python /path/to/honeylocker.py`` or add a job that gets run on login/boot and passes the ``--block`` flag

## legal disclaimer

It may have bugs. You still may get caked. Use at own risk. I guarantee for nothing. Do not sue me thanks...
