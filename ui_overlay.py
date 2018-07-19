from win32gui import GetWindowText, GetForegroundWindow
from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from keydefaultdict import keydefaultdict

from config import *
from ui_overlay_geometry import OverlayGeometry
from ui_iconlist import IconList
from ui_info_panel import InfoPanel
from ui_research_bars import ResearchBars 
from ui_research_list import ResearchList
from interface_bar import InterfaceBar
from interface_info_panel import InterfaceInfoPanel
class Overlay(QtWidgets.QMainWindow):
    WINDOW_TITLE = "Bartender Overlay"
    
    WINDOW_FPS = 30 # Frames per second of overlay window
    WINDOW_UPDATE_MS = lambda: int(1000 / Overlay.WINDOW_FPS) 
    WINDOW_GEOMETRY_FPS = 10
    WINDOW_GEOMETRY_UPDATE_MS = lambda: int(1000 / Overlay.WINDOW_GEOMETRY_FPS) 

    def __init__(self, settings, game):
        super(Overlay, self).__init__()
        self.game = game
        self.settings = settings
        self.widgets = {}
        self.research_bars = ResearchBars(self)
        self.research_list = ResearchList(self)
        #IconCooldownCount.game = game
        #print("Initing Overlay")
        # Sets windows stuff
        self.setWindowTitle(Overlay.WINDOW_TITLE)
        self.setGeometry(OverlayGeometry())
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground) 
        self.prev_window_size = self.width(), self.height()

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
        for idx in range(self.settings.w_tabs_settings.count()):
            interface_widget = self.settings.w_tabs_settings.widget(idx)
            interface_widget.update_overlay_widget()
        self.research_bars.update()
        self.research_list.update()
        

    def create_overlay_widget(self, widget_type, settings):
        if settings not in self.widgets:
            self.widgets[settings] = widget_type(self)
            settings.bind_widget(self.widgets[settings])
            self.widgets[settings].show()
    
    def update_geometry_of_widgets(self, shift_width, shift_height):
        for idx in range(1, self.settings.w_tabs_settings.count()):
            widget = self.widgets[self.settings.w_tabs_settings.widget(idx)]
            right = widget.x() + widget.width()
            bottom = widget.y() + widget.height()
            if right > self.width():
                widget.setGeometry(widget.x() + shift_width, widget.y(), widget.width(), widget.height())
            if bottom > self.height():
                widget.setGeometry(widget.x(), widget.y() + shift_height, widget.width(), widget.height())
 
    def update_geometry(self):
        #return
        self.setGeometry(OverlayGeometry())

        # Check the widgets on overlay
        if self.prev_window_size[0] != self.width() or self.prev_window_size[1] != self.height():
            shift_width = self.width() - self.prev_window_size[0]
            shift_height = self.height() - self.prev_window_size[1]
            if shift_height < 0 or shift_width < 0:
                # Need to move the widgets on overlay, so they can be on the screen
                self.update_geometry_of_widgets(shift_width, shift_height)

            self.prev_window_size = self.width(), self.height()

        if GetWindowText(GetForegroundWindow()) in [AOE_WINDOW_TITLE, Overlay.WINDOW_TITLE, "Bartender"]:
            self.setHidden(False)
        else:
            self.setHidden(True)
    
    def set_movable_widgets(self, boolean):
        for key in self.widgets:
            self.widgets[key].set_movable(boolean)
        self.set_movable_research_bars(boolean)
        #self.set_movable_research_list(boolean)
        self.show()

    def set_movable_research_bars(self, boolean):
        self.research_bars.set_movable(boolean)
        self.show()

    def set_movable_research_list(self, boolean):
        self.research_list.set_movable(boolean)
        self.show()

if __name__ == '__main__':
    import bartender