from PyQt5 import QtCore, QtGui, QtWidgets,  Qt
from aoc_time import *
from time import time

import os
ospath = os.path.dirname(os.path.abspath(__file__))

#brush.setWidth(2)
class IconResearch(QtWidgets.QWidget):
    game = None
    """docstring for IconResearch"""
    def __init__(self, parent, x,y, player, icon, time):
        super(IconResearch, self).__init__(parent) 
        self.setGeometry(x, y, 42, 42)
        self.player = player
        
        self.scn = QtWidgets.QGraphicsScene()
        self.owner_color = self.player.color.unique
        self.icon = icon 
        self.time = time
        #self.owner_color = self.player.color.in_game
        
        view = QtWidgets.QGraphicsView(self.scn, self)
        view.setStyleSheet("border: 0px; background: transparent")
        view.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        view.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        view.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        view.setGeometry(0, 0, 42,42)
        self.view = view
        self.add_icon()
        self.show()

    def add_icon(self):
        stuff = QtGui.QPixmap(ospath + f"/icons/researches/{str(self.icon).zfill(3)}.bmp")
        self.scn.addPixmap(stuff).setPos(3,3)
        frame = QtGui.QPixmap(ospath + f"/ui/frame{self.owner_color}.png")
        self.scn.addPixmap(frame).setPos(0,0)

    def update(self):
        pass

if __name__ == '__main__':
    import bartender
    exit(1)

