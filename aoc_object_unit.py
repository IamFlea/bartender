#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" aoc_object_unit.py: gets object data of the unit from the game """ 

from pymemory import pymemory as pm
from pymemory import NullAddress
from aoc_object_primitive import *
from aoc_object_data import *
from aoc_object_consts import SuperclassData
from aoc_time import *

class Unit(Primitive): # game obje
    """
    Class variables
        Public
            ResourceTable   Resource table Look-up table
            graphics_data   Graphic data Look-up table 
    Attributes
        Public
            ptr       Pointer to the object
            owner     Owner `Player` strucutre
            udata     Metadata of the object
            id        Game ID of the object, keeps unchanged, new objects get the new ID
            hp        Hit points 
            status    If the object is alive or dead   Alive? = 0; Alive = 2; ?? = 3, destroying 4, died 8, idk 5
                      alive values [0 1 2]
            idle      Boolean - is idle or not
            idle_time Idle time - how long is a unit slacking around?
            idle_total_time Sum of the all slacks of a unit 
            resource  Tuple in the format `(amount, type)` first value is amount of the carrying resources.
                      The second value stands for the type of the resource 1 - wood, 2 - stone, 3 - gold, and the rest values should be food. 
            garrison  List of pointer to garrisoned units 
        Protected 
            _prev_hp_ Previous HP (Used for calculations between the iterations)
    Methods
        Public
            __init__(ptr, owner, udata)  Construcotr
            update()                     Call this for updating new values. 
        Protected
            _check_garrison_()           Fills self.garrison
            _check_idle_()               Sets `self.idle` based on the graphics
            _check_idle_time_()          Calculates idle times of the unit if `self.idle` is set 
    """
    graphics_data = {}
    
    def __init__(self, ptr, owner, udata):
        super(Unit, self).__init__(ptr, owner, udata)
        #self.ptr_graphics = ptr + 0x14 # pointer 
        #self.ptr_status = ptr + 0x4C   # byte

    def _check_garrison_(self):
        garrison = []
        if not self.udata.max_garrison:
            return garrison
        try:
            ptr = pm.pointer(self.ptr + 0x28)
            ptr, cnt = pm.struct(ptr, "II")
            if not ptr:
                return garrison
            arr = pm.struct(ptr, "I"*cnt)
            for ptr in arr:
                udata = UnitData(pm.pointer(ptr + 0xC), self.owner)
                """
                if r is not None:
                    return garrison 
                if udata and udata.superclass == SuperclassData.combatant: # << checks recursion
                    garrison.append(Unit(ptr, self.owner, udata)) # trebuchet shouldnt bug this 
                """
                garrison.append(Unit(ptr, self.owner, udata)) # trebuchet shouldnt bug this 
        except NullAddress:
            return garrison
        self.garrison.clear()
        self.garrison.extend(garrison)

    def _check_idle_(self):
        ## Checking if unit is idle need to write better way 
        # Load pointer
        try:
            pointer = pm.pointer(self.ptr + 0x14)
        except NullAddress:
            print("WARNING aoc_object_unit.py in `_check_idle_(self)`: NULL pointer!")
            self.idle = False
            return
        if pointer in Unit.graphics_data:
            # Is it in look-up table?
            self.idle = Unit.graphics_data[pointer]
        else:
            # Load it inot the lookup table
            try:
                splitted_name = pm.string(pointer+0x50).split("_")
                result = len(splitted_name) > 1 and "FN" in splitted_name[-1] # idle through graphics.. suuucks
                Unit.graphics_data[pointer] = result
                self.idle = result
            except UnicodeDecodeError:
                print("WARNING aoc_object_unit.py in `_check_idle_(self)`: Couldn't parse SLP filename!")
                self.idle = False

    def _check_idle_time_(self):
        if self.idle or (type(self) != Unit and self.construction and self.construction > 1.0):
            self.idle_time += GTime.time_delta
            self.idle_total_time += GTime.time_delta
        else:
            self.idle_time = 0


    def update(self):
        super(Unit, self).update()
        self._check_garrison_()
        self._check_idle_()
        self._check_idle_time_()
        self.group = pm.uint32(self.ptr + 0x158)


if __name__ == '__main__':
    import bartender
