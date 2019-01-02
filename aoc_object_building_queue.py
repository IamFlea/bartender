#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" aoc_object_building_queue.py: gets unit queue from a building """
from pymemory import NullAddress
from pymemory import pymemory as pm


class UnitQueue(list):
    """ 
    List of tuples. Each tuple is in format [uid, icon] in which uid stands for `udata.id` and  icon is `udata.icon`
    Attributes
        public 
            building    `Building` structure
            length      Length of queue, same as `len(self)`
    Methods
        public
            __init__(building)  Constructor
            create()            Returns `self` if there is any unit in a queue, else returns None 
    
    How to use this
        q = UnitQueue(building).create()
        if q: 
            print(q.length, q[0])
    """

    def __init__(self, building):
        super(UnitQueue, self).__init__()
        self.building = building

    def create(self):
        self.length = pm.int16(self.building.ptr + 0x21c)
        try:
            ptr = pm.pointer(self.building.ptr + 0x214)
        except NullAddress:
            return None
        while len(self) < self.length:
            uid, units_amount = pm.struct(ptr, "hh")
            for i in range(units_amount):
                try:
                    ptr_icon = self.building.owner.ptr
                    ptr_icon = pm.pointer(ptr_icon + 0x14)
                    ptr_icon = pm.pointer(ptr_icon + 0x4 * uid)
                    icon = pm.int16(ptr_icon + 0x54)
                except NullAddress:
                    return None
                self.append((uid, icon))
            ptr += 4
        return self


# self.building.ptr_queue = ptr + 0x214        # pointer
# self.building.ptr_queue_units = ptr + 0x21C  # word
if __name__ == '__main__':
    pass
