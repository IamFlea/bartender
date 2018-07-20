from collections import defaultdict

from PyQt5 import QtWidgets, QtCore, Qt, QtGui

from aoc_time import *
from aoc_object_consts import ClassData
from aoc_object_consts_unit import UNITS
from interface_utils import *
from interface_consts import *

from ui_iconlist import IconList

class InterfaceBar(QtWidgets.QWidget):
    """docstring for InterfaceBar"""
    BIND_TYPE = IconList

    def __init__(self, name, parent):
        super(InterfaceBar, self).__init__(parent)
        self.parent = parent
        self.icon_list = None
        self.setGeometry(GEOMETRY)


        self.w_label_name = QtWidgets.QLabel("Name:", self)
        self.w_label_name.setGeometry(GEOMETRY_TOP_0_1)
        self.w_text_name = QtWidgets.QLineEdit(name, self)
        self.w_text_name.setGeometry(GEOMETRY_TOP_0_2)
        self.w_text_name.textChanged.connect(self.rename_tab)

        """
        self.w_label_expand = QtWidgets.QLabel("Expand:", self)
        self.w_label_expand.setGeometry(GEOMETRY_TOP_0_2)
        self.w_combo_expand = QtWidgets.QComboBox(self)
        self.w_combo_expand.setGeometry(GEOMETRY_TOP_0_3)
        self.w_combo_expand.addItems(COMBO_EXPAND_ITEMS)
        self.w_combo_expand.setCurrentIndex(3)
        """
        self.w_checkbox_movable = QtWidgets.QCheckBox("Movable", self)
        self.w_checkbox_movable.setGeometry(GEOMETRY_TOP_0_5)
        self.w_checkbox_movable.stateChanged.connect(self.set_movable)

        self.w_checkbox_aggregate = QtWidgets.QCheckBox("Aggregate", self)
        self.w_checkbox_aggregate.setGeometry(GEOMETRY_TOP_0_3)
        self.w_checkbox_aggregate.stateChanged.connect(self.set_aggregate)

        self.w_checkbox_hidden = QtWidgets.QCheckBox("Hidden", self)
        self.w_checkbox_hidden.setGeometry(GEOMETRY_TOP_0_4)
        self.w_checkbox_hidden.stateChanged.connect(self.set_hidden)

        self.w_label_idle = QtWidgets.QLabel("If Idle Pulse for", self)
        self.w_label_idle.setGeometry(GEOMETRY_TOP_2_1)
        self.w_text_idle_time_for_pulsing = QtWidgets.QSpinBox(self)
        self.w_text_idle_time_for_pulsing.setGeometry(GEOMETRY_TOP_2_2)
        self.w_text_idle_time_for_pulsing.setMaximum(99999)
        self.w_text_idle_time_for_pulsing.setSuffix(" seconds")
        self.w_text_idle_time_for_pulsing.valueChanged.connect(self.pulse)

        self.w_label_idle = QtWidgets.QLabel("If Idle Blink for", self)
        self.w_label_idle.setGeometry(GEOMETRY_TOP_3_1)
        self.w_text_idle_time_for_blinkin = QtWidgets.QSpinBox(self)
        self.w_text_idle_time_for_blinkin.setGeometry(GEOMETRY_TOP_3_2)
        self.w_text_idle_time_for_blinkin.setMaximum(99999)
        self.w_text_idle_time_for_blinkin.setSuffix(" seconds")
        self.w_text_idle_time_for_blinkin.valueChanged.connect(self.blink)
     

        self.w_label__timer_number = QtWidgets.QLabel("Timer:", self)
        self.w_label__timer_number.setGeometry(GEOMETRY_TOP_1_3)
        self.w_combo_timer_number = QtWidgets.QComboBox(self)
        self.w_combo_timer_number.setGeometry(GEOMETRY_TOP_1_4)
        self.w_combo_timer_number.addItems(COMBO_TIMER_ITEMS)
        self.w_combo_timer_number.currentIndexChanged.connect(self.timer)

        self.w_label__top_number = QtWidgets.QLabel("Top Number:", self)
        self.w_label__top_number.setGeometry(GEOMETRY_TOP_2_3)
        self.w_combo_top_number = QtWidgets.QComboBox(self)
        self.w_combo_top_number.setGeometry(GEOMETRY_TOP_2_4)
        self.w_combo_top_number.addItems(COMBO_TOP_BOTTOM_NUMBER_ITEMS)
        self.w_combo_top_number.currentIndexChanged.connect(self.top_text_change)
        self.w_combo_top_number_aggr = QtWidgets.QComboBox(self)
        self.w_combo_top_number_aggr.currentIndexChanged.connect(self.top_text_change)
        self.w_combo_top_number_aggr.setGeometry(GEOMETRY_TOP_2_4)
        self.w_combo_top_number_aggr.addItems(COMBO_TOP_BOTTOM_NUMBER_ITEMS_AGGR)
        self.w_combo_top_number_aggr.setHidden(True)
        self.w_label__bottom_number = QtWidgets.QLabel("Bottom Number:", self)
        self.w_label__bottom_number.setGeometry(GEOMETRY_TOP_3_3)
        self.w_combo_bottom_number = QtWidgets.QComboBox(self)
        self.w_combo_bottom_number.setGeometry(GEOMETRY_TOP_3_4)
        self.w_combo_bottom_number.addItems(COMBO_TOP_BOTTOM_NUMBER_ITEMS)
        self.w_combo_bottom_number.currentIndexChanged.connect(self.bottom_text_change)
        self.w_combo_bottom_number_aggr = QtWidgets.QComboBox(self)
        self.w_combo_bottom_number_aggr.setGeometry(GEOMETRY_TOP_3_4)
        self.w_combo_bottom_number_aggr.addItems(COMBO_TOP_BOTTOM_NUMBER_ITEMS_AGGR)
        self.w_combo_bottom_number_aggr.setHidden(True)
        self.w_combo_bottom_number_aggr.currentIndexChanged.connect(self.bottom_text_change)

        self.w_groupbox = QtWidgets.QGroupBox("Shown Icons", self)
        self.w_groupbox.setGeometry(GEOMETRY_GROUPBOX_POLICY)
        self.w_checkbox_show_all_units = QtWidgets.QCheckBox("All Units", self)
        self.w_checkbox_show_all_units.setGeometry(GEOMETRY_GROUPBOX_POLICY_0_0)
        self.w_checkbox_show_all_units.stateChanged.connect(self.policy)
        self.w_checkbox_show_civilians = QtWidgets.QCheckBox("Civilians", self)
        self.w_checkbox_show_civilians.setGeometry(GEOMETRY_GROUPBOX_POLICY_0_1)
        self.w_checkbox_show_civilians.stateChanged.connect(self.policy)
        self.w_checkbox_show_military = QtWidgets.QCheckBox("Military", self)
        self.w_checkbox_show_military.setGeometry(GEOMETRY_GROUPBOX_POLICY_0_2)
        self.w_checkbox_show_military.stateChanged.connect(self.policy)        
        self.w_checkbox_show_trade_units = QtWidgets.QCheckBox("Trade Units", self)
        self.w_checkbox_show_trade_units.setGeometry(GEOMETRY_GROUPBOX_POLICY_0_3)
        self.w_checkbox_show_trade_units.stateChanged.connect(self.policy)
        self.w_checkbox_show_fish_ships = QtWidgets.QCheckBox("Fish Ships", self)
        self.w_checkbox_show_fish_ships.setGeometry(GEOMETRY_GROUPBOX_POLICY_0_4)
        self.w_checkbox_show_fish_ships.stateChanged.connect(self.policy)
        
        self.w_checkbox_show_villagers = QtWidgets.QCheckBox("Villagers", self)
        self.w_checkbox_show_villagers.setGeometry(GEOMETRY_GROUPBOX_POLICY_1_0)
        self.w_checkbox_show_villagers.stateChanged.connect(self.policy)
        self.w_checkbox_show_food_vills = QtWidgets.QCheckBox("Food Vills", self)
        self.w_checkbox_show_food_vills.setGeometry(GEOMETRY_GROUPBOX_POLICY_1_1)
        self.w_checkbox_show_food_vills.stateChanged.connect(self.policy)
        self.w_checkbox_show_wood_vills = QtWidgets.QCheckBox("Wood Vills", self)
        self.w_checkbox_show_wood_vills.setGeometry(GEOMETRY_GROUPBOX_POLICY_1_2)
        self.w_checkbox_show_wood_vills.stateChanged.connect(self.policy)
        self.w_checkbox_show_gold_vills = QtWidgets.QCheckBox("Gold Vills", self)
        self.w_checkbox_show_gold_vills.setGeometry(GEOMETRY_GROUPBOX_POLICY_1_3)
        self.w_checkbox_show_gold_vills.stateChanged.connect(self.policy)
        self.w_checkbox_show_stone_vills = QtWidgets.QCheckBox("Stone Vills", self)
        self.w_checkbox_show_stone_vills.setGeometry(GEOMETRY_GROUPBOX_POLICY_1_4)
        self.w_checkbox_show_stone_vills.stateChanged.connect(self.policy)

        self.w_checkbox_show_swordsmen = QtWidgets.QCheckBox("Swordsmen", self)
        self.w_checkbox_show_swordsmen.setGeometry(GEOMETRY_GROUPBOX_POLICY_2_0)
        self.w_checkbox_show_swordsmen.stateChanged.connect(self.policy)
        self.w_checkbox_show_pikemen = QtWidgets.QCheckBox("Pikemen", self)
        self.w_checkbox_show_pikemen.setGeometry(GEOMETRY_GROUPBOX_POLICY_2_1)
        self.w_checkbox_show_pikemen.stateChanged.connect(self.policy)
        self.w_checkbox_show_eagles = QtWidgets.QCheckBox("Eagle War.", self)
        self.w_checkbox_show_eagles.setGeometry(GEOMETRY_GROUPBOX_POLICY_2_2)
        self.w_checkbox_show_eagles.stateChanged.connect(self.policy)
        self.w_checkbox_show_huskarls = QtWidgets.QCheckBox("Huskarls", self)
        self.w_checkbox_show_huskarls.setGeometry(GEOMETRY_GROUPBOX_POLICY_2_3)
        self.w_checkbox_show_huskarls.stateChanged.connect(self.policy)
        self.w_checkbox_show_condottieros = QtWidgets.QCheckBox("Condottieros", self)
        self.w_checkbox_show_condottieros.setGeometry(GEOMETRY_GROUPBOX_POLICY_2_4)
        self.w_checkbox_show_condottieros.stateChanged.connect(self.policy)


        self.w_checkbox_show_light_cavalry = QtWidgets.QCheckBox("Light Cavalry", self)
        self.w_checkbox_show_light_cavalry.setGeometry(GEOMETRY_GROUPBOX_POLICY_3_0)
        self.w_checkbox_show_light_cavalry.stateChanged.connect(self.policy)
        self.w_checkbox_show_heavy_cavalry = QtWidgets.QCheckBox("Heavy Cav.", self)
        self.w_checkbox_show_heavy_cavalry.setGeometry(GEOMETRY_GROUPBOX_POLICY_3_1)
        self.w_checkbox_show_heavy_cavalry.stateChanged.connect(self.policy)
        self.w_checkbox_show_camels = QtWidgets.QCheckBox("Camels", self)
        self.w_checkbox_show_camels.setGeometry(GEOMETRY_GROUPBOX_POLICY_3_2)
        self.w_checkbox_show_camels.stateChanged.connect(self.policy)
        self.w_checkbox_show_tarkans = QtWidgets.QCheckBox("Tarkans", self)
        self.w_checkbox_show_tarkans.setGeometry(GEOMETRY_GROUPBOX_POLICY_3_3)
        self.w_checkbox_show_tarkans.stateChanged.connect(self.policy)
        self.w_checkbox_show_battle_elephants = QtWidgets.QCheckBox("Battle Elph.", self)
        self.w_checkbox_show_battle_elephants.setGeometry(GEOMETRY_GROUPBOX_POLICY_3_4)
        self.w_checkbox_show_battle_elephants.stateChanged.connect(self.policy)

        self.w_checkbox_show_archers = QtWidgets.QCheckBox("Archers", self)
        self.w_checkbox_show_archers.setGeometry(GEOMETRY_GROUPBOX_POLICY_4_0)
        self.w_checkbox_show_archers.stateChanged.connect(self.policy)
        self.w_checkbox_show_skirmishers = QtWidgets.QCheckBox("Skirmishers", self)
        self.w_checkbox_show_skirmishers.setGeometry(GEOMETRY_GROUPBOX_POLICY_4_1)
        self.w_checkbox_show_skirmishers.stateChanged.connect(self.policy)
        self.w_checkbox_show_cavalry_archers = QtWidgets.QCheckBox("Cav. Archers", self)
        self.w_checkbox_show_cavalry_archers.setGeometry(GEOMETRY_GROUPBOX_POLICY_4_2)
        self.w_checkbox_show_cavalry_archers.stateChanged.connect(self.policy)
        self.w_checkbox_show_genitours = QtWidgets.QCheckBox("Genitours", self)
        self.w_checkbox_show_genitours.setGeometry(GEOMETRY_GROUPBOX_POLICY_4_3)
        self.w_checkbox_show_genitours.stateChanged.connect(self.policy)
        self.w_checkbox_show_hand_cannoneers = QtWidgets.QCheckBox("Hand Canno.", self)
        self.w_checkbox_show_hand_cannoneers.setGeometry(GEOMETRY_GROUPBOX_POLICY_4_4)
        self.w_checkbox_show_hand_cannoneers.stateChanged.connect(self.policy)

        self.w_checkbox_show_siege_rams = QtWidgets.QCheckBox("Siege Rams", self)
        self.w_checkbox_show_siege_rams.setGeometry(GEOMETRY_GROUPBOX_POLICY_5_0)
        self.w_checkbox_show_siege_rams.stateChanged.connect(self.policy)
        self.w_checkbox_show_onagers = QtWidgets.QCheckBox("Onagers", self)
        self.w_checkbox_show_onagers.setGeometry(GEOMETRY_GROUPBOX_POLICY_5_1)
        self.w_checkbox_show_onagers.stateChanged.connect(self.policy)
        self.w_checkbox_show_scorpions = QtWidgets.QCheckBox("Scorpions", self)
        self.w_checkbox_show_scorpions.setGeometry(GEOMETRY_GROUPBOX_POLICY_5_2)
        self.w_checkbox_show_scorpions.stateChanged.connect(self.policy)
        self.w_checkbox_show_bombard_cannons = QtWidgets.QCheckBox("Bombard C.", self)
        self.w_checkbox_show_bombard_cannons.setGeometry(GEOMETRY_GROUPBOX_POLICY_5_3)
        self.w_checkbox_show_bombard_cannons.stateChanged.connect(self.policy)
        self.w_checkbox_show_siege_towers = QtWidgets.QCheckBox("Siege Tower", self)
        self.w_checkbox_show_siege_towers.setGeometry(GEOMETRY_GROUPBOX_POLICY_5_4)
        self.w_checkbox_show_siege_towers.stateChanged.connect(self.policy)


        self.w_checkbox_show_war_ships = QtWidgets.QCheckBox("War Ships", self)
        self.w_checkbox_show_war_ships.setGeometry(GEOMETRY_GROUPBOX_POLICY_6_0)
        self.w_checkbox_show_war_ships.stateChanged.connect(self.policy)
        self.w_checkbox_show_fire_ships = QtWidgets.QCheckBox("Fire Ships", self)
        self.w_checkbox_show_fire_ships.setGeometry(GEOMETRY_GROUPBOX_POLICY_6_1)
        self.w_checkbox_show_fire_ships.stateChanged.connect(self.policy)
        self.w_checkbox_show_demolition_ships = QtWidgets.QCheckBox("Demo. Ships", self)
        self.w_checkbox_show_demolition_ships.setGeometry(GEOMETRY_GROUPBOX_POLICY_6_2)
        self.w_checkbox_show_demolition_ships.stateChanged.connect(self.policy)
        self.w_checkbox_show_cannon_galleons = QtWidgets.QCheckBox("Cannon Gal.", self)
        self.w_checkbox_show_cannon_galleons.setGeometry(GEOMETRY_GROUPBOX_POLICY_6_3)
        self.w_checkbox_show_cannon_galleons.stateChanged.connect(self.policy)
        self.w_checkbox_show_unique_unit_ships = QtWidgets.QCheckBox("Unique Ships", self)
        self.w_checkbox_show_unique_unit_ships.setGeometry(GEOMETRY_GROUPBOX_POLICY_6_4)
        self.w_checkbox_show_unique_unit_ships.stateChanged.connect(self.policy)

        self.w_checkbox_show_petards = QtWidgets.QCheckBox("Petards", self)
        self.w_checkbox_show_petards.setGeometry(GEOMETRY_GROUPBOX_POLICY_7_0)
        self.w_checkbox_show_petards.stateChanged.connect(self.policy)
        self.w_checkbox_show_trebuchets = QtWidgets.QCheckBox("Trebuchets", self)
        self.w_checkbox_show_trebuchets.setGeometry(GEOMETRY_GROUPBOX_POLICY_7_1)
        self.w_checkbox_show_trebuchets.stateChanged.connect(self.policy)
        self.w_checkbox_show_unique_units = QtWidgets.QCheckBox("Unique Units", self)
        self.w_checkbox_show_unique_units.setGeometry(GEOMETRY_GROUPBOX_POLICY_7_2)
        self.w_checkbox_show_unique_units.stateChanged.connect(self.policy)
        self.w_checkbox_show_monks = QtWidgets.QCheckBox("Monks", self)
        self.w_checkbox_show_monks.setGeometry(GEOMETRY_GROUPBOX_POLICY_7_3)
        self.w_checkbox_show_monks.stateChanged.connect(self.policy)
        self.w_checkbox_show_transport_ships = QtWidgets.QCheckBox("Transport S.", self)
        self.w_checkbox_show_transport_ships.setGeometry(GEOMETRY_GROUPBOX_POLICY_7_4)
        self.w_checkbox_show_transport_ships.stateChanged.connect(self.policy)

        self.w_checkbox_show_all_buildings = QtWidgets.QCheckBox("All Buildings", self)
        self.w_checkbox_show_all_buildings.setGeometry(GEOMETRY_GROUPBOX_POLICY_8_0)
        self.w_checkbox_show_all_buildings.stateChanged.connect(self.policy)
        self.w_checkbox_show_town_centers = QtWidgets.QCheckBox("Town Center", self)
        self.w_checkbox_show_town_centers.setGeometry(GEOMETRY_GROUPBOX_POLICY_8_1)
        self.w_checkbox_show_town_centers.stateChanged.connect(self.policy)
        self.w_checkbox_show_lumber_camps = QtWidgets.QCheckBox("Lumber C.", self)
        self.w_checkbox_show_lumber_camps.setGeometry(GEOMETRY_GROUPBOX_POLICY_8_2)
        self.w_checkbox_show_lumber_camps.stateChanged.connect(self.policy)
        self.w_checkbox_show_mining_camps = QtWidgets.QCheckBox("Mining C.", self)
        self.w_checkbox_show_mining_camps.setGeometry(GEOMETRY_GROUPBOX_POLICY_8_3)
        self.w_checkbox_show_mining_camps.stateChanged.connect(self.policy)
        self.w_checkbox_show_mills = QtWidgets.QCheckBox("Mills", self)
        self.w_checkbox_show_mills.setGeometry(GEOMETRY_GROUPBOX_POLICY_8_4)
        self.w_checkbox_show_mills.stateChanged.connect(self.policy)

        self.w_checkbox_show_barracks = QtWidgets.QCheckBox("Barracks", self)
        self.w_checkbox_show_barracks.setGeometry(GEOMETRY_GROUPBOX_POLICY_9_0)
        self.w_checkbox_show_barracks.stateChanged.connect(self.policy)
        self.w_checkbox_show_archery_ranges = QtWidgets.QCheckBox("Archery R.", self)
        self.w_checkbox_show_archery_ranges.setGeometry(GEOMETRY_GROUPBOX_POLICY_9_1)
        self.w_checkbox_show_archery_ranges.stateChanged.connect(self.policy)
        self.w_checkbox_show_stables = QtWidgets.QCheckBox("Stables", self)
        self.w_checkbox_show_stables.setGeometry(GEOMETRY_GROUPBOX_POLICY_9_2)
        self.w_checkbox_show_stables.stateChanged.connect(self.policy)
        self.w_checkbox_show_siege_workshops = QtWidgets.QCheckBox("Siege W.", self)
        self.w_checkbox_show_siege_workshops.setGeometry(GEOMETRY_GROUPBOX_POLICY_9_3)
        self.w_checkbox_show_siege_workshops.stateChanged.connect(self.policy)
        self.w_checkbox_show_monastries = QtWidgets.QCheckBox("Monastries", self)
        self.w_checkbox_show_monastries.setGeometry(GEOMETRY_GROUPBOX_POLICY_9_4)
        self.w_checkbox_show_monastries.stateChanged.connect(self.policy)
        
        self.w_checkbox_show_castles = QtWidgets.QCheckBox("Castles", self)
        self.w_checkbox_show_castles.setGeometry(GEOMETRY_GROUPBOX_POLICY_10_0)
        self.w_checkbox_show_castles.stateChanged.connect(self.policy)
        self.w_checkbox_show_docks = QtWidgets.QCheckBox("Docks", self)
        self.w_checkbox_show_docks.setGeometry(GEOMETRY_GROUPBOX_POLICY_10_1)
        self.w_checkbox_show_docks.stateChanged.connect(self.policy)
        self.w_checkbox_show_blacksmiths = QtWidgets.QCheckBox("Blacksmiths", self)
        self.w_checkbox_show_blacksmiths.setGeometry(GEOMETRY_GROUPBOX_POLICY_10_2)
        self.w_checkbox_show_blacksmiths.stateChanged.connect(self.policy)            
        self.w_checkbox_show_universities = QtWidgets.QCheckBox("Universities", self)
        self.w_checkbox_show_universities.setGeometry(GEOMETRY_GROUPBOX_POLICY_10_3)
        self.w_checkbox_show_universities.stateChanged.connect(self.policy)
        self.w_checkbox_show_markets = QtWidgets.QCheckBox("Markets", self)
        self.w_checkbox_show_markets.setGeometry(GEOMETRY_GROUPBOX_POLICY_10_4)
        self.w_checkbox_show_markets.stateChanged.connect(self.policy)

        self.w_checkbox_show_towers = QtWidgets.QCheckBox("Towers", self)
        self.w_checkbox_show_towers.setGeometry(GEOMETRY_GROUPBOX_POLICY_11_0)
        self.w_checkbox_show_towers.stateChanged.connect(self.policy)
        self.w_checkbox_show_slingers = QtWidgets.QCheckBox("Slingers", self)
        self.w_checkbox_show_slingers.setGeometry(GEOMETRY_GROUPBOX_POLICY_11_1)
        self.w_checkbox_show_slingers.stateChanged.connect(self.policy)
        self.w_checkbox_show_livestock = QtWidgets.QCheckBox("Livestock", self)
        self.w_checkbox_show_livestock.setGeometry(GEOMETRY_GROUPBOX_POLICY_11_2)
        self.w_checkbox_show_livestock.stateChanged.connect(self.policy)            
        self.w_checkbox_show_gates = QtWidgets.QCheckBox("Gates", self)
        self.w_checkbox_show_gates.setGeometry(GEOMETRY_GROUPBOX_POLICY_11_3)
        self.w_checkbox_show_gates.stateChanged.connect(self.policy)
        self.w_checkbox_show_walls = QtWidgets.QCheckBox("Walls", self)
        self.w_checkbox_show_walls.setGeometry(GEOMETRY_GROUPBOX_POLICY_11_4)
        self.w_checkbox_show_walls.stateChanged.connect(self.policy)

        self.w_button_remove = QtWidgets.QPushButton("Remove", self)
        self.w_button_remove.setGeometry(GEOMETRY_REMOVE_BUTTON)
        self.w_button_remove.clicked.connect(self.remove)



        ###############################################################################################################################################
        ###############################################################################################################################################
        # FILTERS
        self.w_groupbox_filter = QtWidgets.QGroupBox("Filters", self)
        self.w_groupbox_filter.setGeometry(GEMOETRY_GROUPBOX_FILTER)

        
        self.w_label_filter_min_hp = QtWidgets.QLabel("Minimum Unit HP", self)
        self.w_label_filter_min_hp.setGeometry(GEMOETRY_GROUPBOX_FILTER_0_0)
        self.w_text_hp_min = QtWidgets.QSpinBox(self)
        self.w_text_hp_min.setGeometry(GEMOETRY_GROUPBOX_FILTER_0_1)
        self.w_text_hp_min.setMaximum(100)
        self.w_text_hp_min.setSuffix(" %")

        self.w_label_filter_max_hp = QtWidgets.QLabel("Maximum Unit HP", self)
        self.w_label_filter_max_hp.setGeometry(GEMOETRY_GROUPBOX_FILTER_1_0)
        self.w_text_hp_max = QtWidgets.QSpinBox(self)
        self.w_text_hp_max.setGeometry(GEMOETRY_GROUPBOX_FILTER_1_1)
        self.w_text_hp_max.setMaximum(100)
        self.w_text_hp_max.setSuffix(" %")
        self.w_text_hp_max.setValue(self.w_text_hp_max.maximum())

        self.w_label_filter_min_time = QtWidgets.QLabel("Minimum Idle Time", self)
        self.w_label_filter_min_time.setGeometry(GEMOETRY_GROUPBOX_FILTER_2_0)
        self.w_text_idle_min = QtWidgets.QSpinBox(self)
        self.w_text_idle_min.setGeometry(GEMOETRY_GROUPBOX_FILTER_2_1)
        self.w_text_idle_min.setMaximum(99999)
        self.w_text_idle_min.setSuffix(" seconds")

        self.w_filter_max_time = QtWidgets.QLabel("Maximum Idle Time", self)
        self.w_filter_max_time.setGeometry(GEMOETRY_GROUPBOX_FILTER_3_0)
        self.w_text_idle_max = QtWidgets.QSpinBox(self)
        self.w_text_idle_max.setGeometry(GEMOETRY_GROUPBOX_FILTER_3_1)
        self.w_text_idle_max.setMaximum(99999)
        self.w_text_idle_max.setSuffix(" seconds")
        self.w_text_idle_max.setValue(self.w_text_idle_max.maximum())

        """
        self.w_filter_idle = QtWidgets.QCheckBox("Idle", self)
        self.w_filter_idle.setGeometry(GEMOETRY_GROUPBOX_FILTER_4_0)
        self.w_filter_idle.setTristate(True)
        self.w_filter_idle.stateChanged.connect(self.policy)
        """

        self.w_filter_training = QtWidgets.QCheckBox("Training", self)
        self.w_filter_training.setGeometry(GEMOETRY_GROUPBOX_FILTER_5_0)
        self.w_filter_training.setTristate(True)
        self.w_filter_training.nextCheckState()
        self.w_filter_training.stateChanged.connect(self.policy)

        self.w_filter_researching = QtWidgets.QCheckBox("Researching", self)
        self.w_filter_researching.setGeometry(GEMOETRY_GROUPBOX_FILTER_5_1)
        self.w_filter_researching.setTristate(True)
        self.w_filter_researching.nextCheckState()
        self.w_filter_researching.stateChanged.connect(self.policy)

        self.w_filter_constucted = QtWidgets.QCheckBox("Constructing", self)
        self.w_filter_constucted.setGeometry(GEMOETRY_GROUPBOX_FILTER_6_0)
        self.w_filter_constucted.setTristate(True)
        self.w_filter_constucted.nextCheckState()
        self.w_filter_constucted.stateChanged.connect(self.policy)

        self.w_filter_selected = QtWidgets.QCheckBox("Selected", self)
        self.w_filter_selected.setGeometry(GEMOETRY_GROUPBOX_FILTER_6_1)
        self.w_filter_selected.setTristate(True)
        self.w_filter_selected.nextCheckState()
        self.w_filter_selected.stateChanged.connect(self.policy)
                
        self.w_filter_group0 = QtWidgets.QCheckBox("In Group 0", self)
        self.w_filter_group0.setGeometry(GEMOETRY_GROUPBOX_FILTER_7_0)
        self.w_filter_group0.setTristate(True)
        self.w_filter_group0.nextCheckState()
        self.w_filter_group0.stateChanged.connect(self.policy)
        
        self.w_filter_group1 = QtWidgets.QCheckBox("In Group 1", self)
        self.w_filter_group1.setGeometry(GEMOETRY_GROUPBOX_FILTER_8_0)
        self.w_filter_group1.setTristate(True)
        self.w_filter_group1.nextCheckState()
        self.w_filter_group1.stateChanged.connect(self.policy)
        
        self.w_filter_group2 = QtWidgets.QCheckBox("In Group 2", self)
        self.w_filter_group2.setGeometry(GEMOETRY_GROUPBOX_FILTER_9_0)
        self.w_filter_group2.setTristate(True)
        self.w_filter_group2.nextCheckState()
        self.w_filter_group2.stateChanged.connect(self.policy)
        
        self.w_filter_group3 = QtWidgets.QCheckBox("In Group 3", self)
        self.w_filter_group3.setGeometry(GEMOETRY_GROUPBOX_FILTER_10_0)
        self.w_filter_group3.setTristate(True)
        self.w_filter_group3.nextCheckState()
        self.w_filter_group3.stateChanged.connect(self.policy)
        
        self.w_filter_group4 = QtWidgets.QCheckBox("In Group 4", self)
        self.w_filter_group4.setGeometry(GEMOETRY_GROUPBOX_FILTER_11_0)
        self.w_filter_group4.setTristate(True)
        self.w_filter_group4.nextCheckState()
        self.w_filter_group4.stateChanged.connect(self.policy)
        
        self.w_filter_group5 = QtWidgets.QCheckBox("In Group 5", self)
        self.w_filter_group5.setGeometry(GEMOETRY_GROUPBOX_FILTER_7_1)
        self.w_filter_group5.setTristate(True)
        self.w_filter_group5.nextCheckState()
        self.w_filter_group5.stateChanged.connect(self.policy)
        
        self.w_filter_group6 = QtWidgets.QCheckBox("In Group 6", self)
        self.w_filter_group6.setGeometry(GEMOETRY_GROUPBOX_FILTER_8_1)
        self.w_filter_group6.setTristate(True)
        self.w_filter_group6.nextCheckState()
        self.w_filter_group6.stateChanged.connect(self.policy)
        
        self.w_filter_group7 = QtWidgets.QCheckBox("In Group 7", self)
        self.w_filter_group7.setGeometry(GEMOETRY_GROUPBOX_FILTER_9_1)
        self.w_filter_group7.setTristate(True)
        self.w_filter_group7.nextCheckState()
        self.w_filter_group7.stateChanged.connect(self.policy)
        
        self.w_filter_group8 = QtWidgets.QCheckBox("In Group 8", self)
        self.w_filter_group8.setGeometry(GEMOETRY_GROUPBOX_FILTER_10_1)
        self.w_filter_group8.setTristate(True)
        self.w_filter_group8.nextCheckState()
        self.w_filter_group8.stateChanged.connect(self.policy)
        
        self.w_filter_group9 = QtWidgets.QCheckBox("In Group 9", self)
        self.w_filter_group9.setGeometry(GEMOETRY_GROUPBOX_FILTER_11_1)
        self.w_filter_group9.setTristate(True)
        self.w_filter_group9.nextCheckState()
        self.w_filter_group9.stateChanged.connect(self.policy)

    def remove(self):
        if self.icon_list is not None:
            self.icon_list.deleteLater()
        self.deleteLater()
        if self.parent.overlay is not None:
            if self in self.parent.overlay.widgets:
                del self.parent.overlay.widgets[self]

    def set_movable(self):
        if self.icon_list is not None:
            self.icon_list.set_movable(self.w_checkbox_movable.isChecked())
            self.icon_list.raise_()

    def set_hidden(self):
        if self.icon_list is not None:
            if self.w_checkbox_hidden.isChecked():
                self.icon_list.setVisible(False)
            else:
                self.icon_list.setVisible(True)
                #self.icon_list.show()

    def rename_tab(self):
        for index in range(self.parent.w_tabs_settings.count()):
            if self == self.parent.w_tabs_settings.widget(index):
                self.parent.w_tabs_settings.setTabText(index, self.w_text_name.text())

    def lock_villagers(self, boolean):
        self.w_checkbox_show_food_vills.setEnabled(boolean)
        self.w_checkbox_show_wood_vills.setEnabled(boolean)
        self.w_checkbox_show_gold_vills.setEnabled(boolean)
        self.w_checkbox_show_stone_vills.setEnabled(boolean)

    def lock_civilians(self, boolean):
        self.lock_villagers(boolean)
        self.w_checkbox_show_trade_units.setEnabled(boolean)
        self.w_checkbox_show_fish_ships.setEnabled(boolean)
        self.w_checkbox_show_villagers.setEnabled(boolean)


    def lock_military(self, boolean):
        self.w_checkbox_show_swordsmen.setEnabled(boolean)
        self.w_checkbox_show_pikemen.setEnabled(boolean)
        self.w_checkbox_show_eagles.setEnabled(boolean)
        self.w_checkbox_show_huskarls.setEnabled(boolean)
        self.w_checkbox_show_condottieros.setEnabled(boolean)
        self.w_checkbox_show_light_cavalry.setEnabled(boolean)
        self.w_checkbox_show_heavy_cavalry.setEnabled(boolean)
        self.w_checkbox_show_camels.setEnabled(boolean)
        self.w_checkbox_show_tarkans.setEnabled(boolean)
        self.w_checkbox_show_slingers.setEnabled(boolean)
        self.w_checkbox_show_archers.setEnabled(boolean)
        self.w_checkbox_show_skirmishers.setEnabled(boolean)
        self.w_checkbox_show_cavalry_archers.setEnabled(boolean)
        self.w_checkbox_show_genitours.setEnabled(boolean)
        self.w_checkbox_show_hand_cannoneers.setEnabled(boolean)
        self.w_checkbox_show_siege_rams.setEnabled(boolean)
        self.w_checkbox_show_onagers.setEnabled(boolean)
        self.w_checkbox_show_scorpions.setEnabled(boolean)
        self.w_checkbox_show_bombard_cannons.setEnabled(boolean)
        self.w_checkbox_show_siege_towers.setEnabled(boolean)
        self.w_checkbox_show_war_ships.setEnabled(boolean)
        self.w_checkbox_show_fire_ships.setEnabled(boolean)
        self.w_checkbox_show_demolition_ships.setEnabled(boolean)
        self.w_checkbox_show_cannon_galleons.setEnabled(boolean)
        self.w_checkbox_show_unique_unit_ships.setEnabled(boolean)
        self.w_checkbox_show_petards.setEnabled(boolean)
        self.w_checkbox_show_trebuchets.setEnabled(boolean)
        self.w_checkbox_show_unique_units.setEnabled(boolean)
        self.w_checkbox_show_monks.setEnabled(boolean)
        self.w_checkbox_show_battle_elephants.setEnabled(boolean)
        
    def lock_units(self, boolean):
        self.w_checkbox_show_transport_ships.setEnabled(boolean)
        self.w_checkbox_show_civilians.setEnabled(boolean)
        self.lock_civilians(boolean)
        self.w_checkbox_show_military.setEnabled(boolean)
        self.lock_military(boolean)
        self.w_checkbox_show_livestock.setEnabled(boolean)

    def lock_buildings(self, boolean):
        self.w_checkbox_show_town_centers.setEnabled(boolean)
        self.w_checkbox_show_lumber_camps.setEnabled(boolean)
        self.w_checkbox_show_mining_camps.setEnabled(boolean)
        self.w_checkbox_show_mills.setEnabled(boolean)
        self.w_checkbox_show_barracks.setEnabled(boolean)
        self.w_checkbox_show_archery_ranges.setEnabled(boolean)
        self.w_checkbox_show_stables.setEnabled(boolean)
        self.w_checkbox_show_siege_workshops.setEnabled(boolean)
        self.w_checkbox_show_monastries.setEnabled(boolean)
        self.w_checkbox_show_castles.setEnabled(boolean)
        self.w_checkbox_show_docks.setEnabled(boolean)
        self.w_checkbox_show_blacksmiths.setEnabled(boolean)
        self.w_checkbox_show_universities.setEnabled(boolean)
        self.w_checkbox_show_markets.setEnabled(boolean)
        self.w_checkbox_show_towers.setEnabled(boolean)
        self.w_checkbox_show_gates.setEnabled(boolean)
        self.w_checkbox_show_walls.setEnabled(boolean)

    def create_set(self):
        result = set()
        try:
            player = self.parent.game.pov
        except AttributeError:
            return result
        if self.w_checkbox_show_all_units.isChecked():
            result.update(set(player.units))
        if self.w_checkbox_show_civilians.isChecked():
            result.update(set(player.civilians))
        if self.w_checkbox_show_villagers.isChecked():
            result.update(set(player.villagers))
        if self.w_checkbox_show_military.isChecked():
            result.update(set(player.military))
        if self.w_checkbox_show_trade_units.isChecked():
            result.update(set(player.trade))
        if self.w_checkbox_show_food_vills.isChecked():
            result.update(set(player.vill_food))
        if self.w_checkbox_show_wood_vills.isChecked():
            result.update(set(player.vill_wood))
        if self.w_checkbox_show_gold_vills.isChecked():
            result.update(set(player.vill_gold))
        if self.w_checkbox_show_stone_vills.isChecked():
            result.update(set(player.vill_stone))
        if self.w_checkbox_show_fish_ships.isChecked():
            result.update(set(player.fish))
        if self.w_checkbox_show_monastries.isChecked():
            result.update(set(player.monastery))
        if self.w_checkbox_show_stables.isChecked():
            result.update(set(player.stables))
        if self.w_checkbox_show_archery_ranges.isChecked():
            result.update(set(player.archery))
        if self.w_checkbox_show_barracks.isChecked():
            result.update(set(player.barracks))
        if self.w_checkbox_show_siege_workshops.isChecked():
            result.update(set(player.siege))
        if self.w_checkbox_show_castles.isChecked():
            result.update(set(player.castle))
        if self.w_checkbox_show_docks.isChecked():
            result.update(set(player.docks))
        if self.w_checkbox_show_lumber_camps.isChecked():
            result.update(set(player.lumber_camps))
        if self.w_checkbox_show_mining_camps.isChecked():
            result.update(set(player.mining_camps))
        if self.w_checkbox_show_mills.isChecked():
            result.update(set(player.mill))
        if self.w_checkbox_show_markets.isChecked():
            result.update(set(player.market))
        if self.w_checkbox_show_blacksmiths.isChecked():
            result.update(set(player.blacksmiths))
        if self.w_checkbox_show_universities.isChecked():
            result.update(set(player.university))
        if self.w_checkbox_show_town_centers.isChecked():
            result.update(set(player.town_centers))
        if self.w_checkbox_show_towers.isChecked():
            result.update(set(player.towers))
        if self.w_checkbox_show_all_buildings.isChecked():
            result.update(set(player.buildings_all))
        if self.w_checkbox_show_gates.isChecked():
            result.update(set(player.gates))
        if self.w_checkbox_show_walls.isChecked():
            result.update(set(player.walls))
        if self.w_checkbox_show_swordsmen.isChecked():
            result.update(set(player.swordsmen))
        if self.w_checkbox_show_pikemen.isChecked():
            result.update(set(player.pikemen))
        if self.w_checkbox_show_eagles.isChecked():
            result.update(set(player.eagles))
        if self.w_checkbox_show_huskarls.isChecked():
            result.update(set(player.huskarls))
        if self.w_checkbox_show_condottieros.isChecked():
            result.update(set(player.condottieros))
        if self.w_checkbox_show_light_cavalry.isChecked():
            result.update(set(player.light_cavalry))
        if self.w_checkbox_show_heavy_cavalry.isChecked():
            result.update(set(player.heavy_cavalry))
        if self.w_checkbox_show_camels.isChecked():
            result.update(set(player.camels))
        if self.w_checkbox_show_tarkans.isChecked():
            result.update(set(player.tarkans))
        if self.w_checkbox_show_slingers.isChecked():
            result.update(set(player.slingers))
        if self.w_checkbox_show_archers.isChecked():
            result.update(set(player.archers))
        if self.w_checkbox_show_skirmishers.isChecked():
            result.update(set(player.skirmishers))
        if self.w_checkbox_show_cavalry_archers.isChecked():
            result.update(set(player.cavalry_archers))
        if self.w_checkbox_show_genitours.isChecked():
            result.update(set(player.genitours))
        if self.w_checkbox_show_hand_cannoneers.isChecked():
            result.update(set(player.hand_cannoneers))
        if self.w_checkbox_show_siege_rams.isChecked():
            result.update(set(player.siege_rams))
        if self.w_checkbox_show_onagers.isChecked():
            result.update(set(player.onagers))
        if self.w_checkbox_show_scorpions.isChecked():
            result.update(set(player.scorpions))
        if self.w_checkbox_show_bombard_cannons.isChecked():
            result.update(set(player.bombard_cannons))
        if self.w_checkbox_show_siege_towers.isChecked():
            result.update(set(player.siege_towers))
        if self.w_checkbox_show_war_ships.isChecked():
            result.update(set(player.war_ships))
        if self.w_checkbox_show_fire_ships.isChecked():
            result.update(set(player.fire_ships))
        if self.w_checkbox_show_demolition_ships.isChecked():
            result.update(set(player.demolition_ships))
        if self.w_checkbox_show_cannon_galleons.isChecked():
            result.update(set(player.cannon_galleons))
        if self.w_checkbox_show_unique_unit_ships.isChecked():
            result.update(set(player.unique_unit_ships))
        if self.w_checkbox_show_petards.isChecked():
            result.update(set(player.petards))
        if self.w_checkbox_show_trebuchets.isChecked():
            result.update(set(player.trebuchets))
        if self.w_checkbox_show_unique_units.isChecked():
            result.update(set(player.unique_units))
        if self.w_checkbox_show_monks.isChecked():
            result.update(set(player.monks))
        if self.w_checkbox_show_transport_ships.isChecked():
            result.update(set(player.transport_ships))
        if self.w_checkbox_show_livestock.isChecked():
            result.update(set(player.livestock))
        return list(result)

    def filter(self, objects):
        if self.w_filter_constucted.checkState() == 2:
            objects = filter(lambda obj: obj.construction, objects)
        elif self.w_filter_constucted.checkState() == 0:
            objects = filter(lambda obj: not bool(obj.construction), objects)
        if self.w_filter_researching.checkState() == 2:
            objects = filter(lambda obj: obj.research, objects)
        elif self.w_filter_researching.checkState() == 0:
            objects = filter(lambda obj: not bool(obj.research), objects)
        if self.w_filter_training.checkState() == 2:
            objects = filter(lambda obj: obj.training, objects)
        elif self.w_filter_training.checkState() == 0:
            objects = filter(lambda obj: not bool(obj.training), objects)
        if self.w_filter_selected.checkState() == 2:
            objects = filter(lambda obj: obj in self.parent.game.pov.selected, objects)
        elif self.w_filter_selected.checkState() == 0:
            objects = filter(lambda obj: obj not in self.parent.game.pov.selected, objects)
            
        if self.w_filter_group0.checkState() == 2:
            objects = filter(lambda obj: obj.group & 0x400, objects)
        elif self.w_filter_group0.checkState() == 0:
            objects = filter(lambda obj: not obj.group & 0x400, objects)
        if self.w_filter_group1.checkState() == 2:
            objects = filter(lambda obj: obj.group & 0x002, objects)
        elif self.w_filter_group1.checkState() == 0:
            objects = filter(lambda obj: not obj.group & 0x002, objects)
        if self.w_filter_group2.checkState() == 2:
            objects = filter(lambda obj: obj.group & 0x004, objects)
        elif self.w_filter_group2.checkState() == 0:
            objects = filter(lambda obj: not obj.group & 0x004, objects)
        if self.w_filter_group3.checkState() == 2:
            objects = filter(lambda obj: obj.group & 0x008, objects)
        elif self.w_filter_group3.checkState() == 0:
            objects = filter(lambda obj: not obj.group & 0x008, objects)
        if self.w_filter_group4.checkState() == 2:
            objects = filter(lambda obj: obj.group & 0x010, objects)
        elif self.w_filter_group4.checkState() == 0:
            objects = filter(lambda obj: not obj.group & 0x010, objects)
        if self.w_filter_group5.checkState() == 2:
            objects = filter(lambda obj: obj.group & 0x020, objects)
        elif self.w_filter_group5.checkState() == 0:
            objects = filter(lambda obj: not obj.group & 0x020, objects)
        if self.w_filter_group6.checkState() == 2:
            objects = filter(lambda obj: obj.group & 0x040, objects)
        elif self.w_filter_group6.checkState() == 0:
            objects = filter(lambda obj: not obj.group & 0x040, objects)
        if self.w_filter_group7.checkState() == 2:
            objects = filter(lambda obj: obj.group & 0x080, objects)
        elif self.w_filter_group7.checkState() == 0:
            objects = filter(lambda obj: not obj.group & 0x080, objects)
        if self.w_filter_group8.checkState() == 2:
            objects = filter(lambda obj: obj.group & 0x100, objects)
        elif self.w_filter_group8.checkState() == 0:
            objects = filter(lambda obj: not obj.group & 0x100, objects)
        if self.w_filter_group9.checkState() == 2:
            objects = filter(lambda obj: obj.group & 0x200, objects)
        elif self.w_filter_group9.checkState() == 0:
            objects = filter(lambda obj: not obj.group & 0x200, objects)
        objects = filter(lambda obj: obj.hp/obj.udata.max_hp * 100 <= int(self.w_text_hp_max.value()) and  obj.hp/obj.udata.max_hp * 100 >= int(self.w_text_hp_min.value()), objects)
        objects = filter(lambda obj: obj.idle_time/1000 <= int(self.w_text_idle_max.value()) and  obj.idle_time/1000 >= int(self.w_text_idle_min.value()), objects)
        return list(objects)



    def set_aggregate(self):
        boolean = self.w_checkbox_aggregate.isChecked()
        self.w_combo_top_number_aggr.setHidden(not boolean)
        self.w_combo_bottom_number_aggr.setHidden(not boolean)
        self.w_combo_top_number.setHidden(boolean)
        self.w_combo_bottom_number.setHidden(boolean)
        if boolean:
            self.w_combo_timer_number.setCurrentIndex(0)
        self.w_combo_timer_number.setEnabled(not boolean)
        self.policy()
        self.bottom_text_change()
        self.top_text_change()

    def policy(self):
        if self.w_checkbox_show_all_units.isChecked():
            self.lock_units(not self.w_checkbox_show_all_units.isChecked())
        else:
            self.lock_units(not self.w_checkbox_show_all_units.isChecked())
            if self.w_checkbox_show_civilians.isChecked():
                self.lock_civilians(not self.w_checkbox_show_civilians.isChecked())
            elif self.w_checkbox_show_villagers.isChecked():
                self.lock_villagers(not self.w_checkbox_show_villagers.isChecked())
            else:
                self.lock_civilians(not self.w_checkbox_show_civilians.isChecked())
                self.lock_villagers(not self.w_checkbox_show_villagers.isChecked())
            self.lock_military(not self.w_checkbox_show_military.isChecked())
        self.lock_buildings(not self.w_checkbox_show_all_buildings.isChecked())
        if self.icon_list is not None:
            self.icon_list.game_obj_f = self.game_objects

    def aggregate(self, set_):
        if self.w_checkbox_aggregate.isChecked():
            result = defaultdict(list)
            for obj in set_:
                name = obj.udata.name if obj.udata.name != "Trebuchet (Packed)" else "Trebuchet"
                if obj.udata.class_ in ClassData.villagers:
                    name = obj.resource_type + " Villager"
                result[name].append(obj)
            return result
        else:
            return set_


    def game_objects(self):
        return self.aggregate(self.filter(self.create_set()))

    def timer(self):
        name = self.w_combo_timer_number.currentText()
        if self.icon_list is not None:
            self.icon_list.set_y_margin(name != "None")
            self.icon_list.timer_f = {"None"            : lambda obj: "",
                                      "Idle Time"       : lambda obj: str_time(obj.idle_time),
                                      "Total Idle Time" : lambda obj: str_time(obj.idle_total_time),
                                      "Created Time"    : lambda obj: str_time(obj.created_time)}[name]



    def check_stuff_normal(self, dropdown_widget):
        name = dropdown_widget.currentText()
        function = {"None"             : lambda obj: "",
                    "Queue"            : lambda obj: int_to_str(obj.queue.length) if obj.queue else "",
                    "Cooldown"         : lambda obj: str(obj.research.cooldown) if obj.research else (str(obj.training.cooldown) if obj.training else ""),
                    "Carrying Res."    : lambda obj: int_to_str(obj.resource_amount) if obj.resource_amount else "",
                    "Resource Type"    : lambda obj: str(obj.resource_type)[0] if len(obj.resource_type) else "",
                    "Hit Points"       : lambda obj: int_to_str(obj.hp) if obj.hp else "",
                    "Maximal HP"       : lambda obj: int_to_str(obj.udata.max_hp) if obj.udata.max_hp else "",
                    "Attack"           : lambda obj: int_to_str(get_attack(obj)) if obj.udata.attack else "",
                    "Armor"            : lambda obj: get_armors(obj) if obj.udata.armor else "",
                    "Garrisoned Units" : lambda obj: int_to_str(len(obj.garrison)) if obj.garrison else "",
                    "Max. Garrison"    : lambda obj: int_to_str(obj.udata.max_garrison) if obj.udata.max_garrison else ""}[name]
        return function


    def check_stuff_aggr(self, dropdown_widget):
        name = dropdown_widget.currentText()
        function = {"None"             : lambda obj: "",
                    "Units Count"      : lambda obj: int_to_str(len(obj.list)),
                    "Sel. units cnt."  : lambda obj: int_to_str(len(list(filter(lambda r: r in r.owner.selected, obj.list))), allow_zero=True),
                    "Carrying Res."    : lambda obj: int_to_str(sum(map(lambda o: o.resource_amount, obj.list)), allow_zero=True),
                    "Resource Type"    : lambda obj: get_res_type_from_list(obj.list),
                    "Hit Points"       : lambda obj: int_to_str(sum(map(lambda o: o.hp, obj.list))),
                    "Maximal HP"       : lambda obj: int_to_str(obj.udata.max_hp * len(obj.list), allow_zero=True),
                    "Attack"           : lambda obj: int_to_str(get_attack(obj) * len(obj.list), allow_zero=True),
                    "Armor"            : lambda obj: int_to_str(get_armor(obj) * len(obj.list), allow_zero=True),
                    "Pierce Armor"     : lambda obj: int_to_str(get_pierce_armor(obj) * len(obj.list), allow_zero=True),
                    "Garrisoned Units" : lambda obj: int_to_str(sum(map(lambda o: len(o.garrison), obj.list))),
                    "Max. Garrison"    : lambda obj: int_to_str(obj.udata.max_garrison * len(obj.list)),
                    "Idle Units"       : lambda obj: int_to_str(len(list(filter(lambda o: o.idle, obj.list))))}[name]
        return function

    def bottom_text_change(self):
        if self.icon_list is not None:
            if self.w_checkbox_aggregate.isChecked():
                self.icon_list.bottom_text_f = self.check_stuff_aggr(self.w_combo_bottom_number_aggr)
            else:
                # normal
                self.icon_list.bottom_text_f = self.check_stuff_normal(self.w_combo_bottom_number)

    def top_text_change(self):
        if self.icon_list is not None:
            if self.w_checkbox_aggregate.isChecked():
                self.icon_list.top_text_f = self.check_stuff_aggr(self.w_combo_top_number_aggr)
            else:
                # Normal mode
                self.icon_list.top_text_f = self.check_stuff_normal(self.w_combo_top_number)

    def blink(self):
        if self.icon_list is not None:
            self.icon_list.max_blink = self.w_text_idle_time_for_blinkin.value()

    def pulse(self):
        if self.icon_list is not None:
            self.icon_list.max_pulse = self.w_text_idle_time_for_pulsing.value()

    def bind_widget(self, widget):
        self.icon_list = widget
        self.policy()
        self.top_text_change()
        self.bottom_text_change()
        self.blink()
        self.pulse()
        self.timer()
        
    def update_overlay_widget(self):
        self.icon_list.update()





if __name__ == '__main__':
    import bartender
        

