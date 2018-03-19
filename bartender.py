#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
0] Init stuff 
1] Waits until the game starts
2] Loads UI
""" 
from pymemory import pymemory as pm
from pymemory import NullAddress
from aoc_game import Game
from ui_main_window import BartenderWindow
from PyQt5 import QtWidgets 

import sys
import time
print("Loading the process")
try:
    pm.load_process("AoK HD.exe")
except ProcessLookupError:
    print("Process not found")
    exit()
with pm:
    print("Starting the parser - waiting until the game is started")
    game = None
    while game is None:
        try:
            game = Game()
        except (NullAddress, UnicodeDecodeError):
            time.sleep(0.01)
    print("First parse")
    # Need some better way how to init the game.
    game.update()
    print("Starting the window")
    # create qapp 
    app = QtWidgets.QApplication(sys.argv)
    # getting screen resolution
    screen_resolution = app.desktop().screenGeometry()
    width, height = screen_resolution.width(), screen_resolution.height()
    # Load data in the window
    window = BartenderWindow(game, width, height)
    window.show()
    # woho
    result = app.exec_()
print("Ending the session")
sys.exit(result)

