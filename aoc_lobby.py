#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" aoc_game.py: parsing aoc data from lobby """ 
from statistics import mode
from copy import copy
from pymemory import pymemory as pm
from pymemory import NullAddress

class LobbyPlayer(object):
    def __init__(self):
        self.number = None
        self.name = None
        self.color = None
        self.ai = None
        self.rating = None
class Lobby(object):
    SKIP_GAIA = 1
    """docstring for Lobby"""
    def __init__(self):
        super(Lobby, self).__init__()        
        ptr = pm.pointer(pm.base_address + 0x6Da30C) 
        ptr = pm.pointer(ptr + 0xD54) 
        self.players = []
        for i in range(9):
            player = LobbyPlayer()
            p = ptr + 0x50 + 0x60*i
            player.number = pm.int32(p + 0x48) # -1 if nobody
            player.name = None
            player.color = None
            player.ai =  None
            player.rating = None
            self.players += [player]

    def update(self):
        ptr = pm.pointer(pm.base_address + 0x6Da30C) 
        ptr = pm.pointer(ptr + 0xD54) 
        for i in range(Lobby.SKIP_GAIA,9):
            p = ptr + 0x50 + 0x60*i
            player = self.players[i]
            # get player number
            player.number = pm.int32(p + 0x48)
            if player.number == -1: #resets it 
                player.name = None
                player.color = None
                player.ai =  None
                player.rating = None
                name = None
            else:
                player.team = pm.int32(p + 0x0)
                player.color = pm.int32(p + 0x44)
                player.ai = False if player.name else True
                name = pm.string(pm.pointer(p + 0xC)) if i > 0 else "Gaia"
            if name != player.name and name is not None:
                #update rating
                player.name = name
                if i == 0:
                    player.rating = None
                else:
                    regular_expression = b'\[\d{1,4}\] ' + str.encode(player.name)
                    result = []
                    for i in pm.re(regular_expression):
                        fullname = i.group(0)[1:]
                        rating_string = fullname.decode("utf-8").split("]")[0]
                        result += [int(rating_string)]
                    player.rating = mode(result)

if __name__ == '__main__':
    import time
    proc_name = "AoK HD.exe"
    pm.load_process(proc_name)
    with pm:
        lobby = Lobby()
        lobby.update()
        for player in lobby.players:
            if player.name is None:
                continue
            print(f"{player.name}     {player.rating}")
        

