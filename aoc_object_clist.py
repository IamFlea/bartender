#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" aoc_object_clist.py: list like classes used in aoc_object_data.py""" 
from pymemory import pymemory as pm
from aoc_object_consts import * 

class cList(list):
    """ List like object. Returns none if superclass is not combatant or building """
    def __new__(self, udata):
        if udata.superclass not in [SuperclassData.combatant, SuperclassData.building]:
            return None

class Armor(cList):
    """ List like object. Returns none if superclass is not combatant or building
    
    List contains armor values in format [class, amount]
    """
    def __init__(self, udata):
        super(Armor, self).__init__()
        cnt = pm.int16(udata.ptr + 0x142)
        ptr = pm.pointer(udata.ptr + 0x144)
        for i in range(cnt):
            self.append(pm.struct(ptr + i*4, "hh"))    

class Attack(cList):
    """ List like object. Returns none if superclass is not combatant or building
    
    List contains armor values in format [class, amount]
    """
    def __init__(self, udata):
        super(Attack, self).__init__()
        self.range = pm.float(udata.ptr + 0x154) 
        self.reload_time = pm.float(udata.ptr + 0x160)
        self.accurancy = pm.int16(udata.ptr + 0x166) 
        cnt = pm.int16(udata.ptr + 0x148)
        ptr = pm.pointer(ptr + 0x14c)
        for i in range(cnt):
            self.append(pm.struct(ptr + i*4, "hh"))

class Costs(cList):
    """ List like object. Returns none if superclass is not combatant or building
    
    List contains cost values in format [type, amount, pay] 
    Length of the list should be lesser than 4. 
    """
    pay = ["Rquired to Train", "Required to Pay"]
    def __init__(self, udata):
        super(Costs, self).__init__()
        r_type, r_amount, r_pay = pm.strct(udata.ptr + 0x18c, "hhh")
        if r_amount != -1:
            self.append((Resources.keys[r_type], r_amount, Costs.pay[r_pay]))

    