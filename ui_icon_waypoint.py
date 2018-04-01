from PyQt5 import QtCore, QtGui, QtWidgets,  Qt
from aoc_object_building import Building 

from ui_consts import * 

class IconWaypoint(QtWidgets.QWidget):
    """docstring for IconWaypoint"""
    def __init__(self, parent, unit):
        super(IconWaypoint, self).__init__(parent)
        self.unit = unit
        self.setGeometry(0,  0, 42, 42)
        icon_filename = str(self.unit.udata.icon).zfill(3) + ".bmp"
        self.color = self.unit.owner.color.unique
        if type(self.unit) == Building:
            self.icon_path = f"/icons/buildings/{icon_filename}"
        else:
            self.icon_path = f"/icons/units/color_{self.color}/{icon_filename}"
        #print(self.icon_path)

        self.scn = QtWidgets.QGraphicsScene()
        view = QtWidgets.QGraphicsView(self.scn, self)
        view.setStyleSheet("border: 0px; background: transparent")
        view.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        view.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        view.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        view.setGeometry(0, 0, 42,42)
        self.view = view

        stuff = QtGui.QPixmap(ospath + self.icon_path)
        self.scn.addPixmap(stuff).setPos(3,3)
        frame = QtGui.QPixmap(ospath + f"/ui/frame.png")
        self.scn.addPixmap(frame).setPos(0,0)
        self.show()

        self.w = parent.width() -42
        self.h = parent.height() -42
        

    def update_bottom(self, k):
        self.setGeometry(self.w*k, self.h, 42, 42)
        self.show()
    
    def update_right(self, k):
        self.setGeometry(self.w, self.h*k, 42, 42)
        self.show()

    def update_top(self, k):
        self.setGeometry(self.w*k, 0, 42, 42)
        self.show()

    def update_left(self, k):
        self.setGeometry(0, self.h*k, 42, 42)
        self.show()
        
if __name__ == '__main__':
    import bartender