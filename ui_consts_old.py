import os

from PyQt5 import QtCore, QtGui, Qt


AOE_WINDOW_TITLE = "Age of Empires II: HD Edition"

ospath = os.path.dirname(os.path.abspath(__file__))

pen = Qt.QPen(Qt.QColor(0x00,0x00,0x00))
pen.setWidth(1)
pencil = Qt.QPen(Qt.QColor(0x00,0x00,0x00))
pencil.setWidth(1)
brush =  Qt.QBrush(Qt.QColor(0xff,0xff,0xff))
#brush.setWidth(2)
font_name = "Arial Black"
font_big = QtGui.QFont(font_name, 20)
font_big.setBold(True)
font_medium = QtGui.QFont(font_name)
font_medium.setBold(True)
font_small = QtGui.QFont(font_name, 12)
font_small.setBold(True)
font_little = QtGui.QFont(font_name)
font_little.setBold(True)

font_idle = QtGui.QFont("Georgia", 8)

font_icon = QtGui.QFont("Georgia", 12)
font_icon.setBold(True)

idle_pen = Qt.QPen()
idle_pen.setWidth(0)
idle_brush  =  Qt.QBrush(Qt.QColor(0xff,0xff,0xff,0x80))
idle_brush.setStyle(QtCore.Qt.Dense3Pattern)

idle_time_brush = Qt.QBrush(Qt.QColor(0x33,0x33,0x33,0x77))
idle_time_brush.setStyle(QtCore.Qt.SolidPattern)
invisible_pen = Qt.QPen(Qt.QColor(0x00,0x00,0x00, 0x00))
invisible_pen.setWidth(0)


font = QtGui.QFont("Georgia", 8)
font.setBold(True)

