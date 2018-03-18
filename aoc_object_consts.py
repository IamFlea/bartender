#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" aoc_object_consts.py: This file contains lots of constants.""" 

class IdData():
    ## UNITS
    # -- villagers --
    vill_wood = [123, 218]
    vill_food = [120, 354, 56, 57, 214, 259, 122, 216, 590, 592, 1192]
    vill_stone = [220, 124]
    vill_gold = [581, 579]
    vill_builder = [212, 118]
    vill_repairer = [222, 156]
    vill_none = [293, 83]
    fish = [13]
    trade_carts = [128, 204]
    trade_cogs = [17]
    trade = trade_cogs + trade_carts
    # --- military ---
    #spearman = [93]
    #pikeman = [358]
    #halbadier = [359]
    spears = [93, 358, 359]
    #milita = [74]
    #man_at_arm = [75]
    #long_swordsman = [77]
    #two_handed_swordsman = [473]
    #champion = [567]
    swords = [74, 75, 77, 473, 567]
    # bored TODO

    ## Buildings 
    # --- military ---
    stables = [86, 101, 153]
    archery = [10, 14, 87]
    barracks = [12, 20, 132, 498]
    siege_workshop = [49, 150]
    monastery = [30, 31, 32, 104]
    #castle = [82]
    castle = [82, 33] # with fortress
    dock = [45, 47, 51, 133, 805, 806, 807, 808]
    # -- eco buildings --
    lumber_camps = [562, 563, 564, 565]
    mining_camps = [584, 585, 586, 587]
    mill = [68, 129, 130, 131]
    market = [84, 116, 137]
    blacksmiths = [18, 19, 103, 105]
    university = [209, 210]
    farms = [50, 1187]
    town_centers = [71, 109, 141, 142, 481, 482, 483, 484, 597, 611, 612, 613, 614, 615, 616, 617, 618, 619, 620, 621]
    # def buildings
    towers = [79, 190, 234, 566, 684, 685, 785]
    bbt = [236]
    palisade = [72, 119]
    stone_wall = [117, 155, 370]
    sea_wall = [788]
    #gates = [TODO]

class ClassData():
    all_str = ["Archer", "Artifact", "Trade Boat", "Building", "Civilian", "Ocean Fish", "Infantry", "Berry Bush", "Stone Mine", "Prey Animal", "Predator Animal", "Miscellaneous", "Cavalry", "Siege Weapon", "Terrain", "Tree", "Tree Stump", "Healer", "Monk", "Trade Cart", "Transport Boat", "Fishing Boat", "Warship", "Conquistador", "War Elephant", "Hero", "Elephant Archer", "Wall", "Phalanx", "Domestic Animal", "Flag", "Deep Sea Fish", "Gold Mine", "Shore Fish", "Cliff", "Petard", "Cavalry Archer", "Doppelganger", "Bird", "Gate", "Salvage Pile", "Resource Pile", "Relic", "Monk with Relic", "Hand Cannoneer", "Two Handed Swordsman", "Pikeman", "Scout", "Ore Mine", "Farm", "Spearman", "Packed Unit", "Tower", "Boarding Boat", "Unpacked Siege Unit", "Ballista", "Raider", "Cavalry Raider", "Livestock", "King", "Misc Building", "Controlled Animal", "Unknown"]
    military_str = ["Archer", "Infantry", "Prey Animal", "Predator Animal", "Cavalry", "Siege Weapon", "Healer", "Monk", "Warship", "Conquistador", "War Elephant", "Hero", "Elephant Archer", "Phalanx", "Petard", "Cavalry Archer", "Salvage Pile", "Resource Pile", "Monk with Relic", "Hand Cannoneer", "Two Handed Swordsman", "Pikeman", "Scout", "Spearman", "Packed Unit", "Boarding Boat", "Unpacked Siege Unit", "Ballista", "Raider", "Cavalry Raider"]
    military_str += ["Transport Boat"] # need to put it somewhere; comment if nessesery
    military = list(map(lambda x, y=all_str : y.index(x), military_str))
    civilians_str = ["Trade Boat", "Civilian", "Trade Cart", "Fishing Boat"]
    civilians = list(map(lambda x, y=all_str : y.index(x), civilians_str))
    all_buildings_str = ["Building", "Misc Building", "Gate", "Wall", "Tower", "Farm"]
    all_buildings = list(map(lambda x, y=all_str : y.index(x), all_buildings_str))
    building_str = ["Building"]
    building = list(map(lambda x, y=all_str : y.index(x), building_str))
    trebuchets_str = ["Unpacked Siege Unit", "Packed Unit"]
    trebuchets = list(map(lambda x, y=all_str : y.index(x), trebuchets_str))
    villagers_str = ["Civilian"]
    villagers = list(map(lambda x, y=all_str : y.index(x), villagers_str))

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
    building = 80 # Trebuchets are combatants
    tree_aoe = 90

