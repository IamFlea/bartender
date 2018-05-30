from PyQt5 import QtCore, QtGui, QtWidgets, Qt

class QResizableWidget(QtWidgets.QWidget):
    """docstring for QResizableWidget"""
    GRIP_PX = 10 # Size of grip for resizing these widgets (in pixels)
    EXPAND_LIST = ["→↓", "→↑", "←↓", "←↑", "↓←", "↑←", "↓→", "↑→", ]
    def __init__(self, parent):
        super(QResizableWidget, self).__init__(parent)

        # Creates a movable stuff
        self.drag_widget = QtWidgets.QWidget(self)
        self.drag_widget.setStyleSheet("background-color: rgba(255,180,0,164);")
        self.drag_widget.setVisible(False)
        # Sets grip
        self.grip = QtWidgets.QWidget(self.drag_widget)
        self.grip.setStyleSheet("background-color: rgba(255,255,255,255);")
        self.expand = QtWidgets.QLabel("", self.drag_widget)
        self.expand.setStyleSheet("color: rgba(0,0,0,255); background-color: rgba(0,0,0,0);")
        font = QtGui.QFont(self.expand.font().family(), 20)
        font.setBold(True)
        self.expand.setFont(font)
        #self.expand.setGeometry(5,5,40,20)
        # ??
        self.movable = False
        self.__moving = False
        self.__resizing = False
        self.__offset = QtCore.QPoint()
        self.expand_index = 0 
        self.expand.setText(QResizableWidget.EXPAND_LIST[self.expand_index])

    def setGeometry(self, *arg):
        super(QResizableWidget, self).setGeometry(*arg)
        self.drag_widget.setGeometry(0,0,self.width(), self.height())
        self.grip.setGeometry(self.width() - QResizableWidget.GRIP_PX, self.height() - QResizableWidget.GRIP_PX, QResizableWidget.GRIP_PX, QResizableWidget.GRIP_PX)
        self.expand.setGeometry(self.width()-42, self.height() - self.expand.height()-15, 42, self.expand.height())
        
        
    def mousePressEvent(self, event):
        pos = event.pos()
        if event.buttons() == QtCore.Qt.LeftButton and self.movable\
                    and (pos.x() <= self.width() - QResizableWidget.GRIP_PX \
                    or pos.y() <= self.height() - QResizableWidget.GRIP_PX):
            self.__moving = True
            self.__offset = pos
        elif not (pos.x() <= self.width() - QResizableWidget.GRIP_PX or pos.y() <= self.height() - QResizableWidget.GRIP_PX):
            self.__resizing = True
        if event.buttons() == QtCore.Qt.RightButton:
            print("waat")
            self.expand_index =  (self.expand_index + 1) % len(QResizableWidget.EXPAND_LIST)
            self.expand.setText(QResizableWidget.EXPAND_LIST[self.expand_index])

    

    def drag(self, position):
        # Move with it 
        self.move(self.mapToParent(position - self.__offset))
        # Grab the new stuff
        x, y = self.x(), self.y()
        width, height = self.width(), self.height()
        max_width, max_height = self.parent().width(), self.parent().height()
        # Checking X value
        if x < 0:
            x = 0
        elif x + width >= max_width:
            x = max_width - width
        # Checking Y value
        if y < 0:
            y = 0
        elif y + height >= max_height:
            y = max_height - height
        # Update if the values are wrong
        self.setGeometry(x, y, width, height)

    def resize(self, position):
        # Make it resizable, restric it to GRIP_PX so user won't hide the widget by mistake
        x, y = position.x(), position.y()
        if x < QResizableWidget.GRIP_PX:
            x = QResizableWidget.GRIP_PX
        if y < QResizableWidget.GRIP_PX:
            y = QResizableWidget.GRIP_PX
        self.setGeometry(self.x(), self.y(), x, y)


    def mouseMoveEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            if self.__moving:
                self.drag(event.pos()) # DO NOT USE NAME "self.move" !!!!
            elif self.__resizing:
                self.resize(event.pos())

    
    def mouseReleaseEvent(self, event):
        self.__offset = QtCore.QPoint()
        self.__moving = False
        self.__resizing = False

    def set_movable(self, boolean):
        self.movable = boolean
        self.drag_widget.setVisible(boolean)
        self.drag_widget.raise_()
        
        



        



if __name__ == '__main__':
    import bartender
        
        