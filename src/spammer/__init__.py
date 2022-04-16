import pyautogui
import time
import os
import msvcrt
import json
import subprocess
from pynput import keyboard

def get_position(message):
    print(message)
    print("3")
    time.sleep(1)
    print("2")
    time.sleep(1)
    print("1")
    time.sleep(1)
    return pyautogui.position()

def cast(key):
    pyautogui.keyDown(key)
    time.sleep(0.10)
    pyautogui.keyUp(key)
    time.sleep(0.05)
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


class Spammer:
    def __init__(self):
        self.keepOnGoing = True
        self.mash_is_active = False
        self.iterations = 0
        self.config = {
            "keyArea": (0, 0, 0, 0),
            "mappings": {}
        }
        self.active_config = {}
        # Example configuration format
        # "keyArea": (0, 0, 0, 0),
        # "mappings": {
        #     "x": {
        #         "readyImage": 0x0,
        #         "position": (0, 0),
        #         "priority": 1
        #     },
        #     "q": {
        #         "readyImage": 0x0,
        #         "position": (0, 0),
        #         "priority": 2
        #     },
        #     "w": {
        #         "readyImage": 0x0,
        #         "position": (0, 0),
        #         "priority": 3
        #     }

    def save_configuration(self, name):
        with open(f'{name}.json', 'w', encoding='utf-8') as f:
            json.dump(self.config, f, ensure_ascii=False, indent=4)

    def load_configuration(self, name):
        with open(f'{name}.json', 'r', encoding='utf-8') as f:
            self.config = json.loads(f.read())

    def ability_ready(self, image):
        try:
            res = pyautogui.locateOnScreen(image, region=self.config["keyArea"])
            return True
        except pyautogui.ImageNotFoundException:
            return False

    def get_ability_image(self):
        print("Registering new ability")
        time.sleep(1)
        key = input("Enter key to register:")
        priority = input("Enter priority ascending (1 is the highest):")
        topLeft = get_position("Get top left position of abilities")
        bottomRight = get_position("Get bottom right position of abilities")
        self.config["mappings"][key] = {}
        self.config["mappings"][key]["priority"] = int(priority)
        self.config["mappings"][key]["position"] = (
            topLeft[0], topLeft[1], bottomRight[0] - topLeft[0], bottomRight[1] - topLeft[1])

        print('Capturing image in')
        time.sleep(0.5)
        print('3')
        time.sleep(1)
        print('2')
        time.sleep(1)
        print(1)
        time.sleep(1)
        pyautogui.screenshot('ability.png', region=self.config["mappings"][key]["position"])
        subprocess.Popen(['explorer', 'ability.png'])

    def get_ability_bar_position(self):
        topLeft = get_position("Get top left position of abilities")
        print(f'Top Left: {topLeft}')
        bottomRight = get_position("Get bottom right position of abilities")
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
        pyautogui.moveTo(keyarea[0], keyarea[1])
        time.sleep(1)
        pyautogui.moveTo(keyarea[0] + keyarea[2], keyarea[1])
        time.sleep(1)
        pyautogui.moveTo(keyarea[0] + keyarea[2], keyarea[1] + keyarea[3])
        time.sleep(1)
        pyautogui.moveTo(keyarea[0], keyarea[1] + keyarea[3])

    def run(self):
        self.active_config = dict(self.config)
        print("Taking pictures of off cooldown abilities in")
        time.sleep(0.5)
        print('3')
        time.sleep(1)
        print('2')
        time.sleep(1)
        print(1)
        time.sleep(1)
        for key in self.active_config["mappings"].keys():
            array = self.active_config["mappings"][key]["position"]
            position = (array[0], array[1], array[2], array[3])
            self.active_config["mappings"][key]["image"] = pyautogui.screenshot(region=position)
            self.active_config["mappings"][key]["ready"] = True
            self.active_config["mappings"][key]["key"] = key
        sortedKeys = [x[0] for x in sorted(self.active_config["mappings"].items(),
                             key=lambda item: item[1]["priority"])]

        self.keepOnGoing = True

        listener = keyboard.Listener(on_press=self.pressed)
        listener.start()

        print('Press 9 to stop')
        iteration = 1
        while self.keepOnGoing:
            if self.mash_is_active:
                nextKey = next((key for key in sortedKeys if self.active_config["mappings"][key]["ready"]), "")
                print(nextKey)
                if nextKey != "":
                    self.active_config["mappings"][nextKey]["ready"] = False
                    cast(nextKey)
            time.sleep(0.25)
            iteration += 1
            if iteration % 10 == 0:
                for key in self.active_config["mappings"].keys():
                    self.active_config["mappings"][key]["ready"] = \
                        self.ability_ready(self.active_config["mappings"][key]["image"])

        listener.stop()

    def pressed(self, key):
        try:
            if key.char == '0':
                self.mash_is_active = not self.mash_is_active
            if key.char == '9':
                self.keepOnGoing = False
        except AttributeError:
            self.mash_is_active = False

    def start(self):
        self.load_configuration("default")
        self.menu()

    def menu(self):
        print("Choose routine to run:")
        print("   1 - Grab ability bar coordinates")
        print("   2 - Register ability configuration")
        print("   3 - Run spammer")
        print("   5 - Load config")
        print("   6 - Load as <name> config")
        print("   7 - Save config")
        print("   8 - Save as <name> config")
        print("   9 - Exit")
        option = input("Enter option number ")
        if option == "1":
            self.get_ability_bar_position()
        elif option == "2":
            self.get_ability_image()
        elif option == "3":
            self.run()
        elif option == "5":
            self.load_configuration("default")
        elif option == "6":
            name = input("Save name:")
            self.load_configuration(name)
        elif option == "7":
            self.save_configuration("default")
        elif option == "8":
            name = input("Save name:")
            self.save_configuration(name)
        elif option == "9":
            exit(0)
        self.menu()
