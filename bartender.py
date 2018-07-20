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
from interface_info_panel import InterfaceInfoPanel
from interface_offscreen_units import InterfaceOffscreenUnits
from ui_overlay import Overlay

from config import * 
from bartender_save_load import *

class Bartender(QtWidgets.QMainWindow):
    BARTENDER_FRAMES_PER_SECOND = 30 # FPS of main window 
    UPDATE_WINDOW_MS = int(1 / BARTENDER_FRAMES_PER_SECOND) 
    
    CONSOLE_PRINT_INFO = True
    WINDOW_PRINT_INFO = True
    
    SPAN = 10
    WINDOW_TITLE = "Bartender"
    WINDOW_WIDTH = 764
    WINDOW_HEIGHT = 600
    WIDE = WINDOW_WIDTH - SPAN*2
    WIDE_FOURTH = (WINDOW_WIDTH - SPAN*(1+4))/4
    
    CELL_HEIGHT = 13

    GEOMETRY_LABEL_INFO = Qt.QRect(SPAN, SPAN, WIDE, SPAN * 2) # X, Y, WIDTH, HEIGHT


    GEOMETRY_CENTER = Qt.QRect(SPAN, SPAN, WIDE, WINDOW_HEIGHT - SPAN * 2) # X, Y, WIDTH, HEIGHT
    


    GEOMETRY_0_0 = Qt.QRect(SPAN, GEOMETRY_LABEL_INFO.bottom() + 1 + SPAN, WIDE_FOURTH, CELL_HEIGHT) 
    GEOMETRY_0_1 = Qt.QRect(SPAN+(SPAN + WIDE_FOURTH)*1, GEOMETRY_0_0.y(), WIDE_FOURTH, CELL_HEIGHT) 
    GEOMETRY_0_2 = Qt.QRect(SPAN+(SPAN + WIDE_FOURTH)*2, GEOMETRY_0_0.y(), WIDE_FOURTH, CELL_HEIGHT) 
    GEOMETRY_0_3 = Qt.QRect(SPAN+(SPAN + WIDE_FOURTH)*3, GEOMETRY_0_0.y()-4, WIDE_FOURTH, CELL_HEIGHT+8) 
    GEOMETRY_00_3 = Qt.QRect(SPAN+(SPAN + WIDE_FOURTH)*3, GEOMETRY_0_0.y()-SPAN-CELL_HEIGHT, WIDE_FOURTH, CELL_HEIGHT) 
    
    GEOMETRY_1_0 = Qt.QRect(SPAN, GEOMETRY_0_0.bottom() + 1 + SPAN, WIDE_FOURTH, CELL_HEIGHT) 
    GEOMETRY_1_1 = Qt.QRect(SPAN+(SPAN + WIDE_FOURTH)*1, GEOMETRY_1_0.y(), WIDE_FOURTH, CELL_HEIGHT) 
    GEOMETRY_1_2 = Qt.QRect(SPAN+(SPAN + WIDE_FOURTH)*2, GEOMETRY_1_0.y(), WIDE_FOURTH, CELL_HEIGHT) 
    GEOMETRY_1_3 = Qt.QRect(SPAN+(SPAN + WIDE_FOURTH)*3, GEOMETRY_1_0.y()-4, WIDE_FOURTH, CELL_HEIGHT+8) 
    

    GEOMETRY_TAB_BAR_SETTINGS_HEIGHT = 285+26+100+50
    GEOMETRY_TAB_BAR_SETTINGS = Qt.QRect(SPAN,  # X
                                    GEOMETRY_1_0.bottom() + 1 + SPAN, # Y
                                    WIDE,
                                    GEOMETRY_TAB_BAR_SETTINGS_HEIGHT)


    # Function for printing FSM position
    def print_info(self, string):
        if string == self.statusbar.lastmsg: 
            return
        if Bartender.CONSOLE_PRINT_INFO:
            print(f"<FSM> {string}")
        if Bartender.WINDOW_PRINT_INFO:
            self.statusbar.showMessage(f"Status: {string}")
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

        # INFO LABEL
        self.w_bartender_title = QtWidgets.QLabel(self)
        self.w_bartender_title.setGeometry(Bartender.GEOMETRY_LABEL_INFO)
        self.w_bartender_title.setAlignment(QtCore.Qt.AlignCenter)
        self.w_bartender_title.setText(Bartender.WINDOW_TITLE)

        font = QtGui.QFont(self.w_bartender_title.font().family(), 12)
        font.setBold(True)
        self.w_bartender_title.setFont(font)


        # Status bar
        self.statusbar = QtWidgets.QStatusBar()
        self.statusbar.lastmsg = ""
        self.setStatusBar(self.statusbar)
        # Info
        self.info_label = QtWidgets.QLabel("Start the game already!", self)
        self.info_label.setGeometry(Bartender.GEOMETRY_CENTER)
        self.info_label.setAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont(self.w_bartender_title.font().family(), 10)
        self.info_label.setFont(font)
        self.show()
        # consts

        ### WIDGETS SETINGS
        # Checkboxes
        self.w_checkbox_completed_researches = QtWidgets.QCheckBox("Completed Researches", self)
        self.w_checkbox_completed_researches.setGeometry(Bartender.GEOMETRY_1_0)
        self.w_checkbox_completed_researches.stateChanged.connect(self.researches_policy)
        self.w_checkbox_completed_researches.setHidden(True)

        self.w_checkbox_completed_researches_movable = QtWidgets.QCheckBox("Movable", self)
        self.w_checkbox_completed_researches_movable.setGeometry(Bartender.GEOMETRY_1_1)
        self.w_checkbox_completed_researches_movable.stateChanged.connect(self.researches_policy)
        self.w_checkbox_completed_researches_movable.setHidden(True)

        self.w_checkbox_completed_researches_times = QtWidgets.QCheckBox("Show Research Times", self)
        self.w_checkbox_completed_researches_times.setGeometry(Bartender.GEOMETRY_1_2)
        self.w_checkbox_completed_researches_times.stateChanged.connect(self.researches_policy)
        self.w_checkbox_completed_researches_times.setHidden(True)

        self.w_checkbox_researches = QtWidgets.QCheckBox("Researching Technologies", self)
        self.w_checkbox_researches.setGeometry(Bartender.GEOMETRY_0_0)
        self.w_checkbox_researches.stateChanged.connect(self.researches_policy)
        self.w_checkbox_researches.setHidden(True)

        self.w_checkbox_researches_movable = QtWidgets.QCheckBox("Movable", self)
        self.w_checkbox_researches_movable.setGeometry(Bartender.GEOMETRY_0_1)
        self.w_checkbox_researches_movable.stateChanged.connect(self.researches_policy)
        self.w_checkbox_researches_movable.setHidden(True)

        self.w_checkbox_researches_show_bars = QtWidgets.QCheckBox("Show Bars", self)
        self.w_checkbox_researches_show_bars.setGeometry(Bartender.GEOMETRY_0_2)
        self.w_checkbox_researches_show_bars.stateChanged.connect(self.researches_policy)
        self.w_checkbox_researches_show_bars.setHidden(True)


        self.w_checkbox_editall = QtWidgets.QCheckBox("All Bars Movable", self)
        self.w_checkbox_editall.setGeometry(Bartender.GEOMETRY_00_3)
        self.w_checkbox_editall.stateChanged.connect(self.moveable)
        self.w_checkbox_editall.setHidden(True)

        # Buttons
        self.w_button_new_header = QtWidgets.QPushButton("New Info Panel", self)
        self.w_button_new_header.setGeometry(Bartender.GEOMETRY_0_3)
        self.w_button_new_header.clicked.connect(self.add_new_header)
        self.w_button_new_header.setHidden(True)

        self.w_button_new_bar = QtWidgets.QPushButton("New Bar", self)
        self.w_button_new_bar.setGeometry(Bartender.GEOMETRY_1_3)
        self.w_button_new_bar.clicked.connect(self.add_new_bar)
        self.w_button_new_bar.setHidden(True)

        # Tab widget
        self.w_tabs_settings = QtWidgets.QTabWidget(self)
        self.w_tabs_settings.setGeometry(Bartender.GEOMETRY_TAB_BAR_SETTINGS)
        self.w_tabs_settings.addTab(InterfaceOffscreenUnits("Offscreen Units", self), f"Offscreen Units")
        self.w_tabs_settings.setHidden(True)
        # hide it all
        self.app = app
        # Consts
        self.overlay = None
        self.game = None
        #self.lobby = Lobby()
        self.state = -1
        self.process_timer = None
        self.timer = None

    def load_settings(self):
        self.info_label.setHidden(True)        

        # Checkboxes
        self.w_checkbox_completed_researches.setHidden(False)
        self.w_checkbox_completed_researches_movable.setHidden(False)
        self.w_checkbox_completed_researches_times.setHidden(False)
        self.w_checkbox_researches.setHidden(False)
        self.w_checkbox_researches_movable.setHidden(False)
        self.w_checkbox_researches_show_bars.setHidden(False)
        self.w_checkbox_editall.setHidden(False)
        # Buttons
        self.w_button_new_header.setHidden(False)
        self.w_button_new_bar.setHidden(False)
        # Tab widget
        self.w_tabs_settings.setHidden(False)
    
        # Load Overlay and UI from settings.txt
        load(self)
        self.start_overlay()
        self.update_overlay_widgets()
        self.researches_policy()
        load_geometry(self)

        self.show()
    
    def researches_policy(self):
        self.w_checkbox_completed_researches_movable.setEnabled(self.w_checkbox_completed_researches.isChecked())
        self.w_checkbox_completed_researches_times.setEnabled(self.w_checkbox_completed_researches.isChecked())
        self.w_checkbox_researches_movable.setEnabled(self.w_checkbox_researches.isChecked())
        self.w_checkbox_researches_show_bars.setEnabled(self.w_checkbox_researches.isChecked())
        if self.overlay is not None:
            self.overlay.research_bars.setHidden(not self.w_checkbox_researches.isChecked())
            self.overlay.research_bars.set_movable(self.w_checkbox_researches_movable.isChecked())
            self.overlay.research_bars.set_magical_bar(self.w_checkbox_researches_show_bars.isChecked())

            self.overlay.research_list.setHidden(not self.w_checkbox_completed_researches.isChecked())
            self.overlay.research_list.set_movable(self.w_checkbox_completed_researches_movable.isChecked())
            self.overlay.research_list.set_magical_timer(self.w_checkbox_completed_researches_times.isChecked())


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
        
    def load_game(self):
        try:
            self.game = Game()
            return True
        except:
            return False
    
                
    def start_overlay(self):
        # Starting overlay UI
        self.overlay = Overlay(self)
        self.researches_policy()
        self.overlay.show()

    def closeEvent(self, event):
        # Closing the window.
        self.print_info("Closing the overlay")
        if SAVE_IF_QUITING_THE_GAME and self.overlay is not None:
            save(self)
        if self.process_timer is not None:
            self.process_timer.stop()
        if self.timer is not None:
            self.timer.stop()
        if self.overlay is not None:
            self.overlay.setHidden(False)
            self.overlay.close()


    def load_lobby(self):
        # Loads lobby data
        try: 
            self.lobby.update()
        except:
            self.lobby = Lobby()
        
    def finite_state_machine(self):
        # State machine.
        if self.state == -1:
            self.print_info("Waiting until the game is started.")
        # Loading the game
        elif self.state == 0:
            if self.load_game() and self.game is not None:
                self.state = 2
                self.lobby = None
                self.print_info("Game loaded. Starting the first iteration.")
        # Getting first iteration
        elif self.state == 2:
            self.game.update()
            if self.game.running:
                self.state = 3
                self.print_info("Starting overlay.")
        # Starting overlay
        elif self.state == 3:
            self.overlay.set_game(self.game)
            self.update_overlay_widgets()
            self.state = 4  
            self.print_info("Waiting until the game is quitted.")
        # Loop
        elif self.state == 4:
            if not self.game.running:
                self.overlay.deleteLater()
                self.overlay = None
                self.state = -1
                

    def run(self):
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.finite_state_machine)
        self.timer.start(Bartender.UPDATE_WINDOW_MS)

    def moveable(self):
        boolean = self.w_checkbox_editall.isChecked()
        if self.overlay is not None:
            self.overlay.set_movable_widgets(boolean)
        
    def add_new_header(self):
        name = f"New Panel"
        widget = InterfaceInfoPanel(name, self)
        self.w_tabs_settings.addTab(widget, name)
        self.update_overlay_widgets()
        self.w_tabs_settings.setCurrentIndex(self.w_tabs_settings.count() - 1)
        
    def add_new_bar(self):
        name = f"New Bar"
        widget = InterfaceBar(name, self)
        self.w_tabs_settings.addTab(widget, name)
        self.update_overlay_widgets()
        self.w_tabs_settings.setCurrentIndex(self.w_tabs_settings.count() - 1)
        
    def update_overlay_widgets(self):
        if self.overlay is None:
            return
        for idx in range(self.w_tabs_settings.count()):
            widget = self.w_tabs_settings.widget(idx)
            self.overlay.create_overlay_widget(widget.BIND_TYPE, widget)



if __name__ == '__main__' or True:
    # Start bartender window.
    app = QtWidgets.QApplication(sys.argv)
    resolution = app.desktop().screenGeometry()
    bartender = Bartender(resolution.width(), resolution.height(), app)
    bartender.load_process()
    if bartender.state == -1:
        sys.exit()
    bartender.run()
    bartender.load_settings()
    result = app.exec_()
    sys.exit(result)
# EOF: bartender.py
