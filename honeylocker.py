#!/usr/bin/env python3
import os
import lib.pyxhook.pyxhook
import time
import json
import sys

password = None
blocked = ["cake", "c a k e", "kuchen", "bring", ":cak", ":cup"]
index = 0

def show_help():
    print('usage: honeylocker.py [OPTION] [PASSWORD]')
    print('options:')
    print('  --block|-b     use blacklist mode instead of whitelist')

for arg in sys.argv:
    if arg == '--help' or arg == 'help' or arg == '-h':
        show_help()
        exit()
    elif arg == '--block' or arg == '-b':
        mode = 'blacklist'
        password = None
    elif arg.startswith('-'):
        print(f"Error: invalid arguemnt '{arg}'")
        exit()
    else:
        password = arg

mode = 'blacklist'
if password:
    mode = 'password'

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

history = []

def CheckPasswd(event):
  global index
  global history
  global blocked
  global password
  global mode
  if event.WindowProcName != 'slack':
      return True
  if not event.Key.lower().startswith('shift'):
      history.append(event.Key.lower())
  print(f"index: {index} history: {history}")
  if mode == 'password':
    if len(password) == index:
      exit() # correc passwd
    if password[index] == event.Key:
      index += 1
      return True
    return True
  else:
    for block in blocked:
        if block in ''.join(history):
            print(f"found blocked word {block}")
            return False
        else:
            print(f"{block} not found in {''.join(history)}")
    # no blocked
    return True
  return False

def OnKeyPress(event):
  global pic_path 
  if CheckPasswd(event):
    return
  print("key pressed: " + event.Key)
  Bust()

def OnMouseClick(event):
  global mode
  if mode == 'blacklist':
      return
  # rightclick blocks the screen lock
  # -> only lock on left click
  if (event.MessageName != "mouse left  down"):
    return
  Bust()
 
new_hook = lib.pyxhook.pyxhook.HookManager()
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
  lib.pyxhook.pyxhook.print_err(msg)
