#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
0] Init UI
1] Waits until the game starts 
2] Loads overlay settings
3] Loads overlay
""" 
import sys
import time

from PyQt5 import QtWidgets, QtCore, Qt, QtGui

from pymemory import pymemory as pm

from aoc_game import Game
from aoc_lobby import Lobby, LobbyException
from interface_bar import InterfaceBar
from interface_header import InterfaceHeader
from ui_overlay import Overlay

from config import * 

class Bartender(QtWidgets.QMainWindow):
    BARTENDER_FRAMES_PER_SECOND = 30 # FPS of main window 
    UPDATE_WINDOW_MS = int(1 / BARTENDER_FRAMES_PER_SECOND) 
    
    CONSOLE_PRINT_INFO = True
    WINDOW_PRINT_INFO = True
    
    SPAN = 10
    WINDOW_TITLE = "Bartender"
    WINDOW_WIDTH = 500
    WINDOW_HEIGHT = 500
    WIDE = WINDOW_WIDTH - SPAN*2

    CHECKBOX_HEIGHT = 13

    GEOMETRY_LABEL_INFO = Qt.QRect(SPAN, SPAN, WIDE, 20) # X, Y, WIDTH, HEIGHT
    
    GEOMETRY_CHECKBOX_EDITALL =  Qt.QRect(SPAN, GEOMETRY_LABEL_INFO.y() + GEOMETRY_LABEL_INFO.height() + SPAN, (WINDOW_WIDTH-SPAN*(1+4))/4, CHECKBOX_HEIGHT) # X, Y, WIDTH, HEIGHT
  
    GEOMETRY_CHECKBOX_BARTENDER_ONTOP = Qt.QRect(GEOMETRY_CHECKBOX_EDITALL.x() + GEOMETRY_CHECKBOX_EDITALL.width() + SPAN, 
                                                 GEOMETRY_LABEL_INFO.y() + GEOMETRY_LABEL_INFO.height() + SPAN, 
                                                 (WINDOW_WIDTH-SPAN*(1+4))/4, 
                                                 CHECKBOX_HEIGHT) 

    GEOMETRY_CHECKBOX_RESEARCHED_TECHS = Qt.QRect(SPAN, 
                                                  GEOMETRY_CHECKBOX_EDITALL.y() + GEOMETRY_CHECKBOX_EDITALL.height() + SPAN, 
                                                  (WINDOW_WIDTH-SPAN*(1+4))/4, 
                                                  CHECKBOX_HEIGHT) 
    GEOMETRY_CHECKBOX_RESEARCH_BARS = Qt.QRect(GEOMETRY_CHECKBOX_RESEARCHED_TECHS.x() + GEOMETRY_CHECKBOX_RESEARCHED_TECHS.width() + SPAN,  
                                               GEOMETRY_CHECKBOX_EDITALL.y() + GEOMETRY_CHECKBOX_EDITALL.height() + SPAN, 
                                               (WINDOW_WIDTH-SPAN*(1+4))/4, 
                                               CHECKBOX_HEIGHT) 
    GEOMETRY_CHECKBOX_WAYPOINT =  Qt.QRect(GEOMETRY_CHECKBOX_RESEARCH_BARS.x() + GEOMETRY_CHECKBOX_RESEARCH_BARS.width() + SPAN,  
                                               GEOMETRY_CHECKBOX_EDITALL.y() + GEOMETRY_CHECKBOX_EDITALL.height() + SPAN, 
                                               (WINDOW_WIDTH-SPAN*(1+4))/4, 
                                               CHECKBOX_HEIGHT) 


    GEOMETRY_BUTTON_NEW_HEADER = Qt.QRect(GEOMETRY_CHECKBOX_WAYPOINT.x() + GEOMETRY_CHECKBOX_WAYPOINT.width() + SPAN,  
                                               GEOMETRY_LABEL_INFO.y() + GEOMETRY_LABEL_INFO.height() + SPAN-4, 
                                               (WINDOW_WIDTH-SPAN*(1+4))/4, 
                                               CHECKBOX_HEIGHT+8) 
    GEOMETRY_BUTTON_NEW_BAR = Qt.QRect(GEOMETRY_CHECKBOX_WAYPOINT.x() + GEOMETRY_CHECKBOX_WAYPOINT.width() + SPAN,  
                                               GEOMETRY_CHECKBOX_EDITALL.y() + GEOMETRY_CHECKBOX_EDITALL.height() + SPAN-4, 
                                               (WINDOW_WIDTH-SPAN*(1+4))/4, 
                                               CHECKBOX_HEIGHT+8) 

    GEOMETRY_TAB_BAR_SETTINGS_HEIGHT = 285
    GEOMETRY_TAB_BAR_SETTINGS = Qt.QRect(SPAN,  # X
                                    GEOMETRY_CHECKBOX_RESEARCHED_TECHS.y() + GEOMETRY_CHECKBOX_RESEARCHED_TECHS.height() + SPAN, # Y
                                    WIDE,
                                    GEOMETRY_TAB_BAR_SETTINGS_HEIGHT)


    ## FROM BOTTOM TO TOP
    # Sets textarea above the button
    GEOMETRY_BUTTON_BALANCE_WIDTH = 100
    GEOMETRY_BUTTON_BALANCE_HEIGHT = 20
    GEOMETRY_BUTTON_BALANCE = Qt.QRect((WINDOW_WIDTH - GEOMETRY_BUTTON_BALANCE_WIDTH)//2,  # X
                                    WINDOW_HEIGHT - GEOMETRY_BUTTON_BALANCE_HEIGHT - SPAN * 2, # Y
                                    GEOMETRY_BUTTON_BALANCE_WIDTH,
                                    GEOMETRY_BUTTON_BALANCE_HEIGHT)

    # Sets textarea balence position
    GEOMETRY_TEXTAREA_BALANCE_WIDTH = 200
    GEOMETRY_TEXTAREA_BALANCE_HEIGHT = 40
    GEOMETRY_TEXTAREA_BALANCE = Qt.QRect((WINDOW_WIDTH - GEOMETRY_TEXTAREA_BALANCE_WIDTH)//2,  # X
                                         GEOMETRY_BUTTON_BALANCE.y() - GEOMETRY_TEXTAREA_BALANCE_HEIGHT - SPAN, # Y
                                         GEOMETRY_TEXTAREA_BALANCE_WIDTH,
                                         GEOMETRY_TEXTAREA_BALANCE_HEIGHT)

    # Function for printing stuff 
    def print_info(self, string):
        if string == self.statusbar.lastmsg: 
            return
        if Bartender.CONSOLE_PRINT_INFO:
            print(string)
        if Bartender.WINDOW_PRINT_INFO:
            self.statusbar.showMessage("Status: " + string)
        self.statusbar.lastmsg = string

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
        # INFO LABEL
        self.w_bartender_title = QtWidgets.QLabel(self)
        self.w_bartender_title.setGeometry(Bartender.GEOMETRY_LABEL_INFO)
        self.w_bartender_title.setAlignment(QtCore.Qt.AlignCenter)
        self.w_bartender_title.setText(Bartender.WINDOW_TITLE)

        font = QtGui.QFont(self.w_bartender_title.font().family(), 12)
        font.setBold(True)
        self.w_bartender_title.setFont(font)
        
        # Movable bars checkbox
        self.w_checkbox_waypoints = QtWidgets.QCheckBox("Waypoint Icons", self)
        self.w_checkbox_waypoints.setGeometry(Bartender.GEOMETRY_CHECKBOX_WAYPOINT)
        #self.w_checkbox_waypoints.stateChanged.connect(self.moveable)

        self.w_checkbox_editall = QtWidgets.QCheckBox("All Bars Movable", self)
        self.w_checkbox_editall.setGeometry(Bartender.GEOMETRY_CHECKBOX_EDITALL)
        self.w_checkbox_editall.stateChanged.connect(self.moveable)

        self.w_checkbox_bartender_ontop = QtWidgets.QCheckBox("Bartender on Top", self)
        self.w_checkbox_bartender_ontop.setGeometry(Bartender.GEOMETRY_CHECKBOX_BARTENDER_ONTOP)
        #self.w_checkbox_bartender_ontop.stateChanged.connect(self.moveable)

        self.w_checkbox_research_bars = QtWidgets.QCheckBox("Research Bars", self)
        self.w_checkbox_research_bars.setGeometry(Bartender.GEOMETRY_CHECKBOX_RESEARCH_BARS)
        
        self.w_checkbox_researched_techs = QtWidgets.QCheckBox("Researched Techs", self)
        self.w_checkbox_researched_techs.setGeometry(Bartender.GEOMETRY_CHECKBOX_RESEARCHED_TECHS)
        
        self.w_button_new_header = QtWidgets.QPushButton("New Header", self)
        self.w_button_new_header.setGeometry(Bartender.GEOMETRY_BUTTON_NEW_HEADER)
        self.w_button_new_header.clicked.connect(self.add_new_header)

        self.w_button_new_bar = QtWidgets.QPushButton("New Bar", self)
        self.w_button_new_bar.setGeometry(Bartender.GEOMETRY_BUTTON_NEW_BAR)
        self.w_button_new_bar.clicked.connect(self.add_new_bar)

        # Tab
        self.w_tabs_settings = QtWidgets.QTabWidget(self)
        self.w_tabs_settings.setGeometry(Bartender.GEOMETRY_TAB_BAR_SETTINGS)
        self.w_tabs_settings.setHidden(True)

        

        # Balancing BUTTON
        self.balance_widgets = []
        self.w_button_balance = QtWidgets.QPushButton("Balance Lobby!", self)
        self.w_button_balance.setGeometry(Bartender.GEOMETRY_BUTTON_BALANCE)
        self.w_button_balance.clicked.connect(self.balance_it)
        self.balance_widgets.append(self.w_button_balance)
        # Balancing Textarea
        self.w_textarea_balance = QtWidgets.QTextEdit(self)
        self.w_textarea_balance.setGeometry(Bartender.GEOMETRY_TEXTAREA_BALANCE)
        self.balance_widgets.append(self.w_textarea_balance)
        
        self.w_tabs_settings.addTab(InterfaceBar("New Bar", self), f"New Bar")

        self.statusbar = QtWidgets.QStatusBar()
        self.statusbar.lastmsg = ""
        self.setStatusBar(self.statusbar)


        #### OTHER STUFF
        self.app = app
        self.overlay = None
        self.game = None
        self.lobby = Lobby()
        self.state = -1
        self.process_timer = None
        self.timer = None
        self.show()
        
    def setHiddenList(self, widgets, boolean):

        for widget in widgets:
            widget.setHidden(boolean)
    
    def __load_process_loop__(self):
        self.print_info(f"Loading the process {AOK_PROCESS_NAME}. Be sure it is running.")
        try:
            pm.load_process(AOK_PROCESS_NAME)
        except ProcessLookupError: 
            return
        self.state = 0
        self.process_timer.stop()
        self.app.exit()        

    def load_process(self):
        """ Loading the process timer """
        self.process_timer = QtCore.QTimer()
        self.process_timer.timeout.connect(self.__load_process_loop__)
        self.process_timer.start(Bartender.UPDATE_WINDOW_MS)
        self.app.exec_()
        

    def balance_it(self):
        try:
            self.lobby.update()
        except:
            self.w_textarea_balance.setText(f"Couldn't parse Lobby")
            return
        try:
            diff1, string1, teams1 = self.lobby.balance_minmax()
            diff2, string2, teams2 = self.lobby.balance_diff()
            self.w_textarea_balance.setText(f"Minmax: {string1}\nDiff: {string2}")
        except LobbyException as e:
            self.w_textarea_balance.setText(str(e)[1:-1])
        except:
            self.w_textarea_balance.setText(f"Couldn't parse Lobby")
            return
        
    def load_game(self):
        # must be run in a block `with pm`
        try:
            self.game = Game()
        except:
            self.game = None
    
                
    def start_overlay(self):
        # Starting overlay UI
        self.overlay = Overlay(self, self.game)
        self.overlay.show()

    def closeEvent(self, event):
        # Closing the window.
        self.print_info("Ending the session")
        if self.process_timer is not None:
            self.process_timer.stop()
        if self.timer is not None:
            self.timer.stop()
        if self.overlay is not None:
            self.overlay.close()

    def load_lobby(self):
        # Loads lobby data
        try: 
            self.lobby.update()
        except:
            self.lobby = Lobby()
        
    def finite_state_machine(self):
        # State machine.
        self.print_info("Waiting until the game is started.")
        if self.state == 0:
            # Loading the game
            self.load_game()
            self.setHiddenList(self.balance_widgets, False)
            self.w_tabs_settings.setHidden(True)
            if self.game is not None:
                self.state = 2
                self.lobby = None
                self.print_info("Game loaded. Starting the first iteration.")
        # Getting first iteration
        if self.state == 2:
            self.game.update()
            if self.game.running:
                self.state = 3
                self.print_info("Starting overlay.")
        # Starting overlay
        if self.state == 3:
            self.start_overlay()
            self.w_tabs_settings.setHidden(False)
            self.setHiddenList(self.balance_widgets, True)
            self.load_bars()
            self.state = 4  
            self.print_info("Waiting until the game is quitted.")
        # Loop
        if self.state == 4:
            if not self.game.running:
                self.overlay.deleteLater()
                self.overlay = None
                self.state = 0

    def run(self):
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.finite_state_machine)
        self.timer.start(Bartender.UPDATE_WINDOW_MS)

    def moveable(self):
        if self.w_checkbox_editall.isChecked():
            self.overlay.set_movable_widgets(True)
        else:
            self.overlay.set_movable_widgets(False)
    
    def add_new_header(self):
        self.w_tabs_settings.addTab(QtWidgets.QWidget(self), f"New Tab")
        
    def add_new_bar(self):
        name = f"New Bar"
        widget = InterfaceBar(name, self)
        self.w_tabs_settings.addTab(widget, name)
        self.load_bars()
        #self.w_tabs_settings.

    def load_bars(self):
        if self.overlay is None:
            return
        for idx in range(self.w_tabs_settings.count()):
            self.overlay.create_bar(self.w_tabs_settings.widget(idx))


if __name__ == '__main__' or True:
    # Start bartender window.
    app = QtWidgets.QApplication(sys.argv)
    resolution = app.desktop().screenGeometry()
    bartender = Bartender(resolution.width(), resolution.height(), app)
    bartender.load_process()
    if bartender.state == -1:
        sys.exit()
    with pm:
        bartender.run()
        result = app.exec_()
    sys.exit(result)
# EOF: bartender.py
