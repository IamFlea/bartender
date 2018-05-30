from PyQt5 import Qt
from win32gui import GetWindowRect, EnumWindows, GetWindowText
from config import *

class OverlayGeometry(object):
    WINDOW_FRAME_MARGIN = [8, 30, 16, 38] # LEFT, TOP, RIGHT, BOT
        
    def get_aoe_window_geometry():
        # Getting aoe window location and resolution
        global geometry
        geometry = None
        def function(hwnd, extra):
            global geometry
            if AOE_WINDOW_TITLE != GetWindowText(hwnd):
                return
            rect = GetWindowRect(hwnd)
            geometry = Qt.QRect(rect[0], rect[1], rect[2] - rect[0], rect[3] - rect[1])
        EnumWindows(function, None) # Previous values are filled with this
        return geometry
    
    def __new__(cls):
        geometry = OverlayGeometry.get_aoe_window_geometry()
        if geometry.x() > 0 or geometry.y() > 0:
            return Qt.QRect(geometry.x() + OverlayGeometry.WINDOW_FRAME_MARGIN[0], 
                            geometry.y() + OverlayGeometry.WINDOW_FRAME_MARGIN[1], 
                            geometry.width() - OverlayGeometry.WINDOW_FRAME_MARGIN[2], 
                            geometry.height() - OverlayGeometry.WINDOW_FRAME_MARGIN[3])
        else:
            return geometry
    