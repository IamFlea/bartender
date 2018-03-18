from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from aoc_time import *
from time import time

import os
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


class IconArmy(QtWidgets.QWidget):
    """docstring for IconArmy"""
    def __init__(self, parent, x,y, player, units):
        super(IconArmy, self).__init__(parent)
        self.setGeometry(x*42,  y*42, 42, 42)
        self.player = player
        
        self.shadow = False        
        self.scn = QtWidgets.QGraphicsScene()
        self.owner_color = self.player.color.unique
        #self.owner_color = self.player.color.in_game
        
        view = QtWidgets.QGraphicsView(self.scn, self)
        view.setStyleSheet("border: 0px; background: transparent")
        view.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        view.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        view.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        view.setGeometry(0, 0, 42,42)
        self.view = view
        self.icon = units[0].udata.icon
        self.add_icon()
        #self.label1 = QtWidgets.QLabel(self)
        #self.label1.setGeometry(42+3, 3, 42-3, 10)
        #self.label1.setFont(font_idle)
        self.show()

    def update_position(self, x, y):
        self.setGeometry(x*42, y*42, 42, 42)
        self.position = (x*42, y*42)


    def add_icon(self):
        icon_filename = f"unit_{self.icon+1}.png"
        stuff = QtGui.QPixmap(ospath + f"\\icons\\{icon_filename}")
        self.scn.addPixmap(stuff).setPos(3,3)
        frame = QtGui.QPixmap(ospath + f"\\ui\\frame{self.owner_color}.png")
        self.scn.addPixmap(frame).setPos(0,0)

    def add_count(self, length):
        text = QtWidgets.QGraphicsSimpleTextItem(str(length))
        text.setFont(font_icon)
        #text.setPen(pen)
        text.setBrush(brush)
        boundingRectangle = text.sceneBoundingRect()
        x, y = 21 - boundingRectangle.width()//2, 21 - boundingRectangle.height()//2  # 21 21 the center
        text.setPos(x, y);
        self.scn.addRect(3,3,36,36, invisible_pen, idle_time_brush)
        self.shadow = True
        self.scn.addItem(text)



    def update(self, units):
        self.scn.clear()
        self.add_icon()
        self.add_count(len(units))
        
        #self.label1.setText(f"Total: {len(units)}")
        #self.label2.setText(f"HP: {len(units)}")
        #self.label3.setText(f"Attack: {len(units)}")
        #self.label4.setText(f"Armor: {len(units)}")

        pass

if __name__ == '__main__':
    import bartender