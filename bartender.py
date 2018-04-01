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

from PyQt5 import QtWidgets, QtCore

from pymemory import NullAddress, pymemory as pm
from aoc_game import Game
from aoc_lobby import Lobby, LobbyException
from ui_window_overlay import BartenderOverlay

class Bartender(QtWidgets.QMainWindow):
    AOK_PROCESS_NAME = "AoK HD.exe"
    UPDATE_WINDOW_MS = 33  # 30 FPS 
    #UPDATE_WINDOW_MS = 16  # 60 FPS 
    load_process_only_once = True # Breaks infinite loop if process not found and exits this script.
    CONSOLE_PRINT_INFO = True
    WINDOW_PRINT_INFO = True
    
    SPAN = 10
    WINDOW_TITLE = "Bartender"
    WINDOW_WIDTH = 400
    WINDOW_HEIGHT = 300
    LABEL_INFO_MARGIN = SPAN
    LABEL_INFO_HEIGHT = 20
    LABEL_INFO_WIDTH = WINDOW_WIDTH

    # Sets textarea to bottom
    TEXTAREA_BALANCE_WIDTH = 200
    TEXTAREA_BALANCE_HEIGHT = 40
    TEXTAREA_BALANCE_MARGIN_X = (WINDOW_WIDTH - TEXTAREA_BALANCE_WIDTH)//2  # Centers
    TEXTAREA_BALANCE_MARGIN_Y = WINDOW_HEIGHT - TEXTAREA_BALANCE_HEIGHT - SPAN 
    # Sets button above the textarea
    BUTTON_INFO_WIDTH = 100
    BUTTON_INFO_HEIGHT = 20
    BUTTON_INFO_MARGIN_X = (WINDOW_WIDTH - BUTTON_INFO_WIDTH)//2  # Centers
    BUTTON_INFO_MARGIN_Y = TEXTAREA_BALANCE_MARGIN_Y  - BUTTON_INFO_HEIGHT - SPAN

    # Function for printing stuff 
    def print_info(self, string):
        if string == self.label_info.lastmsg: 
            return
        if Bartender.CONSOLE_PRINT_INFO:
            print(string)
        if Bartender.WINDOW_PRINT_INFO:
            self.label_info.setText(string)
        self.label_info.lastmsg = string

    def __init__(self, screen_width, screen_height, app):
        """ Constuctor, inits a new window with informations about bartender
        
        `screen_width`   Screen resolution
        `screen_height`  Screen resolution
        """
        super(Bartender, self).__init__()

        ### WINDOW SETTINGS
        self.setWindowTitle(Bartender.WINDOW_TITLE)
        # Set the position of Window to the center.
        self.setGeometry((screen_width - Bartender.WINDOW_WIDTH)//2,   # X
                         (screen_height - Bartender.WINDOW_HEIGHT)//2, # Y
                         Bartender.WINDOW_WIDTH,  # Window width
                         Bartender.WINDOW_HEIGHT) # WIndow height
        
        ### WIDGETS SETINGS
        self.bartender_overlay = None

        self.label_info = QtWidgets.QLabel(self)
        self.label_info.setGeometry(Bartender.LABEL_INFO_MARGIN, # X
                                    Bartender.LABEL_INFO_MARGIN, # Y
                                    Bartender.LABEL_INFO_WIDTH - Bartender.LABEL_INFO_MARGIN*2, # Width of window - margins
                                    Bartender.LABEL_INFO_HEIGHT)
        self.label_info.setAlignment(QtCore.Qt.AlignCenter)
        self.label_info.lastmsg = ""
        
        self.button_balance = QtWidgets.QPushButton("Balance Lobby!", self)
        self.button_balance.setGeometry(Bartender.BUTTON_INFO_MARGIN_X,
                                        Bartender.BUTTON_INFO_MARGIN_Y,
                                        Bartender.BUTTON_INFO_WIDTH, 
                                        Bartender.BUTTON_INFO_HEIGHT)
        self.button_balance.clicked.connect(self.balance_it)

        self.textarea_balance = QtWidgets.QTextEdit(self)
        self.textarea_balance.setGeometry(Bartender.TEXTAREA_BALANCE_MARGIN_X, 
                                          Bartender.TEXTAREA_BALANCE_MARGIN_Y, 
                                          Bartender.TEXTAREA_BALANCE_WIDTH, 
                                          Bartender.TEXTAREA_BALANCE_HEIGHT)

        #### OTHER STUFF
        self.app = app
        self.game = None
        self.lobby = Lobby()
        self.state = 0
        self.show()
        
    
    def __load_process_loop__(self):
        self.print_info(f"Loading the process {Bartender.AOK_PROCESS_NAME}. Be sure it is running.")
        try:
            pm.load_process(Bartender.AOK_PROCESS_NAME)
        except ProcessLookupError:
            return
        self.process_timer.stop()
        self.app.exit()        

    def load_process(self):
        """ Loading the process """
        self.process_timer = QtCore.QTimer()
        self.process_timer.timeout.connect(self.__load_process_loop__)
        self.process_timer.start(Bartender.UPDATE_WINDOW_MS)
        self.app.exec_()

    def balance_it(self):
        try:
            self.lobby.update()
        except:
            self.textarea_balance.setText(f"Couldn't parse Lobby")
            return
        try:
            diff1, string1, teams1 = self.lobby.balance_minmax()
            diff2, string2, teams2 = self.lobby.balance_diff()
            self.textarea_balance.setText(f"Minmax: {string1}\nDiff: {string2}")
        except LobbyException as e:
            self.textarea_balance.setText(str(e)[1:-1])
        except:
            self.textarea_balance.setText(f"Couldn't parse Lobby")
            return
        #print(diff1, string1)
        #print(diff2, string2)
    
    def load_game(self):
        # must be run in a block `with pm`
        try:
            self.game = Game()
        except:
            self.game = None
            
    def start_overlay(self):
        # Getting aoe window location and resolution
        global x, y, width, height
        x, y, width, height = None, None, None, None
        def function(hwnd, extra):
            global x, y, width, height
            if "Age of Empires II: HD Edition" != win32gui.GetWindowText(hwnd):
                return
            #print(win32gui.GetWindowText(hwnd))
            rect = win32gui.GetWindowRect(hwnd)
            x = rect[0]
            y = rect[1]
            width = rect[2] - x
            height = rect[3] - y
        win32gui.EnumWindows(function, None) # Previous values are filled with this
        self.bartender_overlay = BartenderOverlay(self.game, x, y, width, height)
        self.bartender_overlay.show()

    def closeEvent(self, event):
        # Closing the window.
        self.print_info("Ending the session")
        self.print_info = lambda x: x
        if self.bartender_overlay is not None:
            self.bartender_overlay.close()

    def load_lobby(self):
        # Loads lobby data
        try: 
            self.lobby.update()
        except:
            self.lobby = Lobby()
        
    def finite_state_machine(self):
        # State machine.
        if self.state == 0:
            # Loading the game
            self.print_info("Waiting until the game is started.")
            self.load_game()
            if self.game is not None:
                self.state = 2
                self.lobby = None
        #if self.state == 1:
        # Getting first iteration
        if self.state == 2:
            self.print_info("Game loaded. Starting the first iteration.")
            self.game.update()
            if self.game.running:
                self.state = 3
        # Starting overlay
        if self.state == 3:
            self.print_info("Starting overlay.")
            self.start_overlay()
            self.state = 4  
        # Loop
        if self.state == 4:
            self.print_info("Waiting until the game is quitted.")
            if not self.game.running:
                self.bartender_overlay.deleteLater()
                self.bartender_overlay = None
                self.state = 0

    def run(self):
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.finite_state_machine)
        self.timer.start(Bartender.UPDATE_WINDOW_MS)

        


if __name__ == '__main__':
    # Start bartender window.
    app = QtWidgets.QApplication(sys.argv)
    resolution = app.desktop().screenGeometry()
    bartender = Bartender(resolution.width(), resolution.height(), app)
    bartender.load_process()
    with pm:
        bartender.run()
        result = app.exec_()
    sys.exit(result)
# EOF: bartender.py
