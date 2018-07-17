from collections import defaultdict
from PyQt5 import QtWidgets, QtCore, Qt, QtGui

from interface_utils import *
from interface_consts import *
from ui_offscreen_units import OverlayOffscreenUnits

from config import *
from aoc_object_consts import ClassData
class InterfaceOffscreenUnits(QtWidgets.QWidget):
    """docstring for InterfaceOffscreenUnits"""
    BIND_TYPE = OverlayOffscreenUnits

    def __init__(self, name, parent):
        super(InterfaceOffscreenUnits, self).__init__(parent)
        self.name = name
        self.parent = parent
        self.widget = None


        self.w_label_name = QtWidgets.QLabel("Name:", self)
        self.w_label_name.setGeometry(GEOMETRY_TOP_0_1)
        self.w_text_name = QtWidgets.QLineEdit(name, self)
        self.w_text_name.setGeometry(GEOMETRY_TOP_0_2)
        self.w_text_name.textChanged.connect(self.rename_tab)


        self.w_checkbox_hidden = QtWidgets.QCheckBox("Hidden", self)
        self.w_checkbox_hidden.setGeometry(GEOMETRY_TOP_0_3)
        self.w_checkbox_hidden.stateChanged.connect(self.set_hidden)


        self.w_checkbox_selected = QtWidgets.QCheckBox("Selected Units", self)
        self.w_checkbox_selected.setGeometry(GEOMETRY_TOP_2_0)
        self.w_checkbox_selected.stateChanged.connect(self.update)
        self.w_checkbox_selected_policy = QtWidgets.QCheckBox("Not Idle", self)
        self.w_checkbox_selected_policy.setGeometry(GEOMETRY_TOP_2_1)
        self.w_checkbox_selected_policy.setTristate()
        self.w_checkbox_selected_policy.stateChanged.connect(self.update)
        self.w_label_selected_min = QtWidgets.QLabel("Minimal time:", self)
        self.w_label_selected_min.setGeometry(GEOMETRY_TOP_2_2)
        self.w_text_selected_min = QtWidgets.QSpinBox(self)
        self.w_text_selected_min.setGeometry(GEOMETRY_TOP_2_3)
        self.w_text_selected_min.setMaximum(99999)
        self.w_text_selected_min.setSuffix(" seconds")
        self.w_label_selected_max = QtWidgets.QLabel("Maximal time:", self)
        self.w_label_selected_max.setGeometry(GEOMETRY_TOP_2_4)
        self.w_text_selected_max = QtWidgets.QSpinBox(self)
        self.w_text_selected_max.setGeometry(GEOMETRY_TOP_2_5)
        self.w_text_selected_max.setMaximum(99999)
        self.w_text_selected_max.setSuffix(" seconds")
        self.w_text_selected_max.setValue(self.w_text_selected_max.maximum())

        self.w_checkbox_monks_relic = QtWidgets.QCheckBox("Monks with Relic", self)
        self.w_checkbox_monks_relic.setGeometry(GEOMETRY_TOP_3_0)
        self.w_checkbox_monks_relic.stateChanged.connect(self.update)
        self.w_checkbox_monks_relic_policy = QtWidgets.QCheckBox("Not Idle", self)
        self.w_checkbox_monks_relic_policy.setGeometry(GEOMETRY_TOP_3_1)
        self.w_checkbox_monks_relic_policy.setTristate()
        self.w_checkbox_monks_relic_policy.stateChanged.connect(self.update)
        self.w_label_monks_relic_min = QtWidgets.QLabel("Minimal time:", self)
        self.w_label_monks_relic_min.setGeometry(GEOMETRY_TOP_3_2)
        self.w_text_monks_relic_min = QtWidgets.QSpinBox(self)
        self.w_text_monks_relic_min.setGeometry(GEOMETRY_TOP_3_3)
        self.w_text_monks_relic_min.setMaximum(99999)
        self.w_text_monks_relic_min.setSuffix(" seconds")
        self.w_label_monks_relic_max = QtWidgets.QLabel("Maximal time:", self)
        self.w_label_monks_relic_max.setGeometry(GEOMETRY_TOP_3_4)
        self.w_text_monks_relic_max = QtWidgets.QSpinBox(self)
        self.w_text_monks_relic_max.setGeometry(GEOMETRY_TOP_3_5)
        self.w_text_monks_relic_max.setMaximum(99999)
        self.w_text_monks_relic_max.setSuffix(" seconds")
        self.w_text_monks_relic_max.setValue(self.w_text_monks_relic_max.maximum())        

        self.w_checkbox_group1 = QtWidgets.QCheckBox("Group 1", self)
        self.w_checkbox_group1.setGeometry(GEOMETRY_TOP_4_0)
        self.w_checkbox_group1.stateChanged.connect(self.update)
        self.w_checkbox_group1_policy = QtWidgets.QCheckBox("Not Idle", self)
        self.w_checkbox_group1_policy.setGeometry(GEOMETRY_TOP_4_1)
        self.w_checkbox_group1_policy.setTristate()
        self.w_checkbox_group1_policy.stateChanged.connect(self.update)
        self.w_label_group1_min = QtWidgets.QLabel("Minimal time:", self)
        self.w_label_group1_min.setGeometry(GEOMETRY_TOP_4_2)
        self.w_text_group1_min = QtWidgets.QSpinBox(self)
        self.w_text_group1_min.setGeometry(GEOMETRY_TOP_4_3)
        self.w_text_group1_min.setMaximum(99999)
        self.w_text_group1_min.setSuffix(" seconds")
        self.w_label_group1_max = QtWidgets.QLabel("Maximal time:", self)
        self.w_label_group1_max.setGeometry(GEOMETRY_TOP_4_4)
        self.w_text_group1_max = QtWidgets.QSpinBox(self)
        self.w_text_group1_max.setGeometry(GEOMETRY_TOP_4_5)
        self.w_text_group1_max.setMaximum(99999)
        self.w_text_group1_max.setSuffix(" seconds")
        self.w_text_group1_max.setValue(self.w_text_group1_max.maximum())        


        self.w_checkbox_group2 = QtWidgets.QCheckBox("Group 2", self)
        self.w_checkbox_group2.setGeometry(GEOMETRY_TOP_5_0)
        self.w_checkbox_group2.stateChanged.connect(self.update)
        self.w_checkbox_group2_policy = QtWidgets.QCheckBox("Not Idle", self)
        self.w_checkbox_group2_policy.setGeometry(GEOMETRY_TOP_5_1)
        self.w_checkbox_group2_policy.setTristate()
        self.w_checkbox_group2_policy.stateChanged.connect(self.update)
        self.w_label_group2_min = QtWidgets.QLabel("Minimal time:", self)
        self.w_label_group2_min.setGeometry(GEOMETRY_TOP_5_2)
        self.w_text_group2_min = QtWidgets.QSpinBox(self)
        self.w_text_group2_min.setGeometry(GEOMETRY_TOP_5_3)
        self.w_text_group2_min.setMaximum(99999)
        self.w_text_group2_min.setSuffix(" seconds")
        self.w_label_group2_max = QtWidgets.QLabel("Maximal time:", self)
        self.w_label_group2_max.setGeometry(GEOMETRY_TOP_5_4)
        self.w_text_group2_max = QtWidgets.QSpinBox(self)
        self.w_text_group2_max.setGeometry(GEOMETRY_TOP_5_5)
        self.w_text_group2_max.setMaximum(99999)
        self.w_text_group2_max.setSuffix(" seconds")
        self.w_text_group2_max.setValue(self.w_text_group2_max.maximum())        


        self.w_checkbox_group3 = QtWidgets.QCheckBox("Group 3", self)
        self.w_checkbox_group3.setGeometry(GEOMETRY_TOP_6_0)
        self.w_checkbox_group3.stateChanged.connect(self.update)
        self.w_checkbox_group3_policy = QtWidgets.QCheckBox("Not Idle", self)
        self.w_checkbox_group3_policy.setGeometry(GEOMETRY_TOP_6_1)
        self.w_checkbox_group3_policy.setTristate()
        self.w_checkbox_group3_policy.stateChanged.connect(self.update)
        self.w_label_group3_min = QtWidgets.QLabel("Minimal time:", self)
        self.w_label_group3_min.setGeometry(GEOMETRY_TOP_6_2)
        self.w_text_group3_min = QtWidgets.QSpinBox(self)
        self.w_text_group3_min.setGeometry(GEOMETRY_TOP_6_3)
        self.w_text_group3_min.setMaximum(99999)
        self.w_text_group3_min.setSuffix(" seconds")
        self.w_label_group3_max = QtWidgets.QLabel("Maximal time:", self)
        self.w_label_group3_max.setGeometry(GEOMETRY_TOP_6_4)
        self.w_text_group3_max = QtWidgets.QSpinBox(self)
        self.w_text_group3_max.setGeometry(GEOMETRY_TOP_6_5)
        self.w_text_group3_max.setMaximum(99999)
        self.w_text_group3_max.setSuffix(" seconds")
        self.w_text_group3_max.setValue(self.w_text_group3_max.maximum())        


        self.w_checkbox_group4 = QtWidgets.QCheckBox("Group 4", self)
        self.w_checkbox_group4.setGeometry(GEOMETRY_TOP_7_0)
        self.w_checkbox_group4.stateChanged.connect(self.update)
        self.w_checkbox_group4_policy = QtWidgets.QCheckBox("Not Idle", self)
        self.w_checkbox_group4_policy.setGeometry(GEOMETRY_TOP_7_1)
        self.w_checkbox_group4_policy.setTristate()
        self.w_checkbox_group4_policy.stateChanged.connect(self.update)
        self.w_label_group4_min = QtWidgets.QLabel("Minimal time:", self)
        self.w_label_group4_min.setGeometry(GEOMETRY_TOP_7_2)
        self.w_text_group4_min = QtWidgets.QSpinBox(self)
        self.w_text_group4_min.setGeometry(GEOMETRY_TOP_7_3)
        self.w_text_group4_min.setMaximum(99999)
        self.w_text_group4_min.setSuffix(" seconds")
        self.w_label_group4_max = QtWidgets.QLabel("Maximal time:", self)
        self.w_label_group4_max.setGeometry(GEOMETRY_TOP_7_4)
        self.w_text_group4_max = QtWidgets.QSpinBox(self)
        self.w_text_group4_max.setGeometry(GEOMETRY_TOP_7_5)
        self.w_text_group4_max.setMaximum(99999)
        self.w_text_group4_max.setSuffix(" seconds")
        self.w_text_group4_max.setValue(self.w_text_group4_max.maximum())        


        self.w_checkbox_group5 = QtWidgets.QCheckBox("Group 5", self)
        self.w_checkbox_group5.setGeometry(GEOMETRY_TOP_8_0)
        self.w_checkbox_group5.stateChanged.connect(self.update)
        self.w_checkbox_group5_policy = QtWidgets.QCheckBox("Not Idle", self)
        self.w_checkbox_group5_policy.setGeometry(GEOMETRY_TOP_8_1)
        self.w_checkbox_group5_policy.setTristate()
        self.w_checkbox_group5_policy.stateChanged.connect(self.update)
        self.w_label_group5_min = QtWidgets.QLabel("Minimal time:", self)
        self.w_label_group5_min.setGeometry(GEOMETRY_TOP_8_2)
        self.w_text_group5_min = QtWidgets.QSpinBox(self)
        self.w_text_group5_min.setGeometry(GEOMETRY_TOP_8_3)
        self.w_text_group5_min.setMaximum(99999)
        self.w_text_group5_min.setSuffix(" seconds")
        self.w_label_group5_max = QtWidgets.QLabel("Maximal time:", self)
        self.w_label_group5_max.setGeometry(GEOMETRY_TOP_8_4)
        self.w_text_group5_max = QtWidgets.QSpinBox(self)
        self.w_text_group5_max.setGeometry(GEOMETRY_TOP_8_5)
        self.w_text_group5_max.setMaximum(99999)
        self.w_text_group5_max.setSuffix(" seconds")
        self.w_text_group5_max.setValue(self.w_text_group5_max.maximum())        


        self.w_checkbox_group6 = QtWidgets.QCheckBox("Group 6", self)
        self.w_checkbox_group6.setGeometry(GEOMETRY_TOP_9_0)
        self.w_checkbox_group6.stateChanged.connect(self.update)
        self.w_checkbox_group6_policy = QtWidgets.QCheckBox("Not Idle", self)
        self.w_checkbox_group6_policy.setGeometry(GEOMETRY_TOP_9_1)
        self.w_checkbox_group6_policy.setTristate()
        self.w_checkbox_group6_policy.stateChanged.connect(self.update)
        self.w_label_group6_min = QtWidgets.QLabel("Minimal time:", self)
        self.w_label_group6_min.setGeometry(GEOMETRY_TOP_9_2)
        self.w_text_group6_min = QtWidgets.QSpinBox(self)
        self.w_text_group6_min.setGeometry(GEOMETRY_TOP_9_3)
        self.w_text_group6_min.setMaximum(99999)
        self.w_text_group6_min.setSuffix(" seconds")
        self.w_label_group6_max = QtWidgets.QLabel("Maximal time:", self)
        self.w_label_group6_max.setGeometry(GEOMETRY_TOP_9_4)
        self.w_text_group6_max = QtWidgets.QSpinBox(self)
        self.w_text_group6_max.setGeometry(GEOMETRY_TOP_9_5)
        self.w_text_group6_max.setMaximum(99999)
        self.w_text_group6_max.setSuffix(" seconds")
        self.w_text_group6_max.setValue(self.w_text_group6_max.maximum())        


        self.w_checkbox_group7 = QtWidgets.QCheckBox("Group 7", self)
        self.w_checkbox_group7.setGeometry(GEOMETRY_TOP_10_0)
        self.w_checkbox_group7.stateChanged.connect(self.update)
        self.w_checkbox_group7_policy = QtWidgets.QCheckBox("Not Idle", self)
        self.w_checkbox_group7_policy.setGeometry(GEOMETRY_TOP_10_1)
        self.w_checkbox_group7_policy.setTristate()
        self.w_checkbox_group7_policy.stateChanged.connect(self.update)
        self.w_label_group7_min = QtWidgets.QLabel("Minimal time:", self)
        self.w_label_group7_min.setGeometry(GEOMETRY_TOP_10_2)
        self.w_text_group7_min = QtWidgets.QSpinBox(self)
        self.w_text_group7_min.setGeometry(GEOMETRY_TOP_10_3)
        self.w_text_group7_min.setMaximum(99999)
        self.w_text_group7_min.setSuffix(" seconds")
        self.w_label_group7_max = QtWidgets.QLabel("Maximal time:", self)
        self.w_label_group7_max.setGeometry(GEOMETRY_TOP_10_4)
        self.w_text_group7_max = QtWidgets.QSpinBox(self)
        self.w_text_group7_max.setGeometry(GEOMETRY_TOP_10_5)
        self.w_text_group7_max.setMaximum(99999)
        self.w_text_group7_max.setSuffix(" seconds")
        self.w_text_group7_max.setValue(self.w_text_group7_max.maximum())        


        self.w_checkbox_group8 = QtWidgets.QCheckBox("Group 8", self)
        self.w_checkbox_group8.setGeometry(GEOMETRY_TOP_11_0)
        self.w_checkbox_group8.stateChanged.connect(self.update)
        self.w_checkbox_group8_policy = QtWidgets.QCheckBox("Not Idle", self)
        self.w_checkbox_group8_policy.setGeometry(GEOMETRY_TOP_11_1)
        self.w_checkbox_group8_policy.setTristate()
        self.w_checkbox_group8_policy.stateChanged.connect(self.update)
        self.w_label_group8_min = QtWidgets.QLabel("Minimal time:", self)
        self.w_label_group8_min.setGeometry(GEOMETRY_TOP_11_2)
        self.w_text_group8_min = QtWidgets.QSpinBox(self)
        self.w_text_group8_min.setGeometry(GEOMETRY_TOP_11_3)
        self.w_text_group8_min.setMaximum(99999)
        self.w_text_group8_min.setSuffix(" seconds")
        self.w_label_group8_max = QtWidgets.QLabel("Maximal time:", self)
        self.w_label_group8_max.setGeometry(GEOMETRY_TOP_11_4)
        self.w_text_group8_max = QtWidgets.QSpinBox(self)
        self.w_text_group8_max.setGeometry(GEOMETRY_TOP_11_5)
        self.w_text_group8_max.setMaximum(99999)
        self.w_text_group8_max.setSuffix(" seconds")
        self.w_text_group8_max.setValue(self.w_text_group8_max.maximum())        


        self.w_checkbox_group9 = QtWidgets.QCheckBox("Group 9", self)
        self.w_checkbox_group9.setGeometry(GEOMETRY_TOP_12_0)
        self.w_checkbox_group9.stateChanged.connect(self.update)
        self.w_checkbox_group9_policy = QtWidgets.QCheckBox("Not Idle", self)
        self.w_checkbox_group9_policy.setGeometry(GEOMETRY_TOP_12_1)
        self.w_checkbox_group9_policy.setTristate()
        self.w_checkbox_group9_policy.stateChanged.connect(self.update)
        self.w_label_group9_min = QtWidgets.QLabel("Minimal time:", self)
        self.w_label_group9_min.setGeometry(GEOMETRY_TOP_12_2)
        self.w_text_group9_min = QtWidgets.QSpinBox(self)
        self.w_text_group9_min.setGeometry(GEOMETRY_TOP_12_3)
        self.w_text_group9_min.setMaximum(99999)
        self.w_text_group9_min.setSuffix(" seconds")
        self.w_label_group9_max = QtWidgets.QLabel("Maximal time:", self)
        self.w_label_group9_max.setGeometry(GEOMETRY_TOP_12_4)
        self.w_text_group9_max = QtWidgets.QSpinBox(self)
        self.w_text_group9_max.setGeometry(GEOMETRY_TOP_12_5)
        self.w_text_group9_max.setMaximum(99999)
        self.w_text_group9_max.setSuffix(" seconds")
        self.w_text_group9_max.setValue(self.w_text_group9_max.maximum())        


        self.w_checkbox_group0 = QtWidgets.QCheckBox("Group 0", self)
        self.w_checkbox_group0.setGeometry(GEOMETRY_TOP_13_0)
        self.w_checkbox_group0.stateChanged.connect(self.update)
        self.w_checkbox_group0_policy = QtWidgets.QCheckBox("Not Idle", self)
        self.w_checkbox_group0_policy.setGeometry(GEOMETRY_TOP_13_1)
        self.w_checkbox_group0_policy.setTristate()
        self.w_checkbox_group0_policy.stateChanged.connect(self.update)
        self.w_label_group0_min = QtWidgets.QLabel("Minimal time:", self)
        self.w_label_group0_min.setGeometry(GEOMETRY_TOP_13_2)
        self.w_text_group0_min = QtWidgets.QSpinBox(self)
        self.w_text_group0_min.setGeometry(GEOMETRY_TOP_13_3)
        self.w_text_group0_min.setMaximum(99999)
        self.w_text_group0_min.setSuffix(" seconds")
        self.w_label_group0_max = QtWidgets.QLabel("Maximal time:", self)
        self.w_label_group0_max.setGeometry(GEOMETRY_TOP_13_4)
        self.w_text_group0_max = QtWidgets.QSpinBox(self)
        self.w_text_group0_max.setGeometry(GEOMETRY_TOP_13_5)
        self.w_text_group0_max.setMaximum(99999)
        self.w_text_group0_max.setSuffix(" seconds")
        self.w_text_group0_max.setValue(self.w_text_group0_max.maximum())        


        self.w_checkbox_civilians = QtWidgets.QCheckBox("Civilians", self)
        self.w_checkbox_civilians.setGeometry(GEOMETRY_TOP_14_0)
        self.w_checkbox_civilians.stateChanged.connect(self.update)
        self.w_checkbox_civilians_policy = QtWidgets.QCheckBox("Not Idle", self)
        self.w_checkbox_civilians_policy.setGeometry(GEOMETRY_TOP_14_1)
        self.w_checkbox_civilians_policy.setTristate()
        self.w_checkbox_civilians_policy.stateChanged.connect(self.update)
        self.w_label_civilians_min = QtWidgets.QLabel("Minimal time:", self)
        self.w_label_civilians_min.setGeometry(GEOMETRY_TOP_14_2)
        self.w_text_civilians_min = QtWidgets.QSpinBox(self)
        self.w_text_civilians_min.setGeometry(GEOMETRY_TOP_14_3)
        self.w_text_civilians_min.setMaximum(99999)
        self.w_text_civilians_min.setSuffix(" seconds")
        self.w_label_civilians_max = QtWidgets.QLabel("Maximal time:", self)
        self.w_label_civilians_max.setGeometry(GEOMETRY_TOP_14_4)
        self.w_text_civilians_max = QtWidgets.QSpinBox(self)
        self.w_text_civilians_max.setGeometry(GEOMETRY_TOP_14_5)
        self.w_text_civilians_max.setMaximum(99999)
        self.w_text_civilians_max.setSuffix(" seconds")
        self.w_text_civilians_max.setValue(self.w_text_civilians_max.maximum())        


        self.w_checkbox_military = QtWidgets.QCheckBox("Military", self)
        self.w_checkbox_military.setGeometry(GEOMETRY_TOP_15_0)
        self.w_checkbox_military.stateChanged.connect(self.update)
        self.w_checkbox_military_policy = QtWidgets.QCheckBox("Not Idle", self)
        self.w_checkbox_military_policy.setGeometry(GEOMETRY_TOP_15_1)
        self.w_checkbox_military_policy.setTristate()
        self.w_checkbox_military_policy.stateChanged.connect(self.update)
        self.w_label_military_min = QtWidgets.QLabel("Minimal time:", self)
        self.w_label_military_min.setGeometry(GEOMETRY_TOP_15_2)
        self.w_text_military_min = QtWidgets.QSpinBox(self)
        self.w_text_military_min.setGeometry(GEOMETRY_TOP_15_3)
        self.w_text_military_min.setMaximum(99999)
        self.w_text_military_min.setSuffix(" seconds")
        self.w_label_military_max = QtWidgets.QLabel("Maximal time:", self)
        self.w_label_military_max.setGeometry(GEOMETRY_TOP_15_4)
        self.w_text_military_max = QtWidgets.QSpinBox(self)
        self.w_text_military_max.setGeometry(GEOMETRY_TOP_15_5)
        self.w_text_military_max.setMaximum(99999)
        self.w_text_military_max.setSuffix(" seconds")
        self.w_text_military_max.setValue(self.w_text_military_max.maximum())        


        self.update()

    def remove(self):
        print(1/0) # Shouldnt happen
        

    def set_hidden(self):
        if self.widget is not None: 
            if self.w_checkbox_hidden.isChecked():
                self.widget.setVisible(False)
            else:
                self.widget.setVisible(True)

    def rename_tab(self):
        for index in range(self.parent.w_tabs_settings.count()):
            if self == self.parent.w_tabs_settings.widget(index):
                self.parent.w_tabs_settings.setTabText(index, self.w_text_name.text())

    def bind_widget(self, widget):
        self.widget = widget
        self.widget.get_icons = self.settings

    def update_overlay_widget(self):
        self.widget.update()

    def settings(self):
        # Input
        objects = set(self.parent.game.pov.objects)
        # Output
        result = set()
        
        
        if self.w_checkbox_selected.isChecked():
            all_selected_units = list(self.parent.game.pov.selected)
            if self.w_checkbox_selected_policy.checkState() == 0:
                # Idle
                f = lambda obj: self.w_text_selected_min.value() < obj.busy_time/1000 and obj.busy_time/1000 < self.w_text_selected_max.value()
                result.update(set(filter(f, all_selected_units)))
            elif self.w_checkbox_selected_policy.checkState() == 2:
                # Busy
                f = lambda obj: self.w_text_selected_min.value() < obj.idle_time/1000 and obj.idle_time/1000 < self.w_text_selected_max.value() 
                result.update(set(filter(f, all_selected_units)))
            else:
                # No filter
                result.update(set(all_selected_units))
            objects = objects - result

        if self.w_checkbox_monks_relic.isChecked():
            monks = list(filter(lambda obj: obj.udata.class_ == ClassData.monk_with_relic_idx, self.parent.game.pov.monks))
            if self.w_checkbox_monks_relic_policy.checkState() == 0:
                # Idle
                f = lambda obj: self.w_text_monks_relic_min.value() < obj.busy_time/1000 and obj.busy_time/1000 < self.w_text_monks_relic_max.value()
                result.update(set(filter(f, monks)))
            elif self.w_checkbox_monks_relic_policy.checkState() == 2:
                # Busy
                f = lambda obj: self.w_text_monks_relic_min.value() < obj.idle_time/1000 and obj.idle_time/1000 < self.w_text_monks_relic_max.value() 
                result.update(set(filter(f, monks)))
            else:
                # No filter
                result.update(set(monks))
            objects = objects - result

        if self.w_checkbox_group1.isChecked():
            group1 = list(filter(lambda obj: obj.group & 0x002, objects))
            if self.w_checkbox_group1_policy.checkState() == 0:
                # Idle
                f = lambda obj: self.w_text_group1_min.value() < obj.busy_time/1000 and obj.busy_time/1000 < self.w_text_group1_max.value()
                result.update(set(filter(f, group1)))
            elif self.w_checkbox_group1_policy.checkState() == 2:
                # Busy
                f = lambda obj: self.w_text_group1_min.value() < obj.idle_time/1000 and obj.idle_time/1000 < self.w_text_group1_max.value() 
                result.update(set(filter(f, group1)))
            else:
                # No filter
                result.update(set(group1))
            objects = objects - result
        if self.w_checkbox_group2.isChecked():
            group2 = list(filter(lambda obj: obj.group & 0x004, objects))
            if self.w_checkbox_group2_policy.checkState() == 0:
                # Idle
                f = lambda obj: self.w_text_group2_min.value() < obj.busy_time/1000 and obj.busy_time/1000 < self.w_text_group2_max.value()
                result.update(set(filter(f, group2)))
            elif self.w_checkbox_group2_policy.checkState() == 2:
                # Busy
                f = lambda obj: self.w_text_group2_min.value() < obj.idle_time/1000 and obj.idle_time/1000 < self.w_text_group2_max.value() 
                result.update(set(filter(f, group2)))
            else:
                # No filter
                result.update(set(group2))
            objects = objects - result
        if self.w_checkbox_group3.isChecked():
            group3 = list(filter(lambda obj: obj.group & 0x008, objects))
            if self.w_checkbox_group3_policy.checkState() == 0:
                # Idle
                f = lambda obj: self.w_text_group3_min.value() < obj.busy_time/1000 and obj.busy_time/1000 < self.w_text_group3_max.value()
                result.update(set(filter(f, group3)))
            elif self.w_checkbox_group3_policy.checkState() == 2:
                # Busy
                f = lambda obj: self.w_text_group3_min.value() < obj.idle_time/1000 and obj.idle_time/1000 < self.w_text_group3_max.value() 
                result.update(set(filter(f, group3)))
            else:
                # No filter
                result.update(set(group3))
            objects = objects - result
        if self.w_checkbox_group4.isChecked():
            group4 = list(filter(lambda obj: obj.group & 0x010, objects))
            if self.w_checkbox_group4_policy.checkState() == 0:
                # Idle
                f = lambda obj: self.w_text_group4_min.value() < obj.busy_time/1000 and obj.busy_time/1000 < self.w_text_group4_max.value()
                result.update(set(filter(f, group4)))
            elif self.w_checkbox_group4_policy.checkState() == 2:
                # Busy
                f = lambda obj: self.w_text_group4_min.value() < obj.idle_time/1000 and obj.idle_time/1000 < self.w_text_group4_max.value() 
                result.update(set(filter(f, group4)))
            else:
                # No filter
                result.update(set(group4))
            objects = objects - result
        if self.w_checkbox_group5.isChecked():
            group5 = list(filter(lambda obj: obj.group & 0x020, objects))
            if self.w_checkbox_group5_policy.checkState() == 0:
                # Idle
                f = lambda obj: self.w_text_group5_min.value() < obj.busy_time/1000 and obj.busy_time/1000 < self.w_text_group5_max.value()
                result.update(set(filter(f, group5)))
            elif self.w_checkbox_group5_policy.checkState() == 2:
                # Busy
                f = lambda obj: self.w_text_group5_min.value() < obj.idle_time/1000 and obj.idle_time/1000 < self.w_text_group5_max.value() 
                result.update(set(filter(f, group5)))
            else:
                # No filter
                result.update(set(group5))
            objects = objects - result
        if self.w_checkbox_group6.isChecked():
            group6 = list(filter(lambda obj: obj.group & 0x040, objects))
            if self.w_checkbox_group6_policy.checkState() == 0:
                # Idle
                f = lambda obj: self.w_text_group6_min.value() < obj.busy_time/1000 and obj.busy_time/1000 < self.w_text_group6_max.value()
                result.update(set(filter(f, group6)))
            elif self.w_checkbox_group6_policy.checkState() == 2:
                # Busy
                f = lambda obj: self.w_text_group6_min.value() < obj.idle_time/1000 and obj.idle_time/1000 < self.w_text_group6_max.value() 
                result.update(set(filter(f, group6)))
            else:
                # No filter
                result.update(set(group6))
            objects = objects - result
        if self.w_checkbox_group7.isChecked():
            group7 = list(filter(lambda obj: obj.group & 0x080, objects))
            if self.w_checkbox_group7_policy.checkState() == 0:
                # Idle
                f = lambda obj: self.w_text_group7_min.value() < obj.busy_time/1000 and obj.busy_time/1000 < self.w_text_group7_max.value()
                result.update(set(filter(f, group7)))
            elif self.w_checkbox_group7_policy.checkState() == 2:
                # Busy
                f = lambda obj: self.w_text_group7_min.value() < obj.idle_time/1000 and obj.idle_time/1000 < self.w_text_group7_max.value() 
                result.update(set(filter(f, group7)))
            else:
                # No filter
                result.update(set(group7))
            objects = objects - result
        if self.w_checkbox_group8.isChecked():
            group8 = list(filter(lambda obj: obj.group & 0x100, objects))
            if self.w_checkbox_group8_policy.checkState() == 0:
                # Idle
                f = lambda obj: self.w_text_group8_min.value() < obj.busy_time/1000 and obj.busy_time/1000 < self.w_text_group8_max.value()
                result.update(set(filter(f, group8)))
            elif self.w_checkbox_group8_policy.checkState() == 2:
                # Busy
                f = lambda obj: self.w_text_group8_min.value() < obj.idle_time/1000 and obj.idle_time/1000 < self.w_text_group8_max.value() 
                result.update(set(filter(f, group8)))
            else:
                # No filter
                result.update(set(group8))
            objects = objects - result
        if self.w_checkbox_group9.isChecked():
            group9 = list(filter(lambda obj: obj.group & 0x200, objects))
            if self.w_checkbox_group9_policy.checkState() == 0:
                # Idle
                f = lambda obj: self.w_text_group9_min.value() < obj.busy_time/1000 and obj.busy_time/1000 < self.w_text_group9_max.value()
                result.update(set(filter(f, group9)))
            elif self.w_checkbox_group9_policy.checkState() == 2:
                # Busy
                f = lambda obj: self.w_text_group9_min.value() < obj.idle_time/1000 and obj.idle_time/1000 < self.w_text_group9_max.value() 
                result.update(set(filter(f, group9)))
            else:
                # No filter
                result.update(set(group9))
            objects = objects - result
        if self.w_checkbox_group0.isChecked():
            group0 = list(filter(lambda obj: obj.group & 0x400, objects))
            if self.w_checkbox_group0_policy.checkState() == 0:
                # Idle
                f = lambda obj: self.w_text_group0_min.value() < obj.busy_time/1000 and obj.busy_time/1000 < self.w_text_group0_max.value()
                result.update(set(filter(f, group0)))
            elif self.w_checkbox_group0_policy.checkState() == 2:
                # Busy
                f = lambda obj: self.w_text_group0_min.value() < obj.idle_time/1000 and obj.idle_time/1000 < self.w_text_group0_max.value() 
                result.update(set(filter(f, group0)))
            else:
                # No filter
                result.update(set(group0))
            objects = objects - result
        if self.w_checkbox_civilians.isChecked():
            civilians = objects & set(self.parent.game.pov.civilians)
            if self.w_checkbox_civilians_policy.checkState() == 0:
                # Idle
                f = lambda obj: self.w_text_civilians_min.value() < obj.busy_time/1000 and obj.busy_time/1000 < self.w_text_civilians_max.value()
                result.update(set(filter(f, civilians)))
            elif self.w_checkbox_civilians_policy.checkState() == 2:
                # Busy
                f = lambda obj: self.w_text_civilians_min.value() < obj.idle_time/1000 and obj.idle_time/1000 < self.w_text_civilians_max.value() 
                result.update(set(filter(f, civilians)))
            else:
                # No filter
                result.update(set(civilians))
            objects = objects - result
        if self.w_checkbox_military.isChecked():
            military = objects & set(self.parent.game.pov.military)
            if self.w_checkbox_military_policy.checkState() == 0:
                # Idle
                f = lambda obj: self.w_text_military_min.value() < obj.busy_time/1000 and obj.busy_time/1000 < self.w_text_military_max.value()
                result.update(set(filter(f, military)))
            elif self.w_checkbox_military_policy.checkState() == 2:
                # Busy
                f = lambda obj: self.w_text_military_min.value() < obj.idle_time/1000 and obj.idle_time/1000 < self.w_text_military_max.value() 
                result.update(set(filter(f, military)))
            else:
                # No filter
                result.update(set(military))
            objects = objects - result
        return result
        #return self.parent.game.pov.selected


    def lock_unlock(self):
        self.w_checkbox_selected_policy.setEnabled(self.w_checkbox_selected.isChecked())
        self.w_checkbox_monks_relic_policy.setEnabled(self.w_checkbox_monks_relic.isChecked())
        self.w_checkbox_group1_policy.setEnabled(self.w_checkbox_group1.isChecked())
        self.w_checkbox_group2_policy.setEnabled(self.w_checkbox_group2.isChecked())
        self.w_checkbox_group3_policy.setEnabled(self.w_checkbox_group3.isChecked())
        self.w_checkbox_group4_policy.setEnabled(self.w_checkbox_group4.isChecked())
        self.w_checkbox_group5_policy.setEnabled(self.w_checkbox_group5.isChecked())
        self.w_checkbox_group6_policy.setEnabled(self.w_checkbox_group6.isChecked())
        self.w_checkbox_group7_policy.setEnabled(self.w_checkbox_group7.isChecked())
        self.w_checkbox_group8_policy.setEnabled(self.w_checkbox_group8.isChecked())
        self.w_checkbox_group9_policy.setEnabled(self.w_checkbox_group9.isChecked())
        self.w_checkbox_group0_policy.setEnabled(self.w_checkbox_group0.isChecked())
        self.w_checkbox_civilians_policy.setEnabled(self.w_checkbox_civilians.isChecked())
        self.w_checkbox_military_policy.setEnabled(self.w_checkbox_military.isChecked())

        self.w_text_selected_min.setEnabled(self.w_checkbox_selected_policy.checkState() != 1 and self.w_checkbox_selected_policy.isEnabled())
        self.w_text_monks_relic_min.setEnabled(self.w_checkbox_monks_relic_policy.checkState() != 1 and self.w_checkbox_monks_relic_policy.isEnabled())
        self.w_text_group1_min.setEnabled(self.w_checkbox_group1_policy.checkState() != 1 and self.w_checkbox_group1_policy.isEnabled())
        self.w_text_group2_min.setEnabled(self.w_checkbox_group2_policy.checkState() != 1 and self.w_checkbox_group2_policy.isEnabled())
        self.w_text_group3_min.setEnabled(self.w_checkbox_group3_policy.checkState() != 1 and self.w_checkbox_group3_policy.isEnabled())
        self.w_text_group4_min.setEnabled(self.w_checkbox_group4_policy.checkState() != 1 and self.w_checkbox_group4_policy.isEnabled())
        self.w_text_group5_min.setEnabled(self.w_checkbox_group5_policy.checkState() != 1 and self.w_checkbox_group5_policy.isEnabled())
        self.w_text_group6_min.setEnabled(self.w_checkbox_group6_policy.checkState() != 1 and self.w_checkbox_group6_policy.isEnabled())
        self.w_text_group7_min.setEnabled(self.w_checkbox_group7_policy.checkState() != 1 and self.w_checkbox_group7_policy.isEnabled())
        self.w_text_group8_min.setEnabled(self.w_checkbox_group8_policy.checkState() != 1 and self.w_checkbox_group8_policy.isEnabled())
        self.w_text_group9_min.setEnabled(self.w_checkbox_group9_policy.checkState() != 1 and self.w_checkbox_group9_policy.isEnabled())
        self.w_text_group0_min.setEnabled(self.w_checkbox_group0_policy.checkState() != 1 and self.w_checkbox_group0_policy.isEnabled())
        self.w_text_civilians_min.setEnabled(self.w_checkbox_civilians_policy.checkState() != 1 and self.w_checkbox_civilians_policy.isEnabled())
        self.w_text_military_min.setEnabled(self.w_checkbox_military_policy.checkState() != 1 and self.w_checkbox_military_policy.isEnabled())

        self.w_text_selected_max.setEnabled(self.w_checkbox_selected_policy.checkState() != 1 and self.w_checkbox_selected_policy.isEnabled())
        self.w_text_monks_relic_max.setEnabled(self.w_checkbox_monks_relic_policy.checkState() != 1 and self.w_checkbox_monks_relic_policy.isEnabled())
        self.w_text_group1_max.setEnabled(self.w_checkbox_group1_policy.checkState() != 1 and self.w_checkbox_group1_policy.isEnabled())
        self.w_text_group2_max.setEnabled(self.w_checkbox_group2_policy.checkState() != 1 and self.w_checkbox_group2_policy.isEnabled())
        self.w_text_group3_max.setEnabled(self.w_checkbox_group3_policy.checkState() != 1 and self.w_checkbox_group3_policy.isEnabled())
        self.w_text_group4_max.setEnabled(self.w_checkbox_group4_policy.checkState() != 1 and self.w_checkbox_group4_policy.isEnabled())
        self.w_text_group5_max.setEnabled(self.w_checkbox_group5_policy.checkState() != 1 and self.w_checkbox_group5_policy.isEnabled())
        self.w_text_group6_max.setEnabled(self.w_checkbox_group6_policy.checkState() != 1 and self.w_checkbox_group6_policy.isEnabled())
        self.w_text_group7_max.setEnabled(self.w_checkbox_group7_policy.checkState() != 1 and self.w_checkbox_group7_policy.isEnabled())
        self.w_text_group8_max.setEnabled(self.w_checkbox_group8_policy.checkState() != 1 and self.w_checkbox_group8_policy.isEnabled())
        self.w_text_group9_max.setEnabled(self.w_checkbox_group9_policy.checkState() != 1 and self.w_checkbox_group9_policy.isEnabled())
        self.w_text_group0_max.setEnabled(self.w_checkbox_group0_policy.checkState() != 1 and self.w_checkbox_group0_policy.isEnabled())
        self.w_text_civilians_max.setEnabled(self.w_checkbox_civilians_policy.checkState() != 1 and self.w_checkbox_civilians_policy.isEnabled())
        self.w_text_military_max.setEnabled(self.w_checkbox_military_policy.checkState() != 1 and self.w_checkbox_military_policy.isEnabled())

        self.w_label_selected_min.setEnabled(self.w_checkbox_selected_policy.checkState() != 1 and self.w_checkbox_selected_policy.isEnabled())
        self.w_label_monks_relic_min.setEnabled(self.w_checkbox_monks_relic_policy.checkState() != 1 and self.w_checkbox_monks_relic_policy.isEnabled())
        self.w_label_group1_min.setEnabled(self.w_checkbox_group1_policy.checkState() != 1 and self.w_checkbox_group1_policy.isEnabled())
        self.w_label_group2_min.setEnabled(self.w_checkbox_group2_policy.checkState() != 1 and self.w_checkbox_group2_policy.isEnabled())
        self.w_label_group3_min.setEnabled(self.w_checkbox_group3_policy.checkState() != 1 and self.w_checkbox_group3_policy.isEnabled())
        self.w_label_group4_min.setEnabled(self.w_checkbox_group4_policy.checkState() != 1 and self.w_checkbox_group4_policy.isEnabled())
        self.w_label_group5_min.setEnabled(self.w_checkbox_group5_policy.checkState() != 1 and self.w_checkbox_group5_policy.isEnabled())
        self.w_label_group6_min.setEnabled(self.w_checkbox_group6_policy.checkState() != 1 and self.w_checkbox_group6_policy.isEnabled())
        self.w_label_group7_min.setEnabled(self.w_checkbox_group7_policy.checkState() != 1 and self.w_checkbox_group7_policy.isEnabled())
        self.w_label_group8_min.setEnabled(self.w_checkbox_group8_policy.checkState() != 1 and self.w_checkbox_group8_policy.isEnabled())
        self.w_label_group9_min.setEnabled(self.w_checkbox_group9_policy.checkState() != 1 and self.w_checkbox_group9_policy.isEnabled())
        self.w_label_group0_min.setEnabled(self.w_checkbox_group0_policy.checkState() != 1 and self.w_checkbox_group0_policy.isEnabled())
        self.w_label_civilians_min.setEnabled(self.w_checkbox_civilians_policy.checkState() != 1 and self.w_checkbox_civilians_policy.isEnabled())
        self.w_label_military_min.setEnabled(self.w_checkbox_military_policy.checkState() != 1 and self.w_checkbox_military_policy.isEnabled()) #x

        self.w_label_selected_max.setEnabled(self.w_checkbox_selected_policy.checkState() != 1 and self.w_checkbox_selected_policy.isEnabled())
        self.w_label_monks_relic_max.setEnabled(self.w_checkbox_monks_relic_policy.checkState() != 1 and self.w_checkbox_monks_relic_policy.isEnabled())
        self.w_label_group1_max.setEnabled(self.w_checkbox_group1_policy.checkState() != 1 and self.w_checkbox_group1_policy.isEnabled())
        self.w_label_group2_max.setEnabled(self.w_checkbox_group2_policy.checkState() != 1 and self.w_checkbox_group2_policy.isEnabled())
        self.w_label_group3_max.setEnabled(self.w_checkbox_group3_policy.checkState() != 1 and self.w_checkbox_group3_policy.isEnabled())
        self.w_label_group4_max.setEnabled(self.w_checkbox_group4_policy.checkState() != 1 and self.w_checkbox_group4_policy.isEnabled())
        self.w_label_group5_max.setEnabled(self.w_checkbox_group5_policy.checkState() != 1 and self.w_checkbox_group5_policy.isEnabled())
        self.w_label_group6_max.setEnabled(self.w_checkbox_group6_policy.checkState() != 1 and self.w_checkbox_group6_policy.isEnabled())
        self.w_label_group7_max.setEnabled(self.w_checkbox_group7_policy.checkState() != 1 and self.w_checkbox_group7_policy.isEnabled())
        self.w_label_group8_max.setEnabled(self.w_checkbox_group8_policy.checkState() != 1 and self.w_checkbox_group8_policy.isEnabled())
        self.w_label_group9_max.setEnabled(self.w_checkbox_group9_policy.checkState() != 1 and self.w_checkbox_group9_policy.isEnabled())
        self.w_label_group0_max.setEnabled(self.w_checkbox_group0_policy.checkState() != 1 and self.w_checkbox_group0_policy.isEnabled())
        self.w_label_civilians_max.setEnabled(self.w_checkbox_civilians_policy.checkState() != 1 and self.w_checkbox_civilians_policy.isEnabled())
        self.w_label_military_max.setEnabled(self.w_checkbox_military_policy.checkState() != 1 and self.w_checkbox_military_policy.isEnabled())

        name = ["Busy", "Whatever", "Idle"]
        self.w_checkbox_selected_policy.setText(name[self.w_checkbox_selected_policy.checkState()])
        self.w_checkbox_monks_relic_policy.setText(name[self.w_checkbox_monks_relic_policy.checkState()])
        self.w_checkbox_group1_policy.setText(name[self.w_checkbox_group1_policy.checkState()])
        self.w_checkbox_group2_policy.setText(name[self.w_checkbox_group2_policy.checkState()])
        self.w_checkbox_group3_policy.setText(name[self.w_checkbox_group3_policy.checkState()])
        self.w_checkbox_group4_policy.setText(name[self.w_checkbox_group4_policy.checkState()])
        self.w_checkbox_group5_policy.setText(name[self.w_checkbox_group5_policy.checkState()])
        self.w_checkbox_group6_policy.setText(name[self.w_checkbox_group6_policy.checkState()])
        self.w_checkbox_group7_policy.setText(name[self.w_checkbox_group7_policy.checkState()])
        self.w_checkbox_group8_policy.setText(name[self.w_checkbox_group8_policy.checkState()])
        self.w_checkbox_group9_policy.setText(name[self.w_checkbox_group9_policy.checkState()])
        self.w_checkbox_group0_policy.setText(name[self.w_checkbox_group0_policy.checkState()])
        self.w_checkbox_civilians_policy.setText(name[self.w_checkbox_civilians_policy.checkState()])
        self.w_checkbox_military_policy.setText(name[self.w_checkbox_military_policy.checkState()])
        
    def update(self):
        self.lock_unlock()
        # Just update if over_panel is set
        if type(self.widget) is OverlayOffscreenUnits:
            self.widget.get_icons = self.settings
            # Printing the shown icons
            #print(self.widget.panel_info_f())


if __name__ == '__main__':
    import bartender
