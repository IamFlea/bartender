#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
0] Init stuff 
1] Waits until the game starts
2] Loads UI
""" 
import sys
import time
import win32gui

from pymemory import NullAddress, pymemory as pm
from aoc_game import Game
from ui_main_window import BartenderWindow
from PyQt5 import QtWidgets 

# Local Variables
process_name = "AoK HD.exe"
load_process_only_once = True # Breaks infinite loop if process not found and exits this script.
print_infostatus = True
loop_sleep_time = 0.01 # in seoncds

# Function for printing stuff 
def print_info(string):
    global print_infostatus
    if print_infostatus:
        print(string)

def load_process(process_name, load_process_only_once, loop_sleep_time):
    """ Loading the process.
    If `load_process_only_once` is true, exits the program!

    process_name            String, the name of process in tasklist.
    load_process_only_once  Boolean, breaks infinite loop. 
    loop_sleep_time         Float, sleep time in loop
    """
    print_info(f"Loading the process {process_name}. Be sure it is running.")
    while True: 
        try:
            pm.load_process(process_name)
            return
        except ProcessLookupError:
            pass
        if load_process_only_once:
            print_info(f"Process not found.")
            exit(404)
        time.sleep(loop_sleep_time)

def load_game(loop_sleep_time):
    # must be run in a block `with pm`
    print_info("Starting the parser - waiting until the game is started")
    game = None
    while game is None:
        try:
            game = Game()
        except (NullAddress, UnicodeDecodeError):
            time.sleep(loop_sleep_time)
    print_info("Game loaded. Starting the first iteration.")
    game.update()
    return game

def get_aoe_window_size(hwnd, extra):
    global x, y, width, height
    if "Age of Empires II: HD Edition" != win32gui.GetWindowText(hwnd):
        return
    #print(win32gui.GetWindowText(hwnd))
    rect = win32gui.GetWindowRect(hwnd)
    x = rect[0]
    y = rect[1]
    width = rect[2] - x
    height = rect[3] - y

    

# Loading process
load_process(process_name, load_process_only_once, loop_sleep_time)
with pm:
    game = load_game(loop_sleep_time)
    # Getting aoe window location and resolution
    x, y, width, height = None, None, None, None
    win32gui.EnumWindows(get_aoe_window_size, None) # Previous values are villed with this

    # create qapp 
    app = QtWidgets.QApplication(sys.argv)
    #print(x,y,width,height)
    window = BartenderWindow(game, x, y, width, height)
    window.show()
    # woho
    result = app.exec_()
print("Ending the session")
sys.exit()

# EOF: bartender.py
