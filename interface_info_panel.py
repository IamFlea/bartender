from collections import defaultdict

from PyQt5 import QtWidgets, QtCore, Qt, QtGui

from aoc_time import *
from aoc_object_consts_unit import UNITS
from interface_utils import *
from interface_consts import *
from ui_info_panel import InfoPanel

from config import *

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


        self.w_checkbox_wood = QtWidgets.QCheckBox("Wood Vills", self)
        self.w_checkbox_wood.setGeometry(GEOMETRY_TOP_2_0)
        self.w_checkbox_wood.stateChanged.connect(self.update_info_panel)
        self.w_checkbox_food = QtWidgets.QCheckBox("Food Vills", self)
        self.w_checkbox_food.setGeometry(GEOMETRY_TOP_2_1)
        self.w_checkbox_food.stateChanged.connect(self.update_info_panel)
        self.w_checkbox_gold = QtWidgets.QCheckBox("Gold Vills", self)
        self.w_checkbox_gold.setGeometry(GEOMETRY_TOP_2_2)
        self.w_checkbox_gold.stateChanged.connect(self.update_info_panel)
        self.w_checkbox_stone = QtWidgets.QCheckBox("Stone Vills", self)
        self.w_checkbox_stone.setGeometry(GEOMETRY_TOP_2_3)
        self.w_checkbox_stone.stateChanged.connect(self.update_info_panel)
        self.w_checkbox_fish = QtWidgets.QCheckBox("Fishing Boats", self)
        self.w_checkbox_fish.setGeometry(GEOMETRY_TOP_2_4)
        self.w_checkbox_fish.stateChanged.connect(self.update_info_panel)
        self.w_checkbox_trade = QtWidgets.QCheckBox("Trade Units", self)
        self.w_checkbox_trade.setGeometry(GEOMETRY_TOP_2_5)
        self.w_checkbox_trade.stateChanged.connect(self.update_info_panel)


        self.w_checkbox_resources = QtWidgets.QCheckBox("# Vills on Resource", self)
        self.w_checkbox_resources.setGeometry(GEOMETRY_TOP_3_2)
        self.w_checkbox_resources.stateChanged.connect(self.update_info_panel)
        self.w_checkbox_resources_carrying = QtWidgets.QCheckBox("Amount of Carrying Res.", self)
        self.w_checkbox_resources_carrying.setGeometry(GEOMETRY_TOP_3_3)
        self.w_checkbox_resources_carrying.stateChanged.connect(self.update_info_panel)

        self.w_checkbox_idle_vills = QtWidgets.QCheckBox("Idle Vills", self)
        self.w_checkbox_idle_vills.setGeometry(GEOMETRY_TOP_5_1)
        self.w_checkbox_idle_vills.stateChanged.connect(self.update_info_panel)
        self.w_checkbox_idle_vills_time = QtWidgets.QCheckBox("Idle Time of Vills", self)
        self.w_checkbox_idle_vills_time.setGeometry(GEOMETRY_TOP_5_2)
        self.w_checkbox_idle_vills_time.stateChanged.connect(self.update_info_panel)


        self.w_checkbox_farm_reseeds = QtWidgets.QCheckBox("Farm Reseeds", self)
        self.w_checkbox_farm_reseeds.setGeometry(GEOMETRY_TOP_5_3)
        self.w_checkbox_farm_reseeds.stateChanged.connect(self.update_info_panel)
        self.w_checkbox_relics = QtWidgets.QCheckBox("Relics", self)
        self.w_checkbox_relics.setGeometry(GEOMETRY_TOP_5_4)
        self.w_checkbox_relics.stateChanged.connect(self.update_info_panel)

        self.w_checkbox_civilians = QtWidgets.QCheckBox("Civilians", self)
        self.w_checkbox_civilians.setGeometry(GEOMETRY_TOP_6_1)
        self.w_checkbox_civilians.stateChanged.connect(self.update_info_panel)
        self.w_checkbox_military = QtWidgets.QCheckBox("Military", self)
        self.w_checkbox_military.setGeometry(GEOMETRY_TOP_6_2)
        self.w_checkbox_military.stateChanged.connect(self.update_info_panel)
        self.w_checkbox_kd_units = QtWidgets.QCheckBox("K/D units", self)
        self.w_checkbox_kd_units.setGeometry(GEOMETRY_TOP_6_3)
        self.w_checkbox_kd_units.stateChanged.connect(self.update_info_panel)
        self.w_checkbox_kd_buildings = QtWidgets.QCheckBox("K/D buildings", self)
        self.w_checkbox_kd_buildings.setGeometry(GEOMETRY_TOP_6_4)
        self.w_checkbox_kd_buildings.stateChanged.connect(self.update_info_panel)



    def remove(self):
        if self.overlay_panel is not None: 
            self.overlay_panel.deleteLater()
        self.deleteLater()
        if self.parent.overlay is not None:
            if self in self.parent.overlay.widgets:
                del self.parent.overlay.widgets[self]

    def set_movable(self):
        if self.overlay_panel is not None:
            self.overlay_panel.set_movable(self.w_checkbox_movable.isChecked())
            self.overlay_panel.raise_()

    def set_hidden(self):
        if self.overlay_panel is not None: 
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

    def update_overlay_widget(self):
        self.overlay_panel.update()

    def settings(self):
        result = []
        # Adds to info panel stuff. 
        count = self.w_checkbox_resources.isChecked()
        amount = self.w_checkbox_resources_carrying.isChecked()
        # pass
        player = self.parent.game.pov
        filter_remove_idle = lambda unit_list: list(filter(lambda unit: not unit.idle, unit_list))
        filter_show_idle = lambda unit_list: list(filter(lambda unit: unit.idle, unit_list))

        #wtf #omg
        def select_function(unit_list):
            get_len = lambda : int_to_str(len(filter_remove_idle(unit_list)))
            get_amount = lambda : int_to_str(sum(map(lambda vill: vill.resource_amount, unit_list)))
            if count and amount:
                f = lambda : get_len() + "; " + get_amount()
            elif count:
                f = lambda : get_len()
            elif amount:
                f = lambda : get_amount()
            return f
        # Adds the functions
        if self.w_checkbox_wood.isChecked() and (count or amount):
            result += [(WOOD, select_function(player.vill_wood))]
        if self.w_checkbox_food.isChecked() and (count or amount):
            result += [(FOOD, select_function(player.vill_food))]
        if self.w_checkbox_gold.isChecked() and (count or amount):
            result += [(GOLD, select_function(player.vill_gold))]
        if self.w_checkbox_stone.isChecked() and (count or amount):
            result += [(STONE, select_function(player.vill_stone))]
        if self.w_checkbox_fish.isChecked() and (count or amount):
            result += [(FISHES, select_function(player.fish))]
        if self.w_checkbox_trade.isChecked() and (count or amount):
            result += [(TRADE, select_function(player.trade))]


        if self.w_checkbox_idle_vills.isChecked() and self.w_checkbox_idle_vills_time.isChecked():
            result += [(IDLE, lambda: int_to_str(len(filter_show_idle(player.civilians))) + " (" + str_idle(sum(map(lambda unit: unit.idle_total_time,  player.civilians))) + ")")]
        elif self.w_checkbox_idle_vills_time.isChecked():
            result += [(IDLE, lambda: str_idle(sum(map(lambda unit: unit.idle_total_time,  player.civilians))))]
        elif self.w_checkbox_idle_vills.isChecked():
            result += [(IDLE, lambda: int_to_str(len(filter_show_idle(player.civilians))))]

        if self.w_checkbox_farm_reseeds.isChecked():
            result += [(FARM_RESEEDS, lambda: int_to_str(player.farm_reseeds))]
        # These values are in double so i need to do: double > int > bartender string conversion
        if self.w_checkbox_relics.isChecked():
            result += [(RELICS, lambda: str(int(player.resources.values[player.resources.keys.index("RelicsCaptured")])))] 
        if self.w_checkbox_civilians.isChecked():
            result += [(CIVILIANS, lambda: int_to_str(len(player.civilians)))]
        if self.w_checkbox_military.isChecked():
            result += [(MILITARY, lambda: int_to_str(len(player.military)))]
        if self.w_checkbox_kd_units.isChecked():
            result += [(KD_RATIO, lambda: int_to_str(int(player.resources.values[player.resources.keys.index("Units Killed")])) + "/" + int_to_str(int(player.resources.values[player.resources.keys.index("Units Lost")])))]
        if self.w_checkbox_kd_buildings.isChecked():
            result += [(KD_RAZINGS_RATIO, lambda: int_to_str(int(player.resources.values[player.resources.keys.index("Razings")])) + "/"+ int_to_str(int(player.resources.values[player.resources.keys.index("Buildings Lost")])) )]
        return result
    def update_info_panel(self):
        # Just update if over_panel is set
        if type(self.overlay_panel) is InfoPanel:
            self.overlay_panel.panel_info_f = self.settings
            # Printing the shown icons
            #print(self.overlay_panel.panel_info_f())
  
if __name__ == '__main__':
    import bartender
        

