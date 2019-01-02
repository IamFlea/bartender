#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" aoc_object_building_research.py: checks building research """
from math import isnan

from pymemory import NullAddress
from pymemory import pymemory as pm


class BuildingResearch(object):
    """ Building researches

    Attributes
        Public
            building   `Buidling` structure
            id         ID of research
            time       The time spend researching
            total_time Time required for research
            cooldown   Remaining time
            icon       Research icon ID
    Methods
        Public
            __init__(building)  Constructor
            create()            Returns None or self with filled attributes. 

    How to use this
        r = Training(building).create()
        if r: 
            print(r.icon, r.id, r.cooldown)
    """

    def __init__(self, building):
        super(BuildingResearch, self).__init__()
        self.building = building
        self.id = -1
        self.icon = 0
        self.time = 0
        self.total_time = 0
        self.cooldown = 0

    def create(self):  # some kind of constructor.. returns None if none research
        try:
            ptr = pm.pointer(self.building.ptr + 0x1f0)
            ptr = pm.pointer(ptr + 0x8)
            ptr = pm.pointer(ptr)
            self.id = pm.int16(ptr + 0x40)
            if self.id > 800:
                return None
            ptr = pm.pointer(self.building.owner.ptr + 0x1ae8)
            time = pm.float(pm.pointer(ptr) + 16 * self.id)
            ptr = pm.pointer(pm.pointer(ptr + 8))
        except NullAddress:
            return None
        self.building.owner.research.add(self.id)
        self.total_time = pm.int16(ptr + 0x54 * self.id + 0x26)
        self.icon = pm.int16(ptr + 0x54 * self.id + 0x2C)
        self.time = self.total_time if isnan(time) else time  # NaN occurs in the end of the research
        self.cooldown = int(self.total_time - self.time)
        # if ptr not in BuildingResearch.log[self.building.owner]:
        #    BuildingResearch.log[self.building.owner].append(self)
        return self


if __name__ == '__main__':
    pass
