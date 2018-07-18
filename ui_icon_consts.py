from PyQt5 import QtCore, QtGui, Qt

ICON_SIZE_PX = 42 # In pixels. with frame. Not a reference to hitchhiker guide to galaxy
ICON_IMG_POS_X = 3
ICON_IMG_POS_Y = 3
ICON_IMG_SIZE_PX = 36 # FRAMELESS

IDLE_COUNTER_WIDTH = 41
IDLE_COUNTER_HEIGHT = 14
SPACE_BETWEEN_COUNTER_AND_ICON = 6

IDLE_COUNTER_HEIGHT_WITH_SPACE = SPACE_BETWEEN_COUNTER_AND_ICON + IDLE_COUNTER_HEIGHT

SPACE_BETWEEN_ICON_AND_BAR = 6
RESEARCH_BAR_WIDTH = 36*2
RESEARCH_BAR_HEIGHT = 20 # shouldnt be greater than ICON_SIZE_PX! 
RESEARCH_BAR_X = ICON_SIZE_PX + SPACE_BETWEEN_ICON_AND_BAR
RESEARCH_BAR_Y = (ICON_SIZE_PX - RESEARCH_BAR_HEIGHT)//2 # Centered


# PyQT stuff

WHITE_BRUSH = Qt.QBrush(Qt.QColor(0xff,0xff,0xff))


icon_top_text_font = QtGui.QFont("Georgia", 12)
icon_top_text_font.setBold(True)

icon_top_text_brush = WHITE_BRUSH

icon_bottom_text_font = QtGui.QFont("Georgia", 12)
icon_bottom_text_font.setBold(True)

icon_bottom_text_brush = WHITE_BRUSH

invisible_pen = Qt.QPen(Qt.QColor(0x00,0x00,0x00, 0x00))
invisible_pen.setWidth(0)

alpha_brush = Qt.QBrush(Qt.QColor(0xff,0xff,0xff,0x80))
alpha_brush.setStyle(QtCore.Qt.Dense3Pattern)

bar_font = QtGui.QFont("Georgia", 8)

idle_counter_text_font = QtGui.QFont("Georgia", 7)
idle_counter_text_brush = WHITE_BRUSH

idle_counter_rect_pen = Qt.QPen()
idle_counter_rect_pen.setWidth(0)

idle_counter_rect_brush = Qt.QBrush(Qt.QColor(0x33,0x33,0x33,0x77))
idle_counter_rect_brush.setStyle(QtCore.Qt.SolidPattern)

idle_counter_blink  =  Qt.QBrush(Qt.QColor(0xff,0xff,0xff,0x80))
idle_counter_blink.setStyle(QtCore.Qt.Dense3Pattern)