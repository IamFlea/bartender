#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" aoc_civ.py: analyzes civilization data"""
from pymemory import pymemory as pm


class Civilization(object):
    """
    Attributes
        name  Civlization name
        icon  Civlization icon for unique unit
        code  Civlization code 
    Methods
        __init__(ptr)  constructor, ptr is a pointer to the player
    """
    # Check icons once agian
    icons = [3, 41, 46, 50, 45, 44, 36, 35, 43, 37, 39, 38, 42, 47, 106, 110, 108, 105, 117, 133, 93, 97, 99, 114, 190,
             195, 197, 191, 231, 233, 230, 232, ]
    strings = ["Gaia", "British", "French", "Goths", "Teutons", "Japanese", "Chinese", "Byzantine", "Persians",
               "Saracens", "Turks", "Vikings", "Mongols", "Celts", "Spanish", "Aztecs", "Mayan", "Huns", "Koreans",
               "Italians", "Indians", "Incas", "Magyars", "Slavs", "Portuguese", "Ethopians", "Malians", "Berbers",
               "Khmer", "Malay", "Burmese", "Vietnamese"]

    def __init__(self, owner):
        # ptr - pointer to a player
        ptr_civ_name = pm.pointer(owner.ptr + 0x1AE0)
        self.owner = owner
        self.name = pm.string(ptr_civ_name + 4)
        self.code = Civilization.strings.index(self.name)

        self.icon = Civilization.icons[self.code]

    def __repr__(self):
        return self.name
    # EOF: aoc_civ.py
