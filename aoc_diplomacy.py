#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" aoc_diplomacy.py: parsing diplomacies""" 
from pymemory import pymemory as pm
from copy import copy

class Diplomacy(list):
    """ Inherits `list` datatype! 

    Attributes
        ptr Address to player
    Methods
        __init__     Constructor
        update(log)  Updates values; if a change appeared, puts it into the log.
    """
    string = ["Gaia", "Player of View", "Ally", "Neutral", "Enemy", "Not a player"]
    def __init__(self, owner):
        self.owner = owner 
        self.ptr = owner.ptr
        diplomacy = pm.struct(self.ptr + 0x7C, "iiiiiiiii")
        diplomacy = filter(lambda x: x != -1, diplomacy)
        super(Diplomacy, self).__init__(diplomacy)
    def update(self, log):
        diplomacy = pm.struct(self.ptr + 0x7C, "iiiiiiiii")
        diplomacy = list(filter(lambda x: x != -1, diplomacy))
        if diplomacy != self:
            log += [(copy(diplomacy), copy(self))]
            self.clear()
            self.extend(diplomacy)
    def __str__(self):
        l = [f"P{i}: {Diplomacy.string[value]}" for i, value in enumerate(self)]
        return str(l)
