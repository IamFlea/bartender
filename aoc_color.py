#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" aoc_color.py: parsing colors """
from pymemory import pymemory as pm


class Color(object):
    """
    Attributes
        owner   Player struct 
        unique  Unique color which was selected before the game started
        in_game Depending on the toggle fog or foe. [Alt-g] If it is true then; Blue - PoV, Red - enemies, Yellow Allies; Else it should have the same color as unique
        color_address Pointer to the color, changes if [alt-g] was pressed
    Methods
        __init__  Constructor
        update    Updates values in the next iteration
    """

    # strings and color hexadecimal representation; must be sorted by color code
    table = ["Blue", "Red", "Green", "Yellow", "Cyan", "Purple", "Grey", "Orange"]
    rgb_units = [0x6ea6eb, 0xff6464, 0x00ff00, 0xffff00, 0x00ffff, 0xf16ce0, 0xd4d4d4, 0xffb415]
    rgb_minimap = [0x0000ff, 0xff0000, 0x00ff00, 0xffff00, 0x00ffff, 0xff00ff, 0x434343, 0xff8201]

    def __init__(self, owner):
        # Ptr - player pointer
        super(Color, self).__init__()
        self.ptr = owner.ptr  # ptr must be ptr to a player  Should be unchanged
        self.owner = owner
        self.unique = pm.int32(pm.pointer(owner.ptr + 0x100) + 0x8)
        self.color_address = pm.pointer(owner.ptr + 0xFC)
        self.in_game = pm.int32(self.color_address + 0x8)
        self.color = self.in_game

    def __repr__(self):
        return Color.table[self.in_game]

    def update(self):
        tmp = pm.pointer(self.ptr + 0xFC)
        if tmp != self.color_address:
            j = str(self)
            self.in_game = pm.int32(tmp + 0x8)
            self.color_address = tmp


if __name__ == '__main__':
    pass
