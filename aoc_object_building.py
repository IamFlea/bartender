#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" aoc_object_building.py: gets object data of the building from the game """ 

from pymemory import pymemory as pm
from aoc_object_building_research import BuildingResearch
from aoc_object_building_queue import UnitQueue
from aoc_object_building_training import Training
from aoc_object_unit import *

from aoc_time import *

class Building(Unit): 
    """ INHERITS: Building inherits Unit which inherits Primitive
    Sets `owner.housed` 
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
            ---
            research  BuildingResearch class, see file `aoc_object_building_research.py`
            training  Training class, see file `aoc_object_building_training.py`
            queue     UnitQueue class, see file `aoc_object_queue.py`
            construction The time of the construction.  
                         If the building is attacked during the construction, then the time might give a wrong data. 
                         Its set to infinity if the building is not constructed by any villager. 
        Protected 
            _prev_hp_ Previous HP (Used for calculations between the iterations)
            _tmp_constr_ Previous construction time. 
    Methods
        Public
            __init__(ptr, owner, udata)  Construcotr
            update()                     Call this for updating new values. 
        Protected
            _check_garrison_()           Fills self.garrison
            _check_idle_()               Sets `self.idle` based on the graphics
            _check_idle_time_()          Calculates idle times of the unit if `self.idle` is set 
            _check_construction_()       Checks construction.
    """
    def __init__(self, ptr, owner, udata):
        super(Building, self).__init__(ptr, owner, udata)
        self.research = None 
        self.training = None
        self.queue = None
        self.construction = 0.0


    def _check_construction_(self):
        self._tmp_constr_ = self.construction
        # Did not change in time
        if self.hp == self.prev_hp and GTime.time_delta: 
            return float("inf")
        elif GTime.time_delta: # Changed in time
            return int(self.udata.train_time * (self.udata.max_hp - self.hp)/self.udata.max_hp)
        elif self._tmp_constr_:
            return self._tmp_constr_

    def _check_idle_(self):
        # Set variables
        if self.status == 0 and self.udata.max_hp:
            self.construction = self._check_construction_()
        # Check if the building is standing
        if self.status == 2: # Building
            self.research = BuildingResearch(self).create()
            self.queue = UnitQueue(self).create()
            self.training = Training(self).create()
            self.construction = None
        ## Set variables
        self.idle = self.research is None and self.training is None and self.construction is None
        self.owner.housed = self.owner.housed or self.queue and self.training is None
        

    def update(self):
        super(Unit, self).update()
        self._check_garrison_()
        self._check_idle_()
        self._check_idle_time_()    

if __name__ == '__main__':
    import bartender

