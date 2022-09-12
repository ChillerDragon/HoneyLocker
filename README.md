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

## usage

```
./honeylocker.py --block cake
```

Locks the screen if someone types "cake" into slack. This is recommended to run in the background at all times. Using some sort of auto start like bashrc, cronjobs or systemd.

```
./honeylocker.py "my password"
```

Locks the screen if anything other than "my password" is typed. This is basically a trap. The screen looks unlocked but the device can not be used unless you know the password. After "my password" is typed the program will terminate and thus allow free usage of the device. This is recommended to be bound to a keyboard combination and replace your classic lock procedure.

When a attacker is detected it will lock the screen and also take one image from your webcam to identify the intruder. The image will be saved on your ~/Desktop and the filename will be ``busted__hh_mm_ss.jpeg`` so you can see who and when tried to access your device. Make sure to delete or archive those daily otherwise they could (very unlikley) be overwritten the next day.

## legal disclaimer

It may have bugs. You still may get caked. Or worse your system might be compromised by malicious actors. Use at own risk. I guarantee for nothing. Do not sue me thanks...
