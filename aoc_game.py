#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" aoc_game.py: parsing aoc game data which are common to all players """ 
from pymemory import pymemory as pm
from pymemory import NullAddress
from aoc_player import *
from aoc_time import GTime
# debug
#from pymemory import print_addr


class Game(object):
    """
    Attributes
        public
            Players
                gaia         Gaia Player
                players      List of Player
                pov          Player of View (PoV)
                player       PoV 
            Teams  
                teams        List of teamss
                t1           Allies to PoV
                t2           Enemies to PoV
            Game
                screen_position  Position in format [float, float]
                speed            Game speed
    Methods:
        public 
            __init__()   Constructor
            update       Get the next iteration of game
        private 
            __get_teams__()  Creates teams from diplomacy in the beggining of the game. Called in constructor
            __update_teams__() Creates teams DURING the game. Called in `update` method
            
    """
    def __get_teams__(self):
        teams = {} # magic
        for diplo, value in map(lambda p: (p.diplomacy, p), self.players):
            key = map(lambda x: str(x == 4), diplo)
            teams.setdefault("".join(key), []).append(value)
        return list(teams.values())
    def __init__(self):
        super(Game, self).__init__()
        ptr = pm.pointer(pm.base_address + 0x006E62D8)
        ptr_players = pm.pointer(ptr + 0x184)
        # Get gaia firstly and calculate total players
        self.gaia = Player(pm.pointer(ptr_players))
        total_players = len(self.gaia.diplomacy) - 1 # Gaia is considered as player too
        # Get the rest of players
        self.players = [Player(pm.pointer(ptr_players + i * 0x8), i) for i in range(1, total_players+1)]
        self.teams = self.__get_teams__()
        self.t1 = []
        self.t2 = []
        self.player = None
        self.pov = None
        
    def __update_teams__(self):
        self.t1 = []
        self.t2 = []
        for t in self.teams:
            if self.pov in t:
                self.t1 += t 
            else:
                self.t2 += t 

        
    def update(self):
        try:
            ptr = pm.pointer(pm.base_address + 0x006E62D8) # Checking if the game is running 
            pm.pointer(ptr + 0x184)
        except NullAddress:
            return False

        # And get the common stuff
        GTime.set(pm.int32(ptr + 0x68))
        self.screen_position = pm.struct(ptr + 0xD8, "ff")
        self.speed = pm.float(ptr + 0x16C)
        self.pov = self.players[pm.int8(ptr + 0x174) - 1] # Must be -1 
        if self.pov != self.player:
            self.__update_teams__()
        self.player = self.pov # Yay.
        market_price = pm.struct(ptr + 0x238, "fff") # Wood, food, stone coeficient see spirit of the law - markets
        for player in self.players:
            player.update(market_price)
        return True

        
       

if __name__ == '__main__':
    import time
    proc_name = "AoK HD.exe"
    pm.load_process(proc_name)
    with pm:
        game = Game()
        game.update()

