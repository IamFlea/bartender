#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" aoc_resources.py: parsing float strucutre of players """
from pymemory import pymemory as pm


class Resources(object):
    """ Resources 
    
    Attributes
        owner       Player struct
        ptr         A pointer to a resource structure
        keys        Key names, see the big oneliner after this comment
        values      Values in float
    Methods
        __init__    Constructor
        update      UPdate
    """

    keys = ['Food', 'Wood', 'Stone', 'Gold', 'Population Free Room', 'ConversionRange', 'CurrentAge', 'RelicsCaptured',
            'Unused (Trade Bonus)', 'Trade Goods', 'Unused (Trade Production)', 'Population', 'Corpse Decay Time',
            'Remarkable Discovery', 'MonumentsCaptured', 'MeatStorage', 'BerryStorage', 'FishStorage', 'Unused',
            'Total Units Trained', 'Units Killed', 'Technology Count', '% Map Explored', 'Castle Age Tech ID',
            'Imperial Age Tech ID', 'Feudal Age Tech ID', 'Attack Warning Sound ID', 'Enable Monk Conversion',
            'Enable Building Conversion', 'Unused', 'Unused (Building Limit)', 'Unused (Food Limit)', 'Population Cap',
            'Food Maintenance', 'Faith', 'Faith Recharging Rate', 'Farm Food Amount', 'Civilian Population', 'Unused',
            'All Techs Achieved', 'Military Population', 'Units Converted', 'Standing Wonders', 'Razings', 'Kill Ratio',
            'Survival to Finish', 'Tribute Tax', 'Gold Mining Productivity Bonus',
            'Town Center Unavaliable (Dark Age or Feudal)', 'Gold Gathered', 'Reveal Ally (Cartography)', 'Unused',
            'Monastries', 'Tribute Sent', 'All Monuments Captured', 'All Relics Captured', 'Ore Storage',
            'Kidnap Storage', 'Dark Age Tech ID', 'Unused (Trade Good Quality)', 'Unused (Trade Market Level)',
            'Unused (Formations)', 'Building Housing Rate ((maybe garisson))', 'Tax Gather Rate', 'Gather Accumulator',
            'Salvage Gather Rate', 'Unused (Allow Formations)', 'Can Convert', 'Hit Points Killed', 'P1 killed units',
            'P2 killed units', 'P3 killed units', 'P4 killed units', 'P5 killed units', 'P6 killed units',
            'P7 killed units', 'P8 killed units', 'Conversion Resistance', 'Trade Vig Rate',
            'Stone Mining Productivity', 'Queued Units', 'Currentelly Training', 'Start With Unit 444 (PTWC)',
            'Boarding Recharge Rate', 'Starting Villagers', 'Research Cost Modifier', 'Research Time Modifier',
            'Enable Boat Conversion', 'Fish Trap Food Amount', 'Heal Rate Modifier', 'Healing Range', 'Starting Food',
            'Starting Wood', 'Starting Stone', 'Starting Gold', 'Enable PTWC / Kidnap / Loot', 'Berserker Healing Rate',
            'Dominant Sheep Control (Celtic bonus)', 'Building Cost Sum', 'Tech Cost Sum', 'Relic Income Sum',
            'Trade Income Sum', 'To P1', 'To P2', 'To P2', 'To P3', 'To P4', 'To P5', 'To P6', 'To P7', 'To P8',
            'P2 Kill value', 'P3 Kill value', 'P4 Kill value', 'P5 Kill value', 'P6 Kill value', 'P7 Kill value',
            'P8 Kill value', 'P1 Razings', 'P2 Razings', 'P3 Razings', 'P4 Razings', 'P5 Razings', 'P6 Razings',
            'P7 Razings', 'P8 Razings', 'P1 Razing Value', 'P2 Razing Value', 'P3 Razing Value', 'P4 Razing Value',
            'P5 Razing Value', 'P6 Razing Value', 'P7 Razing Value', 'P8 Razing Value', 'Standing Castles',
            'Hitpoints Razed ((unused))', 'Unit Lost by P1', 'Unit Lost by P2', 'Unit Lost by P3', 'Unit Lost by P4',
            'Unit Lost by P5', 'Unit Lost by P6', 'Unit Lost by P7', 'Unit Lost by P8', 'Building Lost by P1',
            'Building Lost by P2', 'Building Lost by P3', 'Building Lost by P4', 'Building Lost by P5',
            'Building Lost by P6', 'Building Lost by P7', 'Building Lost by P8', 'Units Lost Value',
            'Building Lost Value', 'Units Lost', 'Buildings Lost', 'Tribute from P1', 'Tribute from P2',
            'Tribute from P3', 'Tribute from P4', 'Tribute from P5', 'Tribute from P6', 'Tribute from P7',
            'Tribute from P8', 'Value of Army', 'Value of Buildings', 'Food Total Gathered', 'Wood Total Gathered',
            'Stone Total Gathered', 'Gold Total Gathered', 'Kills Value', 'Tribute Received', 'Razings Value',
            'Total Castles', 'Total Wonders', 'Tribute Sent Score Value', 'Convert Min Adjustment',
            'Convert Max Adjustment', 'Convert Resist Min Adjustment', 'Convert Resist Max Adjustment',
            'Convert Building Min Adjustment', 'Convert Building Max Adjustment', 'Convert Building Chance',
            'Reveal Enemy (Spies)', 'Value Wonders/Castles', 'Food Score', 'Wood Score', 'Stone Score', 'Gold Score',
            'Wood Chopping Productivity', 'Food Gathering Productivity', 'Relic Gold Production Rate',
            'Converted Unit Dies', 'Theocracy', 'Crenellations (Teutons Unique Tech)', 'Construction rate',
            'Hun Wonder Bonus', 'Spies Discount', 'Unused [AK]', 'Unused [AK]', 'Unused [AK]', 'Unused [AK]',
            'Unused [AK]', 'Unused [AK]', 'Unused [AK]', 'Feitoria Food Productivity', 'Feitoria Wood Productivity',
            'Feitoria Stone Productivity', 'Feitoria Gold Productivity', 'Reveal Enemy TC', 'Reveal Relics']
    fmt = "f" * len(keys)


    def __init__(self, owner):
        super(Resources, self).__init__()
        self.owner = owner
        self.ptr = pm.pointer(owner.ptr + 0x3c)  # Pointer should be unchanged
        self.keys = Resources.keys
        self.values = pm.struct(self.ptr, Resources.fmt)

    def update(self):
        self.values = pm.struct(self.ptr, Resources.fmt)


if __name__ == '__main__':
    import bartender
    pass
