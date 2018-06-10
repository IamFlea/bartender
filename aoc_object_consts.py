#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" aoc_object_consts.py: This file contains lots of constants.""" 

from aoc_object_consts_unit import UNITS

class SuperclassData():
    eye_candy = 10 # gaia objects 
    tree_aok = 15
    animated = 20
    doppelgang = 25
    moving = 30
    actor = 40
    superclass = 50
    projectile = 60
    combatant = 70
    building = 80 # In our case trebuchets are moved in 70 (they are buildings in terms of the game)
    tree_aoe = 90

class ClassData():
    all_str = ["Archer", "Artifact", "Trade Boat", "Building", "Civilian", "Ocean Fish", "Infantry", "Berry Bush", "Stone Mine", "Prey Animal", "Predator Animal", "Miscellaneous", "Cavalry", "Siege Weapon", "Terrain", "Tree", "Tree Stump", "Healer", "Monk", "Trade Cart", "Transport Boat", "Fishing Boat", "Warship", "Conquistador", "War Elephant", "Hero", "Elephant Archer", "Wall", "Phalanx", "Domestic Animal", "Flag", "Deep Sea Fish", "Gold Mine", "Shore Fish", "Cliff", "Petard", "Cavalry Archer", "Doppelganger", "Bird", "Gate", "Salvage Pile", "Resource Pile", "Relic", "Monk with Relic", "Hand Cannoneer", "Two Handed Swordsman", "Pikeman", "Scout", "Ore Mine", "Farm", "Spearman", "Packed Unit", "Tower", "Boarding Boat", "Unpacked Siege Unit", "Ballista", "Raider", "Cavalry Raider", "Livestock", "King", "Misc Building", "Controlled Animal", "Unknown"]
    military_str = ["Archer", "Infantry", "Prey Animal", "Predator Animal", "Cavalry", "Siege Weapon", "Healer", "Monk", "Warship", "Conquistador", "War Elephant", "Hero", "Elephant Archer", "Phalanx", "Petard", "Cavalry Archer", "Salvage Pile", "Resource Pile", "Monk with Relic", "Hand Cannoneer", "Two Handed Swordsman", "Pikeman", "Scout", "Spearman", "Packed Unit", "Boarding Boat", "Unpacked Siege Unit", "Ballista", "Raider", "Cavalry Raider"]
    military = list(map(lambda x, y=all_str : y.index(x), military_str))

    civilians_str = ["Trade Boat", "Civilian", "Trade Cart", "Fishing Boat"]
    civilians_str += ["Transport Boat"] # need to put it somewhere; comment if nessesery
    civilians = list(map(lambda x, y=all_str : y.index(x), civilians_str))
    all_buildings_str = ["Building", "Misc Building", "Gate", "Wall", "Tower", "Farm"]
    all_buildings = list(map(lambda x, y=all_str : y.index(x), all_buildings_str))
    building_str = ["Building"]
    building = list(map(lambda x, y=all_str : y.index(x), building_str))
    trebuchets_str = ["Unpacked Siege Unit", "Packed Unit"]
    trebuchets = list(map(lambda x, y=all_str : y.index(x), trebuchets_str))
    villagers_str = ["Civilian"]
    villagers = list(map(lambda x, y=all_str : y.index(x), villagers_str))
    livestock_str = ["Livestock"]
    livestock = list(map(lambda x, y=all_str : y.index(x), livestock_str))


