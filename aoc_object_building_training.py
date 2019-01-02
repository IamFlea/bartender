#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" aoc_training.py: parsing aoc memory of recordgames by Flea """
from math import isnan

from pymemory import NullAddress
from pymemory import pymemory as pm


class Training(object):
    """Building trianings. 

    Attributes
        public
            building   `Building` strucutre
            icon       Training unit icon ID 
            time       The time spend training
            total_time Time required for training
            cooldown   Remaining time of train
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
        # Building sturcts
        super(Training, self).__init__()
        self.building = building

    def create(self):
        try:
            # load id and time
            ptr = pm.pointer(self.building.ptr + 0x220)
            ptr = pm.pointer(ptr + 0x8)
            ptr = pm.pointer(ptr)
            self.id = pm.int16(ptr + 0x40)
            if self.id > 1402:
                return None
            time = pm.float(ptr + 0x44)
            # Load icon and total time
            ptr = self.building.owner.ptr
            ptr = pm.pointer(ptr + 0x14)
            ptr = pm.pointer(ptr + 0x4 * self.id)
        except NullAddress:
            return None
        self.icon = pm.int16(ptr + 0x54)
        self.total_time = pm.int16(ptr + 0x19e)
        self.time = 1 if isnan(time) else time
        self.cooldown = int(self.total_time - self.time)
        return self

    # self.ptr_training = pm.read_address(ptr + 0x220)


if __name__ == '__main__':
    pass
