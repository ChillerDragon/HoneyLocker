#!/usr/bin/env python3
"""
honeylocker.py [OPTION] [PASSWORD]

Examples:
    ./honeylocker.py --block
    ./honeylocker.py "my password to unlock"
"""

import os
import distutils.spawn
import time
import sys
import itertools

import lib.pyxhook.pyxhook

PASSWORD = None
MODE = 'password'
BLOCKED = []
index = 0
MAX_HISTORY_LEN = 1024
ARG_STRICT_MATCH = False
history = []

def show_help():
    """
    print help text
    """
    print('usage: honeylocker.py [OPTION] [PASSWORD]')
    print('options:')
    print('  --block|-b     use blacklist mode instead of whitelist')
    print('  --cake|-c      default cake blacklist')
    print('  --strict|-s    enable strict match by default "cake" matches "caaake"')

for arg in sys.argv[1:]:
    if arg in ('--help', 'help', '-h'):
        show_help()
        sys.exit()
    elif arg in ('--cake', '-c'):
        MODE = 'blacklist'
        BLOCKED = ["cake", "c a k e", "kuchen", "bring", ":cak", ":cup"]
    elif arg in ('--block', '-b'):
        MODE = 'blacklist'
        PASSWORD = None
    elif arg in ('--strict', '-s'):
        ARG_STRICT_MATCH = True
    elif arg.startswith('-'):
        print(f"Error: invalid arguemnt '{arg}'")
        sys.exit()
    elif MODE == 'blacklist':
        BLOCKED.append(arg)
    else:
        PASSWORD = arg

MODE = 'blacklist'
if PASSWORD:
    MODE = 'password'

print(f"[*] Started in mode {MODE}")
if MODE == 'password':
    if not PASSWORD:
        print("Error: password can not be empty")
        sys.exit(1)
    print(f"[*]   password: {PASSWORD}")
    print('[*]   typing or clicking anything other than the password will lock the screen')
else:
    if len(BLOCKED) == 0:
        print("Error: block list can not be empty")
        print("       specify blocked words as space seperated arguments")
        print("       or use --cake flag for the cake list")
        sys.exit(1)
    print(f"[*]   blacklist: {BLOCKED}")
    print('[*]   typing on of those words into slack will lock your screen')

def lock_screen(dry = False):
    """
    Locks the screen. In dry mode only checks if it is possible.
    """
    lock_executables = ['xdg-screensaver']
    found_lock = False
    for lock_executable in lock_executables:
        if distutils.spawn.find_executable(lock_executable):
            found_lock = True
            break
    if not found_lock:
        print("Error: executable to lock the screen not found")
        print("       expected one of these in path:")
        print("       " + str(lock_executables))
        sys.exit(1)
    if not dry:
        os.system("xdg-screensaver lock")

# Use a function instead a variable to get the time of the pic shot
# and not of the program launch
def pic_path():
    """
    generate filepath for webpack photo including timestamp
    """
    return "~/Desktop/busted_" + time.strftime("_%I_%M_%S") + ".jpeg"

def bust():
    """
    Takes a webcam image and locks the screen

    should be called when a intruder is detected
    """
    # os.system("say 'Enemy input detected'")
    # os.system("streamer -f jpeg -o " + PicPath() + " 2> /dev/null")
    os.system("ffmpeg -f video4linux2 -i /dev/video0 -vframes 1 " + pic_path() + " 2> /dev/null")
    lock_screen()
    sys.exit()

def check_blacklist():
    """
    Check if the currently typed key
    forms a word that is blacklisted
    """
    hist_str = ''.join(history)
    if not ARG_STRICT_MATCH:
        hist_str = ''.join(ch for ch, _ in itertools.groupby(hist_str))
    for block in BLOCKED:
        if block in hist_str:
            print(f"found blocked word {block}")
            return False
        print(f"{block} not found in {''.join(history)}")
    return True

def check_passwd(key):
    """
    Check if the currently typed key
    is part of the unlock password
    or a intrusiom
    """
    global index
    if len(PASSWORD) == index:
        sys.exit() # correct passwd
    if PASSWORD[index] == key:
        index += 1
        return True
    return False

def on_key_press(event):
    """
    handle all keypresses
    """
    global history
    key = event.Key.lower()
    if not key.startswith('shift'):
        if key == 'space':
            key = ' '
        if key == 'backspace':
            if len(history) > 0:
                history = history[:len(history)-1]
        else:
            history.append(key)
        if len(history) > 2:
            history = history[len(history)-MAX_HISTORY_LEN:]
    if MODE == 'password':
        if check_passwd(key):
            return
    else:
        if event.WindowProcName != 'slack':
            return
        if check_blacklist():
            return
    print("key pressed: " + event.Key)
    bust()

def on_mouse_click(event):
    """
    handle all mouse clicks
    """
    if MODE == 'blacklist':
        return
    # rightclick blocks the screen lock
    # -> only lock on left click
    if event.MessageName != "mouse left  down":
        return
    bust()

def check_deps():
    """
    Check if all needed dependencies are installed
    """
    lock_screen(dry = True)
    if not distutils.spawn.find_executable('ffmpeg'):
        print('Warning: ffmpeg not found in path')
        print('         will not take webcam photo')

new_hook = lib.pyxhook.pyxhook.HookManager()
new_hook.KeyDown = on_key_press
new_hook.MouseAllButtonsDown = on_mouse_click
new_hook.HookKeyboard()

try:
    new_hook.start()
except KeyboardInterrupt:
    # User cancelled from command line.
    pass
except Exception as ex:
    msg = f"Error while catching events:\n {ex}"
    print(msg)
