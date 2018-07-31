#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" aoc_game.py: parsing aoc memory of recordgames by Flea """ 
from pymemory import pymemory as pm
from aoc_diplomacy import *
from aoc_resources import *
from aoc_color import *
from aoc_civ import *
from aoc_object_building_research import BuildingResearch
from aoc_object_consts import *
from aoc_objects import Objects
from aoc_research import Research 

class Player(object):
    """ Player strucutre 

    Attributes
        public
            ptr         Pointer to player structure
            name        Name of the player
            diplomacy   Diplomacy struct
            resources   Resources struct
            color       Color struct
            research    Research struct
            objects     List of player's objects (units, buildings, treees whatever)
            log         Some kind of log if diplomacy changed.. # maybe removei t 
            selected    Selected units pointers
            buildings   Buildings 
            farm_reseeds Number of reseeds in a mill
            pov         Boolean

        Public object lists
            buildings_all   All buildings without trebuchets (not a joke, they are implemented as moving building)
            buildings       All buildings without towers, walls, trebuchets 
            units           Units + trebuchets
            civilians       Vills + fishing ships + trades
            villagers       Vills only
            military        Military + transport ship
          Villagers
            vill_wood       Vills marked as Lumberjack
            vill_food       Vills marked as Fisher, Farmer, Hunter, Cannibal
            vill_gold       Vills marked as Gold Miner
            vill_stone      Vills marked as Stone miner
            trade           Trade cogs + trade carts
            fish            Fishing ships
          Buildings
            monastery       Monstry buildings
            stables         Stable buildings 
            archery         Archery Ranges
            barracks        Barracks 
            siege           Siege workshops
            castle          Castles
            docks           Docks
            lumber_camps    Lumbercamps
            mining_camps    Mining camps
            mill            Mills
            market          Markets
            blacksmiths     Blacksmiths
            university      Universities
            town_centers    Town Centers
            towers          Towers
            constructions   Buildings which are under the construction. 
    Methods
        public
            __init__(ptr, number)
                            Creates this object.
                            ptr is a pointer to Player structure
                            number is a number of the player, if none it assumes it is a gaia
            update(market)  Updates all players data 
        private 
            __get_name__    Used for setting `name` attribute 
            __analyze_objects__
                            Fills all the lists

    """
    SINGLE_PLAYER = True
    def __get_name__(number, ptr_ai):
        """ Get players name, if AI grabs """
        ptr = pm.pointer(pm.base_address + 0x006FD02C) 
        ptr = pm.pointer(ptr + 0xA20) 
        ptr = pm.pointer(ptr + 0xD0C) 
        ptr = pm.pointer(ptr + 0xb0 + 0x68*(number-1) + 0xC)
        try:
            name = pm.string(ptr, 32)
        except:
            name = ""
        name = name if name else f"Player #{number}"
        if pm.int32(ptr_ai + 0x8) == 3: 
            name += " [AI]"
        return name

    def __init__(self, ptr, number=None):
        super(Player, self).__init__()
        self.ptr = ptr
        self.name = "Gaia" if number is None else Player.__get_name__(number, ptr) 
        self.pov = False
        self.diplomacy = Diplomacy(self)
        self.resources = Resources(self)
        self.color = Color(self)
        self.civ = Civilization(self)
        self.research = Research(self)
        #self.map = Map(ptr)
        self.objects = Objects(pm.pointer(ptr + 0x18), self)
        self.log = [] 
        #BuildingResearch.log[self] = [] # Better access for researches
        Objects._all[self] = {} # Dictionary of used objects
        self.housed = False
        self.farm_reseeds  = 0
        self.selected = None
        
    def __analyze_objects__(self):
        #import time
        #now = time.time()
        # This algorithms are optimal in the terms of typing... 
        # else it sucks cuy it has a big time complexity, could be reduced 20 times.. 
        self.buildings_all = list(filter(lambda obj: obj.udata.superclass == SuperclassData.building, self.objects)) 
        self.buildings = list(filter(lambda obj: obj.udata.class_ in ClassData.building, self.objects)) # filters walls, gates, twoers.. 
        self.units = list(filter(lambda obj: obj.udata.superclass == SuperclassData.combatant, self.objects))
        # We need to filter units... 
        #self.units = list(filter(lambda obj: obj.status in [0,1,2], self.units)) # meeh  i am lazy to do comparasion logic
        self.civilians = list(filter(lambda obj: obj.udata.class_ in ClassData.civilians, self.units))
        self.villagers = list(filter(lambda obj: obj.udata.class_ in ClassData.villagers, self.civilians))
        self.military = list(filter(lambda obj: obj.udata.class_ in ClassData.military, self.units))
        #self.military = set(self.units) - set(self.civilians)  # counts sheep as military units too hahahha
        #self.pikes = list(filter(lambda obj: obj.udata.class_ == , self.military))
        # Villagers (with idles!)
        self.vill_wood = list(filter(lambda obj: obj.udata.id in IdData.vill_wood, self.villagers))
        self.vill_food = list(filter(lambda obj: obj.udata.id in IdData.vill_food, self.villagers))
        self.vill_gold = list(filter(lambda obj: obj.udata.id in IdData.vill_gold, self.villagers))
        self.vill_stone = list(filter(lambda obj: obj.udata.id in IdData.vill_stone, self.villagers))
        self.trade = list(filter(lambda obj: obj.udata.id in IdData.trade, self.units))
        self.fish = list(filter(lambda obj: obj.udata.id in IdData.fish, self.units))
        # Buildings
        self.monastery = list(filter(lambda obj: obj.udata.id in IdData.monastery, self.buildings))
        self.stables = list(filter(lambda obj: obj.udata.id in IdData.stables, self.buildings))
        self.archery = list(filter(lambda obj: obj.udata.id in IdData.archery, self.buildings))
        self.barracks = list(filter(lambda obj: obj.udata.id in IdData.barracks, self.buildings))
        self.siege = list(filter(lambda obj: obj.udata.id in IdData.siege_workshop, self.buildings))
        self.castle = list(filter(lambda obj: obj.udata.id in IdData.castle, self.buildings))
        self.docks = list(filter(lambda obj: obj.udata.id in IdData.dock, self.buildings))
        self.lumber_camps = list(filter(lambda obj: obj.udata.id in IdData.lumber_camps, self.buildings))
        self.mining_camps = list(filter(lambda obj: obj.udata.id in IdData.mining_camps, self.buildings))
        self.mill = list(filter(lambda obj: obj.udata.id in IdData.mill, self.buildings))
        self.market = list(filter(lambda obj: obj.udata.id in IdData.market, self.buildings))
        self.blacksmiths = list(filter(lambda obj: obj.udata.id in IdData.blacksmiths, self.buildings))
        self.university = list(filter(lambda obj: obj.udata.id in IdData.university, self.buildings))
        self.town_centers = list(filter(lambda obj: obj.udata.id in IdData.town_centers, self.buildings))
        self.towers = list(filter(lambda obj: obj.udata.id in IdData.towers, self.buildings_all))
        self.gates = list(filter(lambda obj: obj.udata.id in IdData.gates, self.buildings_all))
        self.walls = list(filter(lambda obj: obj.udata.id in IdData.walls, self.buildings_all))
        self.swordsmen = list(filter(lambda obj: obj.udata.id in IdData.swordsmen, self.units))
        self.pikemen = list(filter(lambda obj: obj.udata.id in IdData.pikemen, self.units))
        self.eagles = list(filter(lambda obj: obj.udata.id in IdData.eagles, self.units))
        self.huskarls = list(filter(lambda obj: obj.udata.id in IdData.huskarls, self.units))
        self.condottieros = list(filter(lambda obj: obj.udata.id in IdData.condottieros, self.units))
        self.light_cavalry = list(filter(lambda obj: obj.udata.id in IdData.light_cavalry, self.units))
        self.heavy_cavalry = list(filter(lambda obj: obj.udata.id in IdData.heavy_cavalry, self.units))
        self.camels = list(filter(lambda obj: obj.udata.id in IdData.camels, self.units))
        self.tarkans = list(filter(lambda obj: obj.udata.id in IdData.tarkans, self.units))
        self.slingers = list(filter(lambda obj: obj.udata.id in IdData.slingers, self.units))
        self.archers = list(filter(lambda obj: obj.udata.id in IdData.archers, self.units))
        self.skirmishers = list(filter(lambda obj: obj.udata.id in IdData.skirmishers, self.units))
        self.cavalry_archers = list(filter(lambda obj: obj.udata.id in IdData.cavalry_archers, self.units))
        self.genitours = list(filter(lambda obj: obj.udata.id in IdData.genitours, self.units))
        self.hand_cannoneers = list(filter(lambda obj: obj.udata.id in IdData.hand_cannoneers, self.units))
        self.siege_rams = list(filter(lambda obj: obj.udata.id in IdData.rams, self.units))
        self.onagers = list(filter(lambda obj: obj.udata.id in IdData.onagers, self.units))
        self.scorpions = list(filter(lambda obj: obj.udata.id in IdData.scorpions, self.units))
        self.bombard_cannons = list(filter(lambda obj: obj.udata.id in IdData.bombard_cannons, self.units))
        self.siege_towers = list(filter(lambda obj: obj.udata.id in IdData.siege_towers, self.units))
        self.war_ships = list(filter(lambda obj: obj.udata.id in IdData.war_ships, self.units))
        self.fire_ships = list(filter(lambda obj: obj.udata.id in IdData.fire_ships, self.units))
        self.demolition_ships = list(filter(lambda obj: obj.udata.id in IdData.demolition_ships, self.units))
        self.cannon_galleons = list(filter(lambda obj: obj.udata.id in IdData.cannon_galleons, self.units))
        self.unique_unit_ships = list(filter(lambda obj: obj.udata.id in IdData.dock_unique_units, self.units))
        self.petards = list(filter(lambda obj: obj.udata.id in IdData.petards, self.units))
        self.trebuchets = list(filter(lambda obj: obj.udata.id in IdData.trebuchets, self.units))
        self.unique_units = list(filter(lambda obj: obj.udata.id in IdData.caslte_unique_units, self.units))
        self.monks = list(filter(lambda obj: obj.udata.id in IdData.monks, self.units))
        self.transport_ships = list(filter(lambda obj: obj.udata.id in IdData.transport_ships, self.units))
        self.livestock = list(filter(lambda obj: obj.udata.class_ in ClassData.livestock, self.units)) 
        #self.constructions = list(filter(lambda obj: obj.construction, self.buildings_all))
        # get army
        #self.army = {}
        #for unit in self.military:
        #    if unit.udata.id in self.army:
        #        self.army[unit.udata.id] += [unit]
        #    else:
        #        self.army[unit.udata.id] = [unit]
        #print(time.time()-now)
        
    def update(self, market): 
        self.housed = False
        self.diplomacy.update(self.log)
        self.resources.update()
        self.color.update()
        with self.objects:
            if Player.SINGLE_PLAYER:
                if self.pov:
                    self.objects.update()    
            else:
                self.objects.update()
        self.__analyze_objects__()
        self.research.update()
        self.farm_reseeds = pm.int16(self.ptr + 0x2708)
        self.selected = Objects.selected
        #self.selected = [item for item in objects.selected]  # if buggy
        #print(self.selected)

    

        
if __name__ == '__main__' and True:
    import bartender

if __name__ == '__main__' and False:
    from aoc_game import Game 
    proc_name = "AoK HD.exe"
    pm.load_process(proc_name)
    
    game = Game()
    game.update()


