#!/usr/bin/env python3
import os
import pyxhook
import time

password = ["p", "a", "s", "s", "w", "d"]
index = 0

# Use a function instead a variable to get the time of the pic shot
# and not of the program launch
def PicPath():
  return "~/Desktop/busted_" + time.strftime("_%I_%M_%S") + ".jpeg"

def Bust():
  # os.system("say 'Enemy input detected'")
  # os.system("streamer -f jpeg -o " + PicPath() + " 2> /dev/null")
  os.system("ffmpeg -f video4linux2 -i /dev/video0 -vframes 1 " + PicPath() + " 2> /dev/null")
  os.system("xdg-screensaver lock")
  exit();

def CheckPasswd(event):
  global index
  if len(password) == index:
    exit() # correc passwd
  if password[index] == event.Key:
    index += 1
    return True
  return False

def OnKeyPress(event):
  global pic_path 
  if CheckPasswd(event):
    return
  print("key pressed: " + event.Key)
  Bust()

def OnMouseClick(event):
  # rightclick blocks the screen lock
  # -> only lock on left click
  if (event.MessageName != "mouse left  down"):
    return
  Bust()
 
new_hook = pyxhook.HookManager()
new_hook.KeyDown = OnKeyPress
new_hook.MouseAllButtonsDown = OnMouseClick
new_hook.HookKeyboard()

try:
  new_hook.start()
except KeyboardInterrupt:
  # User cancelled from command line.
  pass
except Exception as ex:
  msg = 'Error while catching events:\n {}'.format(ex)
  pyxhook.print_err(msg)
