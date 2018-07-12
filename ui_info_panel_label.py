from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from config import * 

font = QtGui.QFont("Georgia", 8)
brush = Qt.QBrush(Qt.QColor(0xff,0xff,0xff))

class PanelLabel(QtWidgets.QWidget):
    """docstring for PanelLabel"""
    def __init__(self, parent, name):
        super(PanelLabel, self).__init__(parent)
        self.parent = parent
        #self.set_position(x, y)
        # Creates the scne
        self.scene = QtWidgets.QGraphicsScene()
        # Adds view into the scene 
        self.view = QtWidgets.QGraphicsView(self.scene, self)
        self.view.setStyleSheet("border: 0px;")      # Borderless background 
        self.view.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff) # Without scroll bars
        self.view.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.view.setGeometry(0, 0, self.width(), self.height())      # Sets the geometry
        # For not shadowing it two times
        self.b_shadowed = False
        self.blink = False
        self.opacity = 255
        self.max_opacity = 256
        self.effect = QtWidgets.QGraphicsOpacityEffect(self);
        self.effect.setOpacity(self.opacity/self.max_opacity)
        self.setGraphicsEffect(self.effect)
        # Shows it
        self.show()
        self.icon = name
        self.text = ""

    def set_position(self, x):
        self.setGeometry(x, 0, self.width(), self.height())
        
    def show_text(self, string):
        if string is None or string == "":
            return
        # Creats Text item
        text = QtWidgets.QGraphicsSimpleTextItem(string)
        text.setFont(font)
        text.setBrush(brush)
        # Sets the position
        boundingRectangle = text.sceneBoundingRect()
        x, y = (self.width() - boundingRectangle.width() - 3), (self.height() - boundingRectangle.height() - 2)//2   # 21 21 the center
        text.setPos(x, y);
        self.scene.addItem(text)

    def show_icon(self, icon_filename):
        filename = PATH_PANEL_ICONS + icon_filename
        # Creates the label with icon
        pixmap = QtGui.QPixmap(ospath + filename)
        # Refresh width and height
        self.setGeometry(self.x(), self.y(), pixmap.width(), pixmap.height())
        self.view.setGeometry(0, 0, self.width(), self.height())
        # Adds the label with icon into scene
        self.scene.addPixmap(pixmap).setPos(0,0)

    def redraw(self):
        self.scene.clear()
        self.show_icon(self.icon)
        self.show_text(self.text)
        #print(self.text)
        

        

if __name__ == '__main__':
    import bartender
        
        