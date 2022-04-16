from random import randint

import pyautogui
import time
import os
import msvcrt


def jump():
    pyautogui.keyDown('8')
    time.sleep(0.10)
    pyautogui.keyUp('8')
    time.sleep(randint(30, 40))


def clear_console():
    command = 'clear'
    if os.name in ('nt', 'dos'):
        command = 'cls'
    os.system(command)


# Shamelessly ripped from
# https://stackoverflow.com/questions/29289945/how-to-temporarily-disable-keyboard-input-using-python
class KeyboardDisable:

    def start(self):
        self.on = True

    def stop(self):
        self.on = False

    def __call__(self):
        while self.on:
            msvcrt.getwch()

    def __init__(self):
        self.on = False


class Jumper:
    def __init__(self):
        self.iterations = 0

    def keep_jumping(self):
        keyboardDisable = KeyboardDisable()
        while 1 == 1:
            clear_console()
            print("Close the tab to stop.")
            print(f"Amount of jumps currently at: {self.iterations}")
            keyboardDisable.start()
            jump()
            keyboardDisable.stop()
            self.iterations += 1
