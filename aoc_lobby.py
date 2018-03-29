#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" aoc_game.py: parsing aoc data from lobby """ 
from statistics import mode
from copy import copy
from collections import defaultdict
from itertools import combinations 

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
    STR_LEFT = "Somebody Left"
    STR_EVEN_NUMBERS = "Requires even number of players"

    def __init__(self):
        """ Constructor - creates the players list """
        super(Lobby, self).__init__()        
        self.players = []
        for i in range(9):
            self.players += [LobbyPlayer()]

    def update(self):
        """ Fills the players list"""
        ptr = pm.pointer(pm.base_address + 0x6Da30C) 
        ptr = pm.pointer(ptr + 0xD54) 
        regex = b""
        dict_ratings = defaultdict(list) 
        for i in range(Lobby.SKIP_GAIA,9):
            p = ptr + 0x50 + 0x60*i
            number = pm.int32(p + 0x48) # Get player number
            if number == -1: # A resets it 
                self.players[i] = LobbyPlayer()
            else:
                # Update player's stuff
                player = self.players[i]
                player.number = number
                player.team = pm.int32(p + 0x0)
                player.color = pm.int32(p + 0x44)
                player.ai = False if player.name else True
                name = pm.byte_string(pm.pointer(p + 0xC)) if i > 0 else b"Gaia"
                if name != player.name and i > 0 and name:
                    regex += b'\[\d{1,4}\] ' + name + b'\x00|'
                player.name = name
        if regex: # not empty
            regex = regex[:-1] # remove last | 
            result = []
            for i in pm.re(regex):
                fullname = i.group(0)[1:-1] # removes character `[` and `\x00`
                name_index = fullname.index(b"]") # char `]` is considered as separtor
                rating_string = fullname[:name_index]
                name = fullname[name_index+2:]  # Remove `]` and space character
                result += [(int(rating_string), name)]
                dict_ratings[name] += [int(rating_string)]
            for p in self.players:
                if dict_ratings[p.name]:
                    p.rating = mode(dict_ratings[p.name])
                else:
                    p.rating = None

    def balance_diff(self):
        ratings = list(map(lambda x: x.rating, filter(lambda x: x.rating, self.players)))
        players = list(range(1, len(ratings)+1))
        if len(ratings) != len(list(filter(lambda x: x.name is not None, self.players))):
            print(STR_LEFT)
            raise
        # Check and clean the size of ratings or players
        if len(ratings)%2 != 0:
            print(STR_EVEN_NUMBERS)
            raise
        splitting = len(players)//2

        # Different value between ratings
        diff = float('inf')

        # Best found team split
        team1 = []
        team2 = []
        # Iterate through each combination
        # Checking out over 70 solutions for 8 players
        for i in combinations(zip(ratings, players), splitting):
            current_team1 = i
            current_team2 = list(filter(lambda x: not(x in current_team1), zip(ratings, players)))
            # Calculate current different value
            d = abs(sum(map(lambda x: x[0], current_team1)) - sum(map(lambda x: x[0], current_team2)))
            # Found better solution
            if d < diff:
                diff = d
                team1 = current_team1
                team2 = current_team2
        return team1, team2, diff, players

    def balance_minmax(self):
        ratings = list(map(lambda x: x.rating, filter(lambda x: x.rating, self.players)))
        players = list(range(1, len(ratings)+1))
        if len(ratings) != len(list(filter(lambda x: x.name is not None, self.players))):
            print(STR_LEFT)
            raise
        # Check and clean the size of ratings or players
        if len(ratings)%2 != 0:
            print(STR_EVEN_NUMBERS)
            raise
        stuff = list(zip(ratings, players))
        team1 = []
        team2 = []
        current = team1
        splitting = len(players)//2
        for i in range(0,len(ratings),2):
            elo = max(stuff)
            current.append(elo)
            stuff.remove(elo)
            elo = min(stuff)
            current.append(elo)
            stuff.remove(elo)
            if i % 4:
                current = team1
            else:
                current = team2
        t1 = list(map(lambda x: x[0], team1))
        t2 = list(map(lambda x: x[0], team2))
        return t1, t2, None, players

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
            try:
                name = player.name.decode("utf-8").ljust(32)
            except:
                name = f"Player #{player.number}".ljust(32)
            print(f"{name} {player.rating}")
        t1, t2, _, players = lobby.balance_minmax()
        print("minmax:", t1, t2)
        t1, t2, diff, numbers = lobby.balance_diff()

        team1 = [p[1] for p in t1]
        team2 = [p[1] for p in t2]
    
        def make_str(players, team1, team2):
            string = ""
            for player in players: 
                if player in team1:
                    string += "1"
                else:
                    string += "2"
            return string

        print(f"Team1: {team1}")
        print(f"Team2: {team2}")
        print("Write in chat:", make_str(numbers, team1, team2))
        print("Rating difference:", diff)

        


