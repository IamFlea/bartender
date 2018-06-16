#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" aoc_object_primitive.py: parsing the most primitive game object """ 
from pymemory import pymemory as pm
from collections import defaultdict

from aoc_time import GTime 
class Primitive(object): # game object
    """
    Class variables
        Public
            ResourceTable   Resource table Look-up table
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
    """

    ResourceTable = defaultdict(lambda: "Food", {
            1: "Wood",
            2: "Stone",
            3: "Gold",
            -1: ""
        }) 

    def __init__(self, ptr, owner, udata): 
        # ptr - pointer to the object
        # owner - Player datastructure who has this unit
        # udata - metadata, see `aoc_object_data.py` 
        super(Primitive, self).__init__()
        self.ptr = ptr
        self.owner = owner
        self.udata = udata
        # Load data
        self.id = pm.int32(ptr + 0x8) # Game ID keeps unchanged, no need for update
        self.hp = pm.float(ptr + 0x34)
        self.status = pm.int8(ptr + 0x4C)
        # Load consts
        self.idle = False
        self.idle_time = 0
        self.idle_total_time = 0
        self.garrison = []
        self.research = None 
        self.training = None
        self.queue = None
        self.construction = None
        self.group = 0
        self.created_time = GTime.time
        self.resource_amount = 0
        self.resource_type = ""
        
    def update(self):
        self.prev_hp = self.hp
        self.hp = pm.float(self.ptr + 0x34)
        self.status = pm.int8(self.ptr + 0x4C)
        self.resource_amount = pm.float(self.ptr + 0x48)
        self.resource_type = Primitive.ResourceTable[pm.int8(self.ptr + 0x50)]
        self.position = pm.struct(self.ptr + 0x3c, "ff")
