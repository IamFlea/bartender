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

adj = 20
class IconCooldownCount(QtWidgets.QWidget):
    game = None
    """docstring for IconCooldownCount"""
    def __init__(self, parent, x, y, obj, show_idle=True):
        super(IconCooldownCount, self).__init__(parent) 
        self.adj = adj if show_idle else 0
        self.show_idle = show_idle
        self.setGeometry(x*42,  y*42, 42, self.adj + 42)
        self.position = (x*42, y*42)
        #print(self.position)
        self.delete = False
        self.object = obj
        self.scn = QtWidgets.QGraphicsScene()
        #self.owner_color = self.object.owner.color.unique
        self.owner_color = self.object.owner.color.in_game
        view = QtWidgets.QGraphicsView(self.scn, self)
        view.setStyleSheet("border: 0px; background: transparent")
        view.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        view.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        view.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        view.setGeometry(0, 0, 42, self.adj +42)
        self.view = view
    
        self.show()


    def update_position(self, x, y):
        self.setGeometry(x*42, y*42, 42, self.adj + 42)
        self.position = (x*42, y*42)
    
    def add_idle_time(self):
        text = QtWidgets.QGraphicsSimpleTextItem(str_idle(self.object.idle_total_time))
        text.setFont(font_idle)
        text.setBrush(brush)
        br = text.sceneBoundingRect()
        self.scn.addRect(0,0,41,14, idle_pen, idle_time_brush)
        x, y = 21 - br.width()//2, 7 - br.height()//2  # 21 21 the center
        text.setPos(x, y);
        
        #print(br.width, br.height)

        self.scn.addItem(text)

    def select_icon(self):
        icon_filename = f"building_{self.object.udata.icon+1}.png"
        if self.object.research:
            icon_filename = f"tech_{self.object.research.icon+1}.png"
        elif self.object.queue:
            icon_filename = f"unit_{self.object.queue[0][1]+1}.png"
        return icon_filename

    def get_cooldown(self):
        cooldown = self.object.construction # None if standing
        if self.object.training:
            cooldown = self.object.training.cooldown
        elif self.object.research:
            cooldown = self.object.research.cooldown
        return cooldown

    def get_queue(self):
        result = None
        if self.object.queue:
            result = self.object.queue.length
        return result

    def add_idle(self, show_idle):
        if show_idle and self.object.idle and int(time())%2 and self.object.idle_time < 60000:
            self.scn.addRect(3,self.adj+3,35,35, idle_pen, idle_brush)
        
    def add_icon(self, show_idle=False):
        icon_filename = self.select_icon()
        stuff = QtGui.QPixmap(ospath + f"\\icons\\{icon_filename}")
        self.scn.addPixmap(stuff).setPos(3,self.adj+3)
        self.add_idle(show_idle)
        if self.object.ptr in IconCooldownCount.game.player.selected:
            frame = QtGui.QPixmap(ospath + f"\\ui\\frame.png")
        else:
            frame = QtGui.QPixmap(ospath + f"\\ui\\frame{self.owner_color}.png")
        self.scn.addPixmap(frame).setPos(0,self.adj+0)

    def add_cooldown(self):
        cooldown = self.get_cooldown()
        if cooldown is None:
            return
        text = QtWidgets.QGraphicsSimpleTextItem(str(cooldown))
        font = font_medium if cooldown < 100 else font_small
        text.setFont(font_icon)
        #text.setPen(pen)
        text.setBrush(brush)
        boundingRectangle = text.sceneBoundingRect()
        x, y = 21 - boundingRectangle.width()//2, self.adj+12 - boundingRectangle.height()//2  # 21 21 the center
        text.setPos(x, y);
        if not self.shadow:
            self.scn.addRect(3,self.adj + 3,36,36, invisible_pen, idle_time_brush)
        self.shadow = True
        self.scn.addItem(text)

    def add_queue(self):
        queue = self.get_queue()
        if queue is None:
            return
        text = QtWidgets.QGraphicsSimpleTextItem(str(queue))
        font = font_medium if queue < 100 else font_small
        text.setFont(font_icon)
        #text.setPen(pen)
        text.setBrush(brush)
        boundingRectangle = text.sceneBoundingRect()
        x, y = 21 - boundingRectangle.width()//2, self.adj+30 - boundingRectangle.height()//2  # 21 21 the center
        text.setPos(x, y);
        if not self.shadow:
            self.scn.addRect(3,self.adj + 3,36,36, invisible_pen, idle_time_brush)
        self.shadow = True
        self.scn.addItem(text)

    def update_building(self):
        # removes stuff# Adds icon
        self.scn.clear()
        self.delete = False
        self.shadow = False
        self.add_icon(show_idle=self.show_idle)
        self.add_cooldown()
        self.add_queue()
        if self.show_idle:
            self.add_idle_time()
        #self.show()

if __name__ == '__main__':
    import bartender
    exit(1)