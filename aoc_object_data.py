#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" unitdata.py: parsing aoc memory of recordgames by Flea """
from aoc_object_clist import *
from config import ospath


class UnitData(object):
    """ Returns none if the class is annexed building  (Gate is composed of three buldings )
    Metadata of object
    
    Attributes
        public
            ptr     Pointer to `UnitData`
            owner   `Player` structure
            name_id ID of name
            icon    Object icon ID 
            max_hp  Maximal hitpoints
            max_garrison    Maximal amount for garrison
            id      unifies the same objects in the game; e.g. two knights have the same `unit_id` but knight and paladin don't
            class_  categorize properties of units; e.g. knight and a scout is considered as cavalry = `unit_class`
            superclass      determines the type e.g. combatant units, buildings, trees have different superclass between each other
            armor   `Armor` structure - list of tuples [armor, class]
            attack  `Attack` structure - list of tuples [attack, class]
            speed   Speed of the unit
            train_time      Train time  (Also construction time if this is a building)
        private
            __name  Saved name. 
    Properties 
        public
            name    Name of the object
    Methods
        public
            __new__  Shrugs
            __init__ Constructor

    """
    all_names = None

    def __new__(cls, ptr, owner):
        if pm.int16(ptr + 0x4) == SuperclassData.building:
            # Main unit in TC has 4 buildings.. 
            annex = list(pm.struct(ptr + 0x1F4, "hhhh"))
            annex += [pm.int16(ptr + 0x21c)]
            annex = list(filter(lambda x: x != -1, annex))
            if len(annex) == 1:  # part of TC or gate
                return None
        return super(UnitData, cls).__new__(cls)

    def __init__(self, ptr, owner):
        super(UnitData, self).__init__()
        # Save the address
        self.ptr = ptr
        self.owner = owner

        # constants
        self.__name = None
        self.name_id = pm.int32(ptr + 0x8)
        self.icon = pm.int16(ptr + 0x54)
        self.max_hp = pm.int16(ptr + 0x2a)
        self.max_garrison = pm.int16(ptr + 0x30)
        # pointers
        self.id = pm.int16(ptr + 0x12)
        self.class_ = pm.int16(ptr + 0x16)
        self.superclass = pm.int16(ptr + 0x4)
        # But superclass is different for trebuchet in this script for reasons... 
        if self.class_ in ClassData.trebuchets:
            self.superclass = SuperclassData.combatant
        self.armor = Armor(self)
        self.attack = Attack(self)
        self.costs = Costs(self)
        self.speed = 0.0
        self.train_time = 0
        if self.superclass in [SuperclassData.building, SuperclassData.combatant]:
            self.speed = pm.float(ptr + 0xe8)
            self.train_time = pm.int16(ptr + 0x19e)

    @property
    def name(self):
        name_id = str(self.name_id) + " "
        with open(ospath + "/game_strings.txt", encoding="utf8") as file:
            for line in file:
                if line[:len(name_id)] == name_id:
                    return line[len(name_id) + 1:-2]


if __name__ == '__main__':
    pass
    # import aoc_game
