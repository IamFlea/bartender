#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" aoc_objects.py: List of player|s objects """ 
from pymemory import pymemory as pm
from pymemory import NullAddress
from aoc_object_consts import SuperclassData
from aoc_object_data import *
from aoc_object_building import *
from aoc_object_unit import *
from aoc_object_primitive import *
from aoc_time import *

class Objects(list):
    """ List of objects 

    Class variable
        _all    Nested dictionary in format:  _all[player][pointer]
                returns [Object, delete] 
        selected  A list of selected objects
        selected_pointer  A list of pointers to objects
    Class function
        create(pointer owner)   returns an object from `_all` if it is found
                                else it creates a new object and put it in the `_all

    Object Attributes
        Public
            ptr       Pointer to the object list structure
            owner     Owner `Player` strucutre
    Object Methods 
        Public
            __init__(ptr, owner) Constructor
            update()  Updates the object list, needs to be called with this: this.update() !!
        Private
            __enter__   Sets all objects in `_all` to be deleted.. # this is lost by update()
            __exit__    Deletes objects `_all` which are marked to be deleted
            
    USAGE
        o = Objects(ptr, player)
        with o: # This clears unused objects in `_all`
            o.update()
    """
    _all = {}
    selected = []
    selected_pointers = []
    def __init__(self, ptr, owner):
        # ptr Pointer to objects
        # owner Player struct
        super(Objects, self).__init__()
        self.ptr = ptr
        self.owner = owner

    def update(self):
        """Creates a list of objects."""
        self.clear() # sucks but ok
        ptr_array = pm.pointer(self.ptr + 0x4)
        length = pm.uint32(self.ptr + 0x8)
        object_pointers = pm.struct(ptr_array, "I"*length)
        length = pm.int8(self.owner.ptr + 0x254)
        Objects.selected_pointers += pm.struct(self.owner.ptr + 0x160, "I" * length)
        for ptr in object_pointers:
            r = Objects._create_(ptr, self.owner)
            if r is not None:
                r.update()
                self.append(r)
                # Appends the object to the list and sets that the object will not be deleted
                Objects._all[self.owner][ptr] = [r, False]
                # adds it into selected objects
                if ptr in Objects.selected_pointers:
                    Objects.selected.append(r)

    def __enter__(self):
        for ptr in Objects._all[self.owner]:
            Objects._all[self.owner][ptr][1] = True
        return self

    def __exit__(self, type, value, traceback):
        delete = []
        for ptr in Objects._all[self.owner]:
            if Objects._all[self.owner][ptr][1]:
                delete += [ptr]
        for ptr in delete:
            del Objects._all[self.owner][ptr]

    def _create_(ptr_object, owner):
        """Creates an element of the list. """
        # Checks if the pointer is correct
        if ptr_object == 0:
            return None
        # Load new data
        try:
            ptr = pm.uint32(ptr_object + 0xC)
            udata = UnitData(pm.pointer(ptr_object + 0xC), owner)
        except: 
            print(f"BEEP - Wrong address obj.udata = {hex(ptr)} (For object: {hex(ptr_object)})")
            return None
        if udata is None:
            return None


        if ptr_object in Objects._all[owner]:
            Objects._all[owner][ptr_object][1] = False
            Objects._all[owner][ptr_object][0].udata = udata
            # Sometimes it might create a new object with the same address!! 
            if pm.int32(ptr_object + 0x8) == Objects._all[owner][ptr_object][0].id:
                return Objects._all[owner][ptr_object][0]
        
        if udata.superclass == SuperclassData.building:
            return Building(ptr_object, owner, udata)
        elif udata.superclass == SuperclassData.combatant:
            return Unit(ptr_object, owner, udata)
        else:
            return Primitive(ptr_object, owner, udata)
        

if __name__ == '__main__':
    import bartender

