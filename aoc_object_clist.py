#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" aoc_object_clist.py: list like classes used in aoc_object_data.py"""
from aoc_object_consts import *
from aoc_resources import Resources
from pymemory import pymemory as pm


class cList(list):
    """ List like object. Returns none if superclass is not combatant or building """

    def __new__(cls, udata):
        if udata.superclass not in [SuperclassData.combatant, SuperclassData.building]:
            return None
        return super(cList, cls).__new__(cls)


class Armor(cList):
    """ List like object. Returns none if superclass is not combatant or building
    
    List contains armor values in format [class, amount]
    """
    BONUS_CLASS = ["0 - Unused", "1 - Infantry", "2 - Turtle Ships", "3 - Base Pierce", "4 - Base Melee",
                   "5 - War Elephants", "6 - Unused", "7 - Unused", "8 - Cavalry", "9 - Unused", "10 - Unused",
                   "11 - All Buildings (except Port)", "12 - Unused", "13 - Stone Defense", "14 - FE Predator Animals",
                   "15 - Archers", "16 - Ships & Camels & Saboteurs", "17 - Rams", "18 - Trees",
                   "19 - Unique Units (except Turtle Ship)", "20 - Siege Weapons", "21 - Standard Buildings",
                   "22 - Walls & Gates", "23 - FE Gunpowder Units", "24 - Boars", "25 - Monks", "26 - Castle",
                   "27 - Spearmen", "28 - Cavalry Archers", "29 - Eagle Warriors", "30 - HD Camels"]

    def __init__(self, udata):
        super(Armor, self).__init__()
        cnt = pm.int16(udata.ptr + 0x142)
        self.displayed = pm.int16(udata.ptr + 0x17C)
        self.displayed_pierce = pm.int16(udata.ptr + 0x1A4)
        if cnt != 0:
            ptr = pm.pointer(udata.ptr + 0x144)
            big_struct = pm.struct(ptr, "hh" * cnt)
            iterator = iter(big_struct)
            self.extend(zip(iterator, iterator))


class Attack(cList):
    """ List like object. Returns none if superclass is not combatant or building
    
    List contains armor values in format [class, amount]
    """
    BONUS_CLASS = ["0 - Unused", "1 - Infantry", "2 - Turtle Ships", "3 - Base Pierce", "4 - Base Melee",
                   "5 - War Elephants", "6 - Unused", "7 - Unused", "8 - Cavalry", "9 - Unused", "10 - Unused",
                   "11 - All Buildings (except Port)", "12 - Unused", "13 - Stone Defense", "14 - FE Predator Animals",
                   "15 - Archers", "16 - Ships & Camels & Saboteurs", "17 - Rams", "18 - Trees",
                   "19 - Unique Units (except Turtle Ship)", "20 - Siege Weapons", "21 - Standard Buildings",
                   "22 - Walls & Gates", "23 - FE Gunpowder Units", "24 - Boars", "25 - Monks", "26 - Castle",
                   "27 - Spearmen", "28 - Cavalry Archers", "29 - Eagle Warriors", "30 - HD Camels"]

    def __init__(self, udata):
        super(Attack, self).__init__()
        self.range = pm.float(udata.ptr + 0x154)
        self.reload_time = pm.float(udata.ptr + 0x160)
        self.accurancy = pm.int16(udata.ptr + 0x166)
        self.displayed = pm.int16(udata.ptr + 0x17e)
        cnt = pm.int16(udata.ptr + 0x148)
        if cnt != 0:
            ptr = pm.pointer(udata.ptr + 0x14c)
            big_struct = pm.struct(ptr, "hh" * cnt)
            iterator = iter(big_struct)
            self.extend(zip(iterator, iterator))


class Costs(cList):
    """ List like object. Returns none if superclass is not combatant or building
    
    List contains cost values in format [type, amount, pay] 
    Length of the list should be lesser than 4. 
    """
    pay = ["Rquired to Train", "Required to Pay"]

    def __init__(self, udata):
        super(Costs, self).__init__()
        r_type, r_amount, r_pay = pm.struct(udata.ptr + 0x18c, "hhh")
        if r_amount != -1:
            self.append((Resources.keys[r_type], r_amount, Costs.pay[r_pay]))


if __name__ == '__main__':
    pass
