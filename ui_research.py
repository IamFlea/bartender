from time import time

from PyQt5 import QtCore, QtGui, QtWidgets, Qt

from aoc_time import *
from ui_consts import *

adj = 20

#brush.setWidth(2)
class ResearchBar(QtWidgets.QWidget):
    game = None
    """docstring for ResearchBar"""
    def __init__(self, parent, x,y, player, icon, time, totaltime, cooldown):
        super(ResearchBar, self).__init__(parent) 
        self.setGeometry(x, y*42, 150, 42) # 0x0, 42x0, 84x0
        self.player = player
        
        self.scn = QtWidgets.QGraphicsScene()
        self.owner_color = self.player.color.unique
        self.icon = icon 
        self.time = time
        self.totaltime = totaltime
        self.cooldown = cooldown

        self.frame = QtWidgets.QWidget(self)
        self.frame.setGeometry(42+4, 10, 150-42-8, 42-20)
        self.frame.setStyleSheet("background: black")
        
        self.bg = QtWidgets.QWidget(self)
        self.bg.setGeometry(42+6, 11, 150-42-8-2-2, 42-20-2)
        self.bg.setStyleSheet("background: silver")
        self.completed = QtWidgets.QWidget(self)
        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(42+6, 11, 150-42-8-2-2, 42-20-2)
        self.label.setFont(font_idle)
        #self.owner_color = self.player.color.in_game
        
        view = QtWidgets.QGraphicsView(self.scn, self)
        view.setStyleSheet("border: 0px; background: transparent")
        view.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        view.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        view.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        view.setGeometry(0, 0, 42,42)
        self.view = view
        self.scn.addRect
        self.show()


    def update_position(self, x, y):
        self.setGeometry(x*42, y*42, 150,  42)
        self.position = (x*42, y*42)


    def add_icon(self):
        stuff = QtGui.QPixmap(ospath + f"/icons/researches/{str(self.icon).zfill(3)}.bmp")
        self.scn.addPixmap(stuff).setPos(3,3)
        frame = QtGui.QPixmap(ospath + f"/ui/frame{self.owner_color}.png")
        self.scn.addPixmap(frame).setPos(0,0)


    def add_progressbar(self, percentage):
        width = 150-42-8-2-2
        width = int(width * percentage)
        self.completed.setGeometry(42+6, 11, width, 42-20-2)
        self.completed.setStyleSheet("background: grey")

    def update(self, time, totaltime, cooldown):
        self.scn.clear()
        #self.frame.setGeometry(42+4, 4, 150-42-4, 42-4-4)
        
        self.time = time
        self.totaltime = totaltime
        self.cooldown = cooldown
        self.delete = False
        self.shadow = False # Maybe death code
        self.add_icon()
        #self.add_cooldown()
        self.add_progressbar(time/totaltime)
        self.label.setText(str(int(cooldown)))
        


    def add_cooldown(self):
        cooldown = self.cooldown
        text = QtWidgets.QGraphicsSimpleTextItem(str(cooldown))
        font = font_medium if cooldown < 100 else font_small
        text.setFont(font_icon)
        #text.setPen(pen)
        text.setBrush(brush)
        boundingRectangle = text.sceneBoundingRect()
        x, y = 21 - boundingRectangle.width()//2, 12 - boundingRectangle.height()//2  # 21 21 the center
        text.setPos(x, y);
        if not self.shadow: # maybe always true
            self.scn.addRect(3,self.adj + 3,36,36, invisible_pen, idle_time_brush)
        self.shadow = True
        self.scn.addItem(text)



        
if __name__ == '__main__':
    import bartender
    exit(1)