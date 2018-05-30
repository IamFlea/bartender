from PyQt5 import QtWidgets, QtCore, Qt, QtGui


class InterfaceHeader(QtWidgets.QWidget):
    """docstring for InterfaceHeader"""
    WIDTH, HEIGHT = 474, 364
    GEOMETRY = Qt.QRect(0,0,WIDTH,HEIGHT)
    SPAN = 10
    WIDE = WIDTH - SPAN*2
    WIDE_HALF = (WIDTH-SPAN*(1+2))/2
    WIDE_FOURTH = (WIDTH-SPAN*(1+4))/4
    WIDE_FIFTH = (WIDTH-SPAN*(1+5))/5

    
    HEIGHT_LABEL = 13
    GEOMETRY_LABEL_NAME = Qt.QRect(SPAN, SPAN, WIDE_FOURTH, HEIGHT_LABEL)
    GEOMETRY_TEXT_NAME = Qt.QRect(GEOMETRY_LABEL_NAME.right()+1 + SPAN, SPAN-3, WIDE_FOURTH, HEIGHT_LABEL+6)
    GEOMETRY_CHECKBOX_MOVABLE = Qt.QRect(GEOMETRY_LABEL_NAME.x(), GEOMETRY_LABEL_NAME.bottom() + 1 + SPAN, WIDE_FOURTH, HEIGHT_LABEL)
    GEOMETRY_CHECKBOX_AGGREGATE = Qt.QRect(GEOMETRY_CHECKBOX_MOVABLE.right() + 1 + SPAN, GEOMETRY_CHECKBOX_MOVABLE.y(), WIDE_FOURTH, HEIGHT_LABEL)
    GEOMETRY_CHECKBOX_IDLE_TIME = Qt.QRect(GEOMETRY_LABEL_NAME.x(), GEOMETRY_CHECKBOX_MOVABLE.bottom() + 1 + SPAN, WIDE_FOURTH, HEIGHT_LABEL)
    GEOMETRY_CHECKBOX_IDLE_BLINK = Qt.QRect(GEOMETRY_CHECKBOX_IDLE_TIME.right() + 1 + SPAN, GEOMETRY_CHECKBOX_IDLE_TIME.y(), WIDE_FOURTH, HEIGHT_LABEL)

    GEOMETRY_LABEL_EXPAND = Qt.QRect(WIDE_HALF+SPAN*2, SPAN, WIDE_FOURTH, HEIGHT_LABEL)
    GEOMETRY_COMBO_EXPAND = Qt.QRect(GEOMETRY_LABEL_EXPAND.right()+1 + SPAN, SPAN-3, WIDE_FOURTH, HEIGHT_LABEL+6)
    GEOMETRY_LABEL_TOP_NUMBER = Qt.QRect(GEOMETRY_LABEL_EXPAND.x(), GEOMETRY_LABEL_EXPAND.bottom()+1 + SPAN, WIDE_FOURTH, HEIGHT_LABEL)
    GEOMETRY_COMBO_TOP_NUMBER = Qt.QRect(GEOMETRY_LABEL_TOP_NUMBER.right()+1 + SPAN, GEOMETRY_LABEL_TOP_NUMBER.y() - 3, WIDE_FOURTH, HEIGHT_LABEL + 6)
    GEOMETRY_LABEL_BOTTOM_NUMBER = Qt.QRect(GEOMETRY_LABEL_EXPAND.x(), GEOMETRY_LABEL_TOP_NUMBER.bottom()+1 + SPAN, WIDE_FOURTH, HEIGHT_LABEL)
    GEOMETRY_COMBO_BOTTOM_NUMBER = Qt.QRect(GEOMETRY_LABEL_BOTTOM_NUMBER.right()+1 + SPAN, GEOMETRY_LABEL_BOTTOM_NUMBER.y() - 3, WIDE_FOURTH, HEIGHT_LABEL + 6)


    COMBO_TOP_BOTTOM_NUMBER_ITEMS = ["None", "Queue", "Remaining Time", "Count", "Selected", "Carrying", "Trained"]

    COMBO_EXPAND_ITEMS = ["Down, Left",
                          "Down, Right",
                          "Left, Up",
                          "Left, Down",
                          "Up, Left",
                          "Up, Right",
                          "Right, Up",
                          "Right, Down"]


    def __init__(self, name, parent):
        super(InterfaceHeader, self).__init__(parent)
        self.parent = parent
        self.setGeometry(InterfaceHeader.GEOMETRY)


        self.w_label_name = QtWidgets.QLabel("Name:", self)
        self.w_label_name.setGeometry(InterfaceHeader.GEOMETRY_LABEL_NAME)

        self.w_text_name = QtWidgets.QLineEdit(name, self)
        self.w_text_name.setGeometry(InterfaceHeader.GEOMETRY_TEXT_NAME)

        self.w_checkbox_movable = QtWidgets.QCheckBox("Movable", self)
        self.w_checkbox_movable.setGeometry(InterfaceHeader.GEOMETRY_CHECKBOX_MOVABLE)
        self.w_checkbox_aggregate = QtWidgets.QCheckBox("Aggregate", self)
        self.w_checkbox_aggregate.setGeometry(InterfaceHeader.GEOMETRY_CHECKBOX_AGGREGATE)
        self.w_checkbox_idle_time = QtWidgets.QCheckBox("Idle time", self)
        self.w_checkbox_idle_time.setGeometry(InterfaceHeader.GEOMETRY_CHECKBOX_IDLE_TIME)
        self.w_checkbox_idle_blink = QtWidgets.QCheckBox("Blink when idle", self)
        self.w_checkbox_idle_blink.setGeometry(InterfaceHeader.GEOMETRY_CHECKBOX_IDLE_BLINK)

        self.w_label_expand = QtWidgets.QLabel("Expand:", self)
        self.w_label_expand.setGeometry(InterfaceHeader.GEOMETRY_LABEL_EXPAND)

        self.w_combo_expand = QtWidgets.QComboBox(self)
        self.w_combo_expand.setGeometry(InterfaceHeader.GEOMETRY_COMBO_EXPAND)
        self.w_combo_expand.addItems(InterfaceHeader.COMBO_EXPAND_ITEMS)

        self.w_label_top_number = QtWidgets.QLabel("Top Number:", self)
        self.w_label_top_number.setGeometry(InterfaceHeader.GEOMETRY_LABEL_TOP_NUMBER)

        self.w_combo_top_number = QtWidgets.QComboBox(self)
        self.w_combo_top_number.setGeometry(InterfaceHeader.GEOMETRY_COMBO_TOP_NUMBER)
        self.w_combo_top_number.addItems(InterfaceHeader.COMBO_TOP_BOTTOM_NUMBER_ITEMS)

        self.w_label_bottom_number = QtWidgets.QLabel("Bottom Number:", self)
        self.w_label_bottom_number.setGeometry(InterfaceHeader.GEOMETRY_LABEL_BOTTOM_NUMBER)

        self.w_combo_bottom_number = QtWidgets.QComboBox(self)
        self.w_combo_bottom_number.setGeometry(InterfaceHeader.GEOMETRY_COMBO_BOTTOM_NUMBER)
        self.w_combo_bottom_number.addItems(InterfaceHeader.COMBO_TOP_BOTTOM_NUMBER_ITEMS)




if __name__ == '__main__':
    import bartender
        

