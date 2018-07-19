from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from config import ospath
from ui_icon_consts import * 
from aoc_time import *


class IconGraphics(QtWidgets.QWidget):
    # Creates an icon with a frame
    def __init__(self, parent, x, y, idle_time = True):
        """
        @param parent  - parent widget
        @param x, y    - position in the grid i.e [0,0] [0,1] .. [1,2].. 

        These must be defined:
            self.frame_color = ""
            self.bottom_text = ""
            self.top_text = ""
            self.idle_time_text = ""
        """
        super(IconGraphics, self).__init__(parent)
        self.parent = parent
        self.y_margin = IDLE_COUNTER_HEIGHT_WITH_SPACE if idle_time else 0
        self.r_margin = 0
        self.set_position(x, y)
        # Creates the scne
        self.scene = QtWidgets.QGraphicsScene()
        # Adds view into the scene 
        self.view = QtWidgets.QGraphicsView(self.scene, self)
        self.view.setStyleSheet("border: 0px; background: transparent")      # Transparent borderless background 
        self.view.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff) # Without scroll bars
        self.view.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.view.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)     # More transparency
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

    
    def set_margin(self, boolean):
        self.y_margin = IDLE_COUNTER_HEIGHT_WITH_SPACE if boolean else 0
        self.set_position(self.x(), self.y())

    def set_right_margin(self, boolean):
        self.r_margin =  RESEARCH_BAR_WIDTH + SPACE_BETWEEN_ICON_AND_BAR if boolean else 0
        self.set_position(self.x(), self.y())

    def set_position(self, x, y):
        self.setGeometry(x * (ICON_SIZE_PX + self.r_margin), y * (ICON_SIZE_PX + self.y_margin), ICON_SIZE_PX + self.r_margin, ICON_SIZE_PX + self.y_margin)
    
    def create_alpha_pixmap(self, pixmap, alpha):
        transparent = QtGui.QPixmap(pixmap.size())
        # Do transparency
        transparent.fill(QtCore.Qt.transparent)
        p = QtGui.QPainter(transparent)
        p.setCompositionMode(QtGui.QPainter.CompositionMode_Source)
        p.drawPixmap(0, 0, pixmap)
        p.setCompositionMode(QtGui.QPainter.CompositionMode_DestinationIn)
        # Set transparency level to `alpha` (possible values are 0-255) The alpha channel of a color specifies the transparency effect, 
        # 0 represents a fully transparent color, while 255 represents a fully opaque color.
        p.fillRect(transparent.rect(), Qt.QColor(0, 0, 0, alpha))
        p.end()
        return transparent

    def show_icon(self, filename, frame_color = ""):
        # Adds the icon into the scene and sets its position to 3 x 3 or 3 x 3+adj
        pixmap = QtGui.QPixmap(ospath + filename)
        #if self.opacity != 255:
        #    pixmap = self.create_alpha_pixmap(pixmap, self.opacity)
        self.scene.addPixmap(pixmap).setPos(ICON_IMG_POS_X, ICON_IMG_POS_Y+ self.y_margin)
        # Adds frame
        frame = f"/ui/frame{frame_color}.png"
        pixmap = QtGui.QPixmap(ospath + frame)
        #if self.opacity != 255:
        #    pixmap = self.create_alpha_pixmap(pixmap, self.opacity)
        self.scene.addPixmap(pixmap).setPos(0, 0+ self.y_margin)

    def show_top_text(self, string):
        if string is None or string == "":
            return
        # Sets the text painter
        text = QtWidgets.QGraphicsSimpleTextItem(string)
        text.setFont(icon_top_text_font)
        text.setBrush(icon_top_text_brush)
        # Sets the position
        boundingRectangle = text.sceneBoundingRect()
        x, y = (ICON_SIZE_PX - boundingRectangle.width())//2, self.y_margin + 12 - boundingRectangle.height()//2  # 21 21 the center
        text.setPos(x, y);
        self.set_shadow()
        self.scene.addItem(text)

    def show_bottom_text(self, string):
        if string is None or string == "":
            return
        # Sets the text painter
        text = QtWidgets.QGraphicsSimpleTextItem(string)
        text.setFont(icon_bottom_text_font)
        text.setBrush(icon_bottom_text_brush)
        # Sets the position
        boundingRectangle = text.sceneBoundingRect()
        x, y = (ICON_SIZE_PX - boundingRectangle.width())//2, self.y_margin + 30 - boundingRectangle.height()//2  # 21 21 the center
        text.setPos(x, y);
        self.set_shadow()
        self.scene.addItem(text)

    def set_shadow(self):
        if not self.b_shadowed:
            self.scene.addRect(ICON_IMG_POS_X, ICON_IMG_POS_Y + self.y_margin, ICON_IMG_SIZE_PX, ICON_IMG_SIZE_PX, invisible_pen, idle_counter_rect_brush)
            self.b_shadowed = True


    def show_idle_time_text(self, string):
        if not self.y_margin:
            return
        # sets the painter
        text = QtWidgets.QGraphicsSimpleTextItem(string)
        text.setFont(idle_counter_text_font)
        text.setBrush(idle_counter_text_brush)
        # Sets position to the center
        br = text.sceneBoundingRect()
        x, y = (IDLE_COUNTER_WIDTH - br.width())//2, (IDLE_COUNTER_HEIGHT - br.height())//2   # 21 21 the center
        text.setPos(x, y)
        # Creates the rectangle
        self.scene.addRect(0, 0, IDLE_COUNTER_WIDTH, IDLE_COUNTER_HEIGHT, idle_counter_rect_pen, idle_counter_rect_brush)
        # Adds the text
        self.scene.addItem(text)

    def blink_effect(self):
        if self.blink:
            self.scene.addRect(3,self.y_margin+3,35,35, idle_counter_rect_pen, idle_counter_blink)

    def redraw(self):
        self.b_shadowed = False
        self.scene.clear()
        self.show_icon(self.icon, self.frame_color)
        self.show_bottom_text(self.bottom_text)
        self.show_top_text(self.top_text)
        self.show_idle_time_text(self.timer_text)
        self.blink_effect()
        #self.view.setForegroundBrush(Qt.QColor(0, 0, 0, self.opacity));
        #print(self.parent.parent())
        self.effect.setOpacity(self.opacity/self.max_opacity)
        

if __name__ == '__main__':
    import bartender