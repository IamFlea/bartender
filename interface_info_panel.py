from collections import defaultdict

from PyQt5 import QtWidgets, QtCore, Qt, QtGui

from aoc_time import *
from aoc_object_consts_unit import UNITS
from interface_bar_utils import *
from interface_consts import *
from ui_info_panel import InfoPanel

class InterfaceInfoPanel(QtWidgets.QWidget):
    """docstring for InterfaceInfoPanel"""
    BIND_TYPE = InfoPanel


    def __init__(self, name, parent):
        super(InterfaceInfoPanel, self).__init__(parent)
        self.parent = parent
        self.overlay_panel = None
        self.setGeometry(GEOMETRY)


        self.w_label_name = QtWidgets.QLabel("Name:", self)
        self.w_label_name.setGeometry(GEOMETRY_TOP_0_1)
        self.w_text_name = QtWidgets.QLineEdit(name, self)
        self.w_text_name.setGeometry(GEOMETRY_TOP_0_2)
        self.w_text_name.textChanged.connect(self.rename_tab)


        self.w_checkbox_hidden = QtWidgets.QCheckBox("Hidden", self)
        self.w_checkbox_hidden.setGeometry(GEOMETRY_TOP_0_3)
        self.w_checkbox_hidden.stateChanged.connect(self.set_hidden)

        self.w_checkbox_movable = QtWidgets.QCheckBox("Movable", self)
        self.w_checkbox_movable.setGeometry(GEOMETRY_TOP_0_4)
        self.w_checkbox_movable.stateChanged.connect(self.set_movable)

        self.w_button_remove = QtWidgets.QPushButton("Remove", self)
        self.w_button_remove.setGeometry(GEOMETRY_REMOVE_BUTTON)
        self.w_button_remove.clicked.connect(self.remove)

        self.w_checkbox_resources = QtWidgets.QCheckBox("Vills Resources", self)
        self.w_checkbox_resources.setGeometry(GEOMETRY_TOP_2_0)
        self.w_checkbox_resources_carrying = QtWidgets.QCheckBox("Vills R. Carrying", self)
        self.w_checkbox_resources_carrying.setGeometry(GEOMETRY_TOP_2_1)
        self.w_checkbox_idle_vills = QtWidgets.QCheckBox("Idle Vills", self)
        self.w_checkbox_idle_vills.setGeometry(GEOMETRY_TOP_2_2)
        self.w_checkbox_idle_vills_time = QtWidgets.QCheckBox("Idle Time of Vills", self)
        self.w_checkbox_idle_vills_time.setGeometry(GEOMETRY_TOP_2_3)
        self.w_checkbox_farm_reseeds = QtWidgets.QCheckBox("Farm Reseeds", self)
        self.w_checkbox_farm_reseeds.setGeometry(GEOMETRY_TOP_2_4)
        self.w_checkbox_relics = QtWidgets.QCheckBox("Relics", self)
        self.w_checkbox_relics.setGeometry(GEOMETRY_TOP_2_5)

        self.w_checkbox_civilians = QtWidgets.QCheckBox("Civilians", self)
        self.w_checkbox_civilians.setGeometry(GEOMETRY_TOP_3_1)
        self.w_checkbox_military = QtWidgets.QCheckBox("Military", self)
        self.w_checkbox_military.setGeometry(GEOMETRY_TOP_3_2)
        self.w_checkbox_kd_units = QtWidgets.QCheckBox("K/D units", self)
        self.w_checkbox_kd_units.setGeometry(GEOMETRY_TOP_3_3)
        self.w_checkbox_kd_buildings = QtWidgets.QCheckBox("K/D buildings", self)
        self.w_checkbox_kd_buildings.setGeometry(GEOMETRY_TOP_3_4)



    def remove(self):
        if self.overlay_panel is not None: 
            self.overlay_panel.deleteLater()
        self.deleteLater()

    def set_movable(self):
        if self.overlay_panel is not None:
            self.overlay_panel.set_movable(self.w_checkbox_movable.isChecked())
            self.overlay_panel.raise_()

    def set_hidden(self):
        if self.overlay_panel is None: 
            if self.w_checkbox_hidden.isChecked():
                self.overlay_panel.setVisible(False)
            else:
                self.overlay_panel.setVisible(True)

    def rename_tab(self):
        for index in range(self.parent.w_tabs_settings.count()):
            if self == self.parent.w_tabs_settings.widget(index):
                self.parent.w_tabs_settings.setTabText(index, self.w_text_name.text())

    def bind_widget(self, widget):
        self.overlay_panel = widget

if __name__ == '__main__':
    import bartender
        

