from PyQt5 import QtCore, QtGui, QtWidgets


class QOverlayWidget(QtWidgets.QWidget):
    """docstring for QOverlayWidget"""
    GRIP_PX = 10  # Size of grip for resizing these widgets (in pixels)
    EXPAND_LIST = ["→↓", "→↑", "←↓", "←↑", "↓←", "↑←", "↓→", "↑→", ]

    def __init__(self, name, parent, resizable=True):
        super(QOverlayWidget, self).__init__(parent)
        self.parent = parent
        self.name = name
        # Adds background widget

        # Creates a movable stuff
        self.drag_widget = QtWidgets.QWidget(self)
        self.drag_widget.setStyleSheet("background-color: rgba(255,180,0,164);")
        self.drag_widget.setVisible(False)
        self.label = QtWidgets.QLabel(self.name, self.drag_widget)
        # Sets grip (white area)
        if resizable:
            self.grip = QtWidgets.QWidget(self.drag_widget)
            self.grip.setStyleSheet("background-color: rgba(255,255,255,255);")
        self.expand = QtWidgets.QLabel("", self.drag_widget)
        self.expand.setStyleSheet("color: rgba(0,0,0,255); background-color: rgba(0,0,0,0);")
        font = QtGui.QFont(self.expand.font().family(), 20)
        font.setBold(True)
        self.expand.setFont(font)
        # comment this
        self.movable = False
        self.resizable = resizable
        self.__moving = False
        self.__resizing = False
        self.__offset = QtCore.QPoint()
        self.expand_index = 0
        self.expand.setText(QOverlayWidget.EXPAND_LIST[self.expand_index])

    def setGeometry(self, *arg):
        super(QOverlayWidget, self).setGeometry(*arg)
        self.drag_widget.setGeometry(0, 0, self.width(), self.height())
        if self.resizable:  # and self.icon_list :)
            self.grip.setGeometry(self.width() - QOverlayWidget.GRIP_PX, self.height() - QOverlayWidget.GRIP_PX,
                                  QOverlayWidget.GRIP_PX, QOverlayWidget.GRIP_PX)
        self.expand.setGeometry(self.width() - 42, self.height() - self.expand.height() - 15, 42, self.expand.height())

    def mousePressEvent(self, event):
        pos = event.pos()
        if event.buttons() == QtCore.Qt.LeftButton and self.movable \
                and (pos.x() <= self.width() - QOverlayWidget.GRIP_PX \
                     or pos.y() <= self.height() - QOverlayWidget.GRIP_PX
                     or not self.resizable):
            # Draging // left click on orange area
            self.__moving = True
            self.__offset = pos
        elif not (
                pos.x() <= self.width() - QOverlayWidget.GRIP_PX or pos.y() <= self.height() - QOverlayWidget.GRIP_PX):
            # Resizing // left click on the white area (grip)
            self.__resizing = True
        if event.buttons() == QtCore.Qt.RightButton and self.movable:
            # Changing direction // right click on the whole widget 
            self.expand_index = (self.expand_index + 1) % len(QOverlayWidget.EXPAND_LIST)
            self.expand.setText(QOverlayWidget.EXPAND_LIST[self.expand_index])

    def set_expand_index(self, index):
        self.expand_index = index
        self.expand.setText(QOverlayWidget.EXPAND_LIST[self.expand_index])

    def drag(self, position):
        # Move with it 
        self.move(self.mapToParent(position - self.__offset))
        # Grab the new stuff
        x, y = self.x(), self.y()
        width, height = self.width(), self.height()
        max_width, max_height = self.parent.width(), self.parent.height()
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
        if x < QOverlayWidget.GRIP_PX:
            x = QOverlayWidget.GRIP_PX
        if y < QOverlayWidget.GRIP_PX:
            y = QOverlayWidget.GRIP_PX
        self.setGeometry(self.x(), self.y(), x, y)

    def mouseMoveEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            if self.__moving:
                self.drag(event.pos())  # DO NOT USE NAME "self.move" !!!!
            elif self.__resizing:
                self.resize(event.pos())

    def mouseReleaseEvent(self, event):
        self.__offset = QtCore.QPoint()
        self.__moving = False
        self.__resizing = False

    def set_movable(self, boolean):
        self.raise_()
        self.movable = boolean
        self.drag_widget.setVisible(boolean)
        self.drag_widget.raise_()


if __name__ == '__main__':
    pass
