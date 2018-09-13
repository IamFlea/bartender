#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" aoc_game.py: parsing aoc game data which are common to all players """
from aoc_object_data import UnitData
from aoc_object_unit import Unit
from aoc_objects import Objects
from aoc_player import *
from aoc_time import GTime
from pymemory import NullAddress


# debug
# from pymemory import print_addr


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
                running          Boolean
    Methods:
        public 
            __init__()   Constructor
            update       Get the next iteration of game
        private 
            __get_teams__()  Creates teams from diplomacy in the beggining of the game. Called in constructor
            __update_teams__() Creates teams DURING the game. Called in `update` method
            
    """

    def __get_teams__(self):
        teams = {}  # magic
        for diplo, value in map(lambda p: (p.diplomacy, p), self.players):
            key = map(lambda x: str(x == 4), diplo)
            teams.setdefault("".join(key), []).append(value)
        return list(teams.values())

    def __new__(cls):
        # Check if the game is running. 
        if not pm.int32(pm.base_address + 0x9E0708):
            return None
        # Stupid way how to reset all CLASS variables (not object)
        UnitData.all_names = None
        Unit.graphics_data = {}
        Objects._all = {}
        Objects.selected = []
        Objects.selected_pointers = []
        GTime.time_delta = 0
        GTime.time = 0

        return super(Game, cls).__new__(cls)

    def __init__(self):
        super(Game, self).__init__()
        ptr = pm.pointer(
            pm.base_address + 0x006FDA30)  # three offsets are avaliable here: 006DC7F8, 006DDCA0, 006FDA30 each should point to the same address.. if not remove one   You need to check for each address in record game.
        ptr_players = pm.pointer(ptr + 0x184)
        # Get gaia firstly and calculate total players
        self.gaia = Player(pm.pointer(ptr_players))
        total_players = len(self.gaia.diplomacy) - 1  # Gaia is considered as player too
        # Get the rest of players
        self.players = [Player(pm.pointer(ptr_players + i * 0x8), i) for i in range(1, total_players + 1)]
        self.teams = self.__get_teams__()
        self.t1 = []
        self.t2 = []
        self.player = None
        self.pov = None
        self.running = False

    def __update_teams__(self):
        self.t1 = []
        self.t2 = []
        for t in self.teams:
            if self.pov in t:
                self.t1 += t
            else:
                self.t2 += t

    def update(self):
        # Check if the game is running: 0 not running, 1 running
        pm.update()
        if not pm.int32(pm.base_address + 0x9E0708):
            self.running = False
            return False

        # Second check.
        try:
            ptr = pm.pointer(
                pm.base_address + 0x006FDA30)  # three offsets are avaliable here: 006DC7F8, 006DDCA0, 006FDA30 each should point to the same address.. if not remove one   You need to check for each address in record game.
            pm.pointer(ptr + 0x184)
        except NullAddress:
            self.running = False
            return False

        # Third check. Time
        if pm.int32(ptr + 0x68) <= 0:
            return False

        self.running = True
        # And get the common stuff
        GTime.set(pm.int32(ptr + 0x68))
        self.screen_position = pm.struct(ptr + 0xD8, "ff")
        self.speed = pm.float(ptr + 0x16C)
        self.pov = self.players[pm.int8(ptr + 0x174) - 1]  # Must be -1
        if self.pov != self.player:
            if self.player is not None:
                self.player.pov = False
            self.player = self.pov  # Set the new pov
            self.player.pov = True
            self.__update_teams__()
        market_price = pm.struct(ptr + 0x238, "fff")  # Wood, food, stone coeficient see spirit of the law - markets
        Objects.selected.clear()
        Objects.selected_pointers.clear()
        # Update all players data
        for player in self.players:
            player.update(market_price)
        self.gaia.update(market_price)
        return True


if __name__ == '__main__':

    proc_name = "AoK HD.exe"
    pm.load_process(proc_name)
    game = Game()
    if game is not None:
        t = game.update()
