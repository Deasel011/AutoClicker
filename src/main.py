from gambler import Gambler
import time
import pyautogui
from jumper import Jumper
from spammer import Spammer
from fisher import Fisher
import tool


def button_smasher():
    spammer = Spammer()
    spammer.start()


def fishing():
    fisher = Fisher()
    fisher.start()


def d2_gamble():
    print("Starting D2 gamble routine in 3 seconds")
    time.sleep(1)
    print(".")
    time.sleep(1)
    print(".")
    time.sleep(1)
    merchant_position = tool.get_position("Place your cursor over merchant.")
    gamble_position = tool.get_position("Place your cursor over the gamble option.")
    item_position = tool.get_position("Place your cursor over the item to buy.")
    print("Please close the gamble shop now.")
    time.sleep(3)

    gm = Gambler(merchant_position, gamble_position, item_position, 31)
    gm.gamble()


def jumper_routine():
    jp = Jumper()
    jp.keep_jumping()


def menu():
    print("Choose routine to run:")
    print("   1 - Lost Ark AFK killer")
    print("   2 - Diablo 2 gambler")
    print("   3 - Lost Ark button smasher")
    print("   4 - Lost Ark fisher")
    print("   9 - Exit")
    option = input("Enter option number ")
    if option == "1":
        jumper_routine()
    elif option == "2":
        d2_gamble()
    elif option == "3":
        button_smasher()
    elif option == "4":
        fishing()
    elif option == "9":
        exit(0)
    else:
        menu()


if __name__ == '__main__':
    menu()
