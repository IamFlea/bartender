from win32gui import GetWindowText, GetForegroundWindow
from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from keydefaultdict import keydefaultdict

from config import *
from ui_overlay_geometry import OverlayGeometry
from ui_iconlist import IconList

class Overlay(QtWidgets.QMainWindow):
    WINDOW_TITLE = "Bartender Overlay"
    
    WINDOW_FPS = 30 # Frames per second of overlay window
    WINDOW_UPDATE_MS = lambda: int(1000 / Overlay.WINDOW_FPS) 
    WINDOW_GEOMETRY_FPS = 10
    WINDOW_GEOMETRY_UPDATE_MS = lambda: int(1000 / Overlay.WINDOW_GEOMETRY_FPS) 

    def __init__(self, settings, game):
        super(Overlay, self).__init__()
        from ui_icon_old import  IconCooldownCount
        IconCooldownCount.game = game
        self.game = game
        self.settings = settings
        self.widgets = {}
        #IconCooldownCount.game = game
        print("Initing Overlay")
        # Sets windows stuff
        self.setWindowTitle(Overlay.WINDOW_TITLE)
        self.setGeometry(OverlayGeometry())
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground) 
        
        #self.widgets[None] = IconList(self, self.game.player.buildings)
        #print(self.width(), self.height())
        # Updating stuff
        self.update_timer = QtCore.QTimer()
        self.update_timer.timeout.connect(self.update)
        self.update_timer.start(Overlay.WINDOW_UPDATE_MS())

        # Updating window position
        self.geometry_timer = QtCore.QTimer()
        self.geometry_timer.timeout.connect(self.update_geometry)
        self.geometry_timer.start(Overlay.WINDOW_GEOMETRY_UPDATE_MS())
        self.show()
        
    def update(self):
        self.game.update() # Get new data
        for key in self.widgets:
            self.widgets[key].update()

    def create_bar(self, settings):
        if settings not in self.widgets:
            self.widgets[settings] = IconList(self, self.game.player.selected)
            self.widgets[settings].show()

    def update_geometry(self):
        #return
        self.setGeometry(OverlayGeometry())
        if GetWindowText(GetForegroundWindow()) in [AOE_WINDOW_TITLE, Overlay.WINDOW_TITLE, "Bartender"]:
            self.setGeometry(OverlayGeometry())
        else:
            self.setGeometry(0,0,0,0)
    
    def set_movable_widgets(self, boolean):
        for key in self.widgets:
            self.widgets[key].set_movable(boolean)
        self.show()

if __name__ == '__main__':
    import bartender