import datetime
from src.tool import get_position
import pyautogui
import time
import os
import msvcrt
from pynput import keyboard


def cast(key):
    pyautogui.keyDown(key)
    time.sleep(0.10)
    pyautogui.keyUp(key)

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


class Fisher:
    def __init__(self):
        self.bauble_is_active = False
        self.bauble_activated = None
        self.keepOnGoing = True
        self.fishing_is_active = False
        self.iterations = 0
        self.config = {
            "keyArea": (630, 345, 750, 445),
            "mappings": {}
        }

    def locate_image(self, image):
        try:
            print(f'Locating image {image}')
            res = pyautogui.locateOnScreen(image, region=self.config["keyArea"], grayscale=True)
            print(f'     result:{res}')
            return res is not None
        except pyautogui.ImageNotFoundException:
            return False

    def get_fishing_area_position(self):
        topLeft = get_position("Get top left position of fishing area")
        print(f'Top Left: {topLeft}')
        bottomRight = get_position("Get bottom right position of fishing area")
        print(f'Bottom right: {bottomRight}')
        self.config["keyArea"] = (topLeft[0], topLeft[1], bottomRight[0] - topLeft[0], bottomRight[1] - topLeft[1])
        keyarea = self.config["keyArea"]
        print('Displaying the boundaries in')
        time.sleep(0.5)
        print('3')
        time.sleep(1)
        print('2')
        time.sleep(1)
        print(1)
        time.sleep(1)
        self.show_boundary(keyarea)

    def show_boundary(self, keyarea):
        pyautogui.moveTo(keyarea[0], keyarea[1])
        time.sleep(1)
        pyautogui.moveTo(keyarea[0] + keyarea[2], keyarea[1])
        time.sleep(1)
        pyautogui.moveTo(keyarea[0] + keyarea[2], keyarea[1] + keyarea[3])
        time.sleep(1)
        pyautogui.moveTo(keyarea[0], keyarea[1] + keyarea[3])

    def cast_rod(self):
        self.bauble_activated = time.time()
        print('Casting rod.')
        cast('e')
        self.bauble_is_active = True
        time.sleep(2)
        self.show_boundary(self.config["keyArea"])

    def reel_in(self):
        print('Reeling in.')
        cast('e')
        time.sleep(7)
        self.bauble_is_active = False
        self.bauble_activated = None

    def run(self):
        self.keepOnGoing = True

        listener = keyboard.Listener(on_press=self.pressed)
        listener.start()

        print('Press 9 to stop')
        iteration = 1
        while self.keepOnGoing:
            if self.fishing_is_active:
                if self.bauble_activated is not None and int(time.time()-self.bauble_activated) > 15:
                    self.reel_in()
                elif self.bauble_is_active:
                    if self.locate_image('exclamation.png'):
                        self.reel_in()
                elif not self.bauble_is_active:
                    self.cast_rod()
            time.sleep(0.100)
            iteration += 1

        listener.stop()

    def pressed(self, key):
        try:
            if key.char == '0':
                self.fishing_is_active = not self.fishing_is_active
            if key.char == '9':
                self.keepOnGoing = False
        except AttributeError:
            self.fishing_is_active = False

    def start(self):
        self.menu()

    def menu(self):
        print("Choose routine to run:")
        print("   1 - Grab fishing area coordinates")
        print("   2 - Run fisher")
        print("   9 - Exit")
        option = input("Enter option number ")
        if option == "1":
            self.get_fishing_area_position()
        elif option == "2":
            self.run()
        elif option == "9":
            exit(0)
        self.menu()