class IdData():
    ## UNITS
    # -- villagers --
    vill_wood  = UNITS['Lumberjack']
    vill_food  = UNITS['Forager'] + UNITS['Hunter'] + UNITS['Farmer'] + UNITS['Fisherman'] + UNITS['Shepherd'] 
    vill_stone = UNITS['Stone Miner']
    vill_gold  = UNITS['Gold Miner']
    vill_builder = UNITS['Builder']
    vill_repairer = UNITS['Repairer']
    vill_none = UNITS['Villager'] # Idle vill 

    fish = UNITS['Fishing Ship']
    trade = UNITS['Trade Cart'] + UNITS['Trade Cog']
    # --- military ---

    # barracks
    swordsmen = UNITS['Militia'] + UNITS['Man-at-Arms'] + UNITS['Long Swordsman'] + UNITS['Two-Handed Swordsman'] + UNITS['Champion']
    pikemen = UNITS['Spearman'] + UNITS['Pikeman'] + UNITS['Halberdier']
    eagles = UNITS['Eagle Scout'] + UNITS['Elite Eagle Warrior'] + UNITS['Eagle Warrior']
    condottieros = UNITS['Condottiero'] # dunno
    
    # archery ranges
    archers = UNITS['Archer'] + UNITS['Arbalest'] + UNITS['Crossbowman']
    skirmishers = UNITS['Skirmisher'] + UNITS['Elite Skirmisher'] + UNITS['Imperial Skirmisher']
    cavalry_archers = UNITS['Cavalry Archer'] + UNITS['Heavy Cavalry Archer']
    slingers = UNITS['Slinger']
    genitours = UNITS['Genitour'] + UNITS['Elite Genitour']
    hand_cannoneers = UNITS['Hand Cannoneer']
    
    # stables 
    light_cavalry = UNITS['Scout Cavalry'] + UNITS['Light Cavalry'] + UNITS['Hussar']
    heavy_cavalry = UNITS['Knight'] + UNITS['Cavalier'] + UNITS['Paladin']
    camels = UNITS['Camel'] + UNITS['Heavy Camel'] + UNITS['Imperial Camel']
    battle_elephants = UNITS['Battle Elephant'] + UNITS['Elite Battle Elephant']
    
    # dock military units
    fire_ships = UNITS['Fire Galley']+ UNITS['Fire Ship']+ UNITS['Fast Fire Ship']
    demolition_ships = UNITS['Demolition Raft'] + UNITS['Demolition Ship'] + UNITS['Heavy Demolition Ship']
    war_ships = UNITS['Galley'] + UNITS['War Galley'] + UNITS['Galleon']
    cannon_galleons = UNITS['Cannon Galleon'] + UNITS['Elite Cannon Galleon'] 
    longboats = UNITS['Longboat'] + UNITS['Elite Longboat']
    caravels = UNITS['Caravel'] + UNITS['Elite Caravel']
    turtle_ships = UNITS['Turtle Ship'] + UNITS['Elite Turtle Ship'] 
    transport_ships = UNITS['Transport Ship']
    # Siege workshop units
    rams = UNITS['Battering Ram'] + UNITS['Capped Ram'] + UNITS['Siege Ram']
    scorpions = UNITS['Scorpion'] + UNITS['Heavy Scorpion']
    onagers = UNITS['Mangonel'] + UNITS['Onager'] + UNITS['Siege Onager']
    siege_towers = UNITS['Siege Tower']
    bombard_cannons = UNITS['Bombard Cannon']

    # Monks
    monks = UNITS['Monk'] + UNITS['Missionary'] + UNITS['Monk with Relic'] + UNITS['Monk with Turkish Relic']

    # Castles 
    trebuchets = UNITS['Trebuchet'] + UNITS['Trebuchet (Packed)']
    petards = UNITS['Petard']

    # Uniqe Units
    longbowmans = UNITS['Longbowman'] + UNITS['Elite Longbowman']
    throwing_axemans = UNITS['Throwing Axeman'] + UNITS['Elite Throwing Axeman']
    woad_raiders = UNITS['Woad Raider'] + UNITS['Elite Woad Raider']
    cataphracts = UNITS['Cataphract'] + UNITS['Elite Cataphract']
    teutonic_knights = UNITS['Teutonic Knight'] + UNITS['Elite Teutonic Knight']
    huskarls = UNITS['Huskarl'] + UNITS['Elite Huskarl']
    mamelukes = UNITS['Mameluke'] + UNITS['Elite Mameluke']
    janissarys = UNITS['Janissary'] + UNITS['Elite Janissary']
    war_elephants = UNITS['War Elephant'] + UNITS['Elite War Elephant']
    chu_ko_nus = UNITS['Chu Ko Nu'] + UNITS['Elite Chu Ko Nu']
    samurais = UNITS['Samurai'] + UNITS['Elite Samurai']
    mangudais = UNITS['Mangudai'] + UNITS['Elite Mangudai']
    berserks = UNITS['Berserk'] + UNITS['Elite Berserk']
    jaguar_warriors = UNITS['Jaguar Warrior'] + UNITS['Elite Jaguar Warrior']
    tarkans = UNITS['Tarkan'] + UNITS['Elite Tarkan']
    plumed_archers = UNITS['Plumed Archer'] + UNITS['Elite Plumed Archer']
    conquistadors = UNITS['Conquistador'] + UNITS['Elite Conquistador']
    war_wagons = UNITS['War Wagon'] + UNITS['Elite War Wagon']
    genoese_crossbowmans = UNITS['Genoese Crossbowman'] + UNITS['Elite Genoese Crossbowman']
    magyar_huszars = UNITS['Magyar Huszar'] + UNITS['Elite Magyar Huszar']
    elephant_archers = UNITS['Elephant Archer'] + UNITS['Elite Elephant Archer']
    boyars = UNITS['Boyar'] + UNITS['Elite Boyar']
    kamayuks = UNITS['Kamayuk'] + UNITS['Elite Kamayuk']
    gbetos = UNITS['Gbeto'] + UNITS['Elite Gbeto']
    tarkans = UNITS['Tarkan'] + UNITS['Elite Tarkan']
    organ_guns = UNITS['Organ Gun'] + UNITS['Elite Organ Gun']
    camel_archers = UNITS['Camel Archer'] + UNITS['Elite Camel Archer']
    shotel_warriors = UNITS['Shotel Warrior'] + UNITS['Elite Shotel Warrior']
    ballista_elephants = UNITS['Ballista Elephant'] + UNITS['Elite Ballista Elephant']
    karambit_warriors = UNITS['Karambit Warrior'] + UNITS['Elite Karambit Warrior']
    arambais = UNITS['Arambai'] + UNITS['Elite Arambai']
    rattan_archers = UNITS['Rattan Archer'] + UNITS['Elite Rattan Archer']
    battle_elephants = UNITS['Battle Elephant'] + UNITS['Elite Battle Elephant']
    caslte_unique_units = longbowmans + throwing_axemans + woad_raiders + cataphracts + teutonic_knights + huskarls + huskarls + mamelukes + janissarys + war_elephants + chu_ko_nus + samurais + mangudais + berserks + jaguar_warriors + tarkans + plumed_archers + conquistadors + war_wagons + genoese_crossbowmans + magyar_huszars + elephant_archers + boyars + kamayuks + tarkans + organ_guns + camel_archers + gbetos + shotel_warriors + ballista_elephants + karambit_warriors + arambais + rattan_archers + battle_elephants
    dock_unique_units = longboats + turtle_ships + caravels
    all_unique_units = caslte_unique_units + dock_unique_units
    
    ## Buildings 
    # --- military ---
    stables = UNITS['Stable']
    archery = UNITS['Archery Range']
    barracks = UNITS['Barracks']
    siege_workshop = UNITS['Siege Workshop']
    monastery = UNITS['Monastery']
    castle = UNITS['Castle'] + UNITS['Fortress']
    dock = UNITS['Dock']
    # -- eco buildings --
    lumber_camps = UNITS['Lumber Camp']
    mining_camps = UNITS['Mining Camp']
    mill = UNITS['Mill']
    market = UNITS['Market']
    blacksmiths = UNITS['Blacksmith']
    university = UNITS['University']
    farms = UNITS['Farm']
    town_centers = UNITS['Town Center']
    # def buildings
    arrow_tower = UNITS['Watch Tower'] + UNITS['Guard Tower'] + UNITS['Keep'] + UNITS['Fire Tower'] + UNITS['The Accursed Tower'] + UNITS['Sea Tower'] + UNITS['The Tower of Flies']
    bombard_tower = UNITS['Bombard Tower']
    towers = arrow_tower + bombard_tower
    palisade = UNITS['Palisade Wall'] + UNITS['Palisade Gate'] 
    stone_wall = UNITS['Stone Wall'] + UNITS['Fortified Wall']  + UNITS['Gate']
    walls = UNITS['Palisade Wall'] + UNITS['Stone Wall'] + UNITS['Fortified Wall'] + UNITS['Sea Wall'] + UNITS['Fortified Palisade Wall'] + UNITS['City Wall'] + UNITS['Fence'] + UNITS['Aqueduct']
    gates = UNITS['Gate'] + UNITS['Palisade Gate']

if __name__ == '__main__':
    import bartender