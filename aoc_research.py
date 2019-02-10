#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" aoc_research.py: researches """ 
from pymemory import pymemory as pm
from aoc_time import GTime
from collections import defaultdict

class Technology(object):
    """docstring for Technology"""
    def __init__(self, owner, id, icon, time, total_time=None, cooldown=None):
        super(Technology, self).__init__()
        self.update(owner, id, icon, time, total_time, cooldown)

    def update(self, owner, id, icon, time, total_time=None, cooldown=None):
        self.owner = owner
        self.id = id
        self.icon = icon
        self.time = time
        self.total_time = total_time
        self.cooldown = cooldown   
        

class Research(object):
    """
    Attributes
        public
            owner           `Player` struct
            ptr_times       Pointer to timers
            length          Length of research struct (should be constant to all players)
            ptr_researches  Pointer to researches # common to all players
            id_list         Currently researched techs - id list
            dictionary      Currently researched techs - dict
            progression     Currently researched techs - list
            done            Technologies done
        method
            __init__        Construcotr, requires owner (`Player` struct) as argument
            add             Adds an research into the id_list ((called in file `aoc_object_building_research.py`))
            update          Updates times

    """

    RESEARCH_STATE = {
        -1 : "Unavaliable", # it is not in the research tree
        0 : "Avaliable Later", # Unava
        1 : "Avaliable",
        2 : "Researching",
        3 : "Completed"
    }
    RESEARCH_STATE_INDEXES = {
        "Unavaliable" : -1, # it is not in the research tree
        "Avaliable Later" : 0 ,
        "Avaliable" : 1 ,
        "Researching" : 2 ,
        "Completed" : 3
    }

    def __init__(self, owner):
        super(Research, self).__init__()
        self.owner = owner
        ptr = pm.pointer(owner.ptr + 0x1ae8)
        self.ptr_times = pm.pointer(ptr) # struct size: 0x10 
        self.length = pm.int32(ptr + 0x4)
        self.ptr_researches  = pm.pointer(pm.pointer(ptr + 0x8))   # struct size: 0x54 
        self.id_list = []
        self.dictionary = {}
        self.progression = []
        self.done = []
        # self.ptr_researches should be the same address for each plaeyr
        self.update = self.firstUpdate

    def add(self, id):
        if id not in self.id_list:
            self.id_list.append(id)
            
    def firstUpdate(self):

        for id in range(self.length):
            status = pm.int8(self.ptr_times + 0x10 * id + 0x4)
            if status == Research.RESEARCH_STATE_INDEXES["Completed"]:
                icon = pm.int16(self.ptr_researches  + 0x54*id + 0x2C)
                if icon <= 0 or icon > 121:
                    continue
                name = pm.string(pm.pointer(self.ptr_researches  + 0x54*id))
                if "avail" in name or name == "Scorpion":
                    continue

                #if(self.owner.name == "Kova"):
                #    print(name, icon)

                self.done.append(Technology(self.owner, id, icon, GTime.time));
                
                #print(icon)
            #self.done.append(Technology(self.owner, id, icon, GTime.time));
        #exit(1)
        self.update = self.nthUpdate
        self.update()


    def nthUpdate(self):
        for key in self.dictionary:
            self.dictionary[key].delete = True
        delete = []
        for id in self.id_list:
            time = pm.float(self.ptr_times + 0x10 * id)
            #status = pm.int8(self.ptr_times + 0x14 * id)
            total_time = pm.int16(self.ptr_researches + 0x54*id + 0x26)
            icon = pm.int16(self.ptr_researches  + 0x54*id + 0x2C)
            cooldown = total_time - time
            if time == 0.0:
                delete.append(id)
            elif total_time > time:
                if id not in self.dictionary:
                    self.dictionary[id] = Technology(self.owner, id, icon, time, total_time, cooldown)
                else:
                    self.dictionary[id].update(self.owner, id, icon, time, total_time, cooldown)
                self.dictionary[id].delete = False
            else:
                self.done.append(Technology(self.owner, id, icon, GTime.time))
                delete.append(id)
        for id in delete: 
            self.id_list.remove(id)
        delete = []
        for key in self.dictionary:
            if self.dictionary[key].delete:
                delete += [key]
        for key in delete:
            del self.dictionary[key]
        self.progression = list(self.dictionary.values())

if __name__ == '__main__':
    # import bartender
    import aoc_game
    proc_name = "AoK HD.exe"
    pm.load_process(proc_name)
    game = aoc_game.Game()
    if game is not None:
        t = game.update()

    exit(1)
    print(game.pov.researches);
    ##print(game.pov.resources.values[0]) # food
    #print(game.pov.resources.values[1]) # Wood

    p = game.pov  # p = player 
    score = 0
    # Military - Military score is 20% of the resource value (cost) of all enemy units and buildings each player destroyed or converted.
    score += p.resources.values[170]*0.2 # units value razed
    score += p.resources.values[172]*0.2 # buildings value razed
        
    # Economy score is 10% of all resources each player currently has or has paid in tribute,     
    # Reousrces
    score += p.resources.values[0]*0.1 + p.resources.values[1] * 0.1 + p.resources.values[2] *0.1 + p.resources.values[3] *0.1
    # plus 20% of the resource value of surviving units and standing buildings (except Castles or Wonders).  
    score += p.resources.values[164] * 0.2 
    score += p.resources.values[165] * 0.2
    # Units TODO
    
    # Technology score is 20% of the resource value of every technology each player has researched, plus 10 points for every 1% of the map explored.
    score += p.resources.values[99] * 0.2
    # 10 for 1% of the map   Note that this is approximation! It can have numbers after decimal point 91.5%
    score += p.resources.values[22] * 10
    
    #Society score is 20% of the cost of the Castles and Wonders each player has constructed.
    # NONE already calculated in Enconomy??
    score += p.resources.values[184] * 0.2

