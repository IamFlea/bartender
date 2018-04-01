from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from aoc_time import *
from time import time

from ui_consts import *

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
        self.icon = str(units[0].udata.icon).zfill(3)
        self.add_icon(False)
        #self.label1 = QtWidgets.QLabel(self)
        #self.label1.setGeometry(42+3, 3, 42-3, 10)
        #self.label1.setFont(font_idle)
        self.show()

    def update_position(self, x, y):
        self.setGeometry(x*42, y*42, 42, 42)
        self.position = (x*42, y*42)


    def add_icon(self, selection):
        icon = QtGui.QPixmap(ospath + f"\\icons\\units\\color_{self.player.color.unique}\\{self.icon}.bmp")
        self.scn.addPixmap(icon).setPos(3,3)
        if selection:
            frame = QtGui.QPixmap(ospath + f"\\ui\\frame{self.owner_color}.png")
        else:
            frame = QtGui.QPixmap(ospath + f"\\ui\\frame.png")
        self.scn.addPixmap(frame).setPos(0,0)

    def add_count(self, length, adj_top=21):
        text = QtWidgets.QGraphicsSimpleTextItem(str(length))
        text.setFont(font_icon)
        #text.setPen(pen)
        text.setBrush(brush)
        boundingRectangle = text.sceneBoundingRect()
        x, y = 21 - boundingRectangle.width()//2, adj_top - boundingRectangle.height()//2  # 21 21 the center
        text.setPos(x, y);
        self.scn.addRect(3,3,36,36, invisible_pen, idle_time_brush)
        self.shadow = True
        self.scn.addItem(text)



    def update(self, units):
        self.scn.clear()
        selected_units = list(filter(lambda u, x=self.player.selected: u in x, units))
        selection = len(selected_units) > 0 # At least one is selected
        #selection = len(units) == len(selected_units) # All units are selected
        self.add_icon(selection)
        if selected_units:
            self.add_count(len(selected_units), adj_top=12)
            self.add_count(len(units), adj_top=30)
        else:
            self.add_count(len(units))
        
        #self.label1.setText(f"Total: {len(units)}")
        #self.label2.setText(f"HP: {len(units)}")
        #self.label3.setText(f"Attack: {len(units)}")
        #self.label4.setText(f"Armor: {len(units)}")

        pass

if __name__ == '__main__':
    import bartender