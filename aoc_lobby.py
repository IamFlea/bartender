#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" aoc_game.py: parsing aoc data from lobby """
from collections import defaultdict
from itertools import combinations
from re import escape
from statistics import mode

from pymemory import pymemory as pm


class LobbyPlayer(object):
    def __init__(self):
        self.number = None
        self.team = None
        self.color = None
        self.deathmatch_rating = None
        self.rating = None
        self.ai = None
        self.name = None
        self.civ = None
        self.rating = None


class LobbyException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


def make_str(players, team1, team2):
    string = ""
    for player in players:
        if player in team1:
            string += "1"
        else:
            string += "2"
    return string


class Lobby(object):
    SKIP_GAIA = 1
    STR_LEFT = "Somebody Left"
    STR_EVEN_NUMBERS = "Requires even number of players"
    REVEAL_MAP_OPTIONS = {0: "Standard", 1: "Explored", 2: "All Visible"}
    VICTORY_OPTIONS = {9: "Standard", 1: "Conquest", 7: "Time Limit", 8: "Score", 0xb: "Last Man Standing"}
    STARTING_AGE_OPTIONS = {0: "Standard", 2: "Dark Age", 3: "Feudal Age", 4: "Castle Age", 5: "Imperial Age",
                            6: "Post-Imperial Age"}
    RESOURCES_OPTIONS = {0: "Standard", 1: "Low", 2: "Medium", 3: "High"}
    MAP_SIZE_OPTIONS = {0: "2 players", 1: "3 players", 2: "4 players", 3: "6 players", 4: "8 players", 5: "Giant",
                        6: "LudiKRIS"}

    def __init__(self):
        """ Constructor - creates the players list """
        super(Lobby, self).__init__()
        self.up = True
        self.players = []
        for i in range(9):
            self.players += [LobbyPlayer()]
        self.something_new = False

    def update(self):
        """ Fills the players list"""
        self.up = True
        ptr = pm.pointer(pm.base_address + 0x006EEFB4)
        ptr = pm.pointer(ptr + 0x0)
        ptr = pm.pointer(ptr + 0x60)
        ptr = pm.pointer(ptr + 0xCE4)

        if not ptr:  # ptr is null if not in the lobby
            return False

        self.victory = Lobby.VICTORY_OPTIONS[pm.int32(ptr + 0x50)]
        self.victory_time_or_score = pm.int32(ptr + 0x54)  # Time is in years!
        self.map_size = Lobby.MAP_SIZE_OPTIONS[pm.int32(ptr + 0x90)]
        self.reveal_map = Lobby.REVEAL_MAP_OPTIONS[pm.int32(ptr + 0x9c)]
        self.resources = Lobby.RESOURCES_OPTIONS[pm.int32(ptr + 0xa0)]
        self.starting_age = Lobby.STARTING_AGE_OPTIONS[pm.int32(ptr + 0xa4)]
        self.ending_age = Lobby.STARTING_AGE_OPTIONS[pm.int32(ptr + 0xa8)]
        self.game_speed = pm.float(ptr + 0x3b4 + 8 * 8)
        self.treaty_length = pm.int32(ptr + 0x3b8 + 8 * 8)
        self.population_limit = pm.int32(ptr + 0x3bC + 8 * 8)

        for i in range(Lobby.SKIP_GAIA, 9):
            p = ptr + 0x48 + 0x68 * i
            number = pm.int32(p + 0x50)  # Get player number

            if number == -1:  # A resets it
                self.players[i] = LobbyPlayer()
            else:
                # Update player's stuff
                player = self.players[i]
                player.number = number
                player.team = pm.int32(p + 0x0)
                player.deathmatch_rating = pm.int32(p + 0x44)
                player.rating = pm.int32(p + 0x48)
                player.color = pm.int32(p + 0x4C)
                player.name = pm.byte_string(pm.pointer(p + 0xC)) if i > 0 else b"Gaia"
                player.ai = False if player.name and player.name is not "Gaia" else True
                player.civ = None

        self.teams_together = not bool(pm.int8(ptr + 0x3c2 + 8 * 8))
        self.all_techs = bool(pm.int8(ptr + 0x3c3 + 8 * 8))
        self.lock_teams = bool(pm.int8(ptr + 0x3c5 + 8 * 8))
        self.lock_speed = bool(pm.int8(ptr + 0x3c6 + 8 * 8))
        self.record_game = bool(pm.int8(ptr + 0x3cc + 8 * 8))
        self.allow_cheats = bool(pm.int8(ptr + 0x3cf + 8 * 8))
        return True

    def update_ratings(self):
        return
        # This is no longer needed
        dict_ratings = defaultdict(list)
        regex = b""
        length = 0
        for p in self.players:
            if p.name is not None:
                regex += b'\[\d{1,4}\] ' + escape(p.name) + b'\x00|'
                length += 1
        if length % 2 != 0:
            raise LobbyException(Lobby.STR_EVEN_NUMBERS)
        # Check and clean the size of ratings or players
        if regex:  # not empty
            regex = regex[:-1]  # remove last |
            result = []
            for i in pm.re(regex):
                fullname = i.group(0)[1:-1]  # removes character `[` and `\x00`
                try:
                    name_index = fullname.index(b"]")  # char `]` is considered as separtor
                except ValueError:
                    print(fullname)
                rating_string = fullname[:name_index]
                name = fullname[name_index + 2:]  # Remove `]` and space character
                result += [(int(rating_string), name)]
                dict_ratings[name] += [int(rating_string)]
            for p in self.players:
                if dict_ratings[p.name]:
                    p.rating = mode(dict_ratings[p.name])
                else:
                    p.rating = None

    def balance_diff(self):
        """Calculate balanced teams based on (rating) numbers.

        Supports 2-8 players (1v1 to 4v4).
        Expects a list with an even number of up to 8 values,
        raises a TypeError when not supplied with a list of integers and
        raises a ValueError when supplied numbers are violating this rule.
        Returns a list (values are integers):
        [[Teams], Difference, [Team1 numbers], [Team2 numbers]]
        Uses bruteforce for optimal balancing (up to 35 teams for 8 players).
        """
        if self.up:
            self.update_ratings()
            self.up = False

        ratings = list(map(lambda x: x.rating, filter(lambda x: x.rating, self.players)))
        players = list(range(1, len(ratings) + 1))
        splitting = len(players) // 2

        if len(ratings) > 8:
            raise ValueError("No more than 8 players are supported.")
        if len(ratings) % 2 != 0:
            raise ValueError("Only an even number of players is supported.")

        # Different value between ratings
        diff = float('inf')

        # Best found team split
        team1 = []
        team2 = []
        ratings_sum = lambda team: sum(map(lambda x: x[0], team))
        # Only half of every possible combination is needed because the other half
        # would redundantly calculate B vs A when A vs B was already calculated.
        max_number_of_combinations = {2: 1, 4: 3, 6: 10, 8: 35}[len(ratings)]
        # Iterate through each combination
        for combination in list(combinations(zip(ratings, players), splitting))[:max_number_of_combinations]:
            current_team1 = combination
            current_team2 = list(filter(lambda x: not (x in current_team1), zip(ratings, players)))
            # Calculate current different value
            current_diff = abs(ratings_sum(current_team1) - ratings_sum(current_team2))
            # Found better solution
            if current_diff < diff:
                diff = current_diff
                team1 = current_team1
                team2 = current_team2
        teams = [team1, team2]
        team1 = [p[1] for p in team1]
        team2 = [p[1] for p in team2]
        return diff, make_str(players, team1, team2), teams

    def balance_minmax(self):
        if self.up:
            self.update_ratings()
            self.up = False
        ratings = list(map(lambda x: x.rating, filter(lambda x: x.rating, self.players)))
        players = list(range(1, len(ratings) + 1))
        stuff = list(zip(ratings, players))
        team1 = []
        team2 = []
        current = team1
        splitting = len(players) // 2
        if len(ratings) >= 4:
            for i in range(2):
                elo = max(stuff)
                current.append(elo)
                stuff.remove(elo)
                elo = min(stuff)
                current.append(elo)
                stuff.remove(elo)
                current = team2
        if len(ratings) == 6:
            elo = max(stuff)
            team2.append(elo)
            stuff.remove(elo)
            elo = min(stuff)
            team1.append(elo)
            stuff.remove(elo)
        elif len(ratings) == 8:
            for i in range(2):
                elo = max(stuff)
                current.append(elo)
                stuff.remove(elo)
                elo = min(stuff)
                current.append(elo)
                stuff.remove(elo)
                current = team1

        # t1, t2, diff, numbers = lobby.balance_minmax()
        teams = [team1, team2]
        team1 = [p[1] for p in team1]
        team2 = [p[1] for p in team2]
        return None, make_str(players, team1, team2), teams


if __name__ == '__main__':

    proc_name = "AoK HD.exe"
    pm.load_process(proc_name)
    lobby = Lobby()
    lobby.update()
    print(f"victory: {lobby.victory}")
    print(f"victory_time_or_score: {lobby.victory_time_or_score}")
    print(f"map_size: {lobby.map_size}")
    print(f"reveal_map: {lobby.reveal_map}")
    print(f"resources: {lobby.resources}")
    print(f"starting_age: {lobby.starting_age}")
    print(f"ending_age: {lobby.ending_age}")
    print(f"game_speed: {lobby.game_speed}")
    print(f"treaty_length: {lobby.treaty_length}")
    print(f"population_limit: {lobby.population_limit}")
    print(f"teams_together: {lobby.teams_together}")
    print(f"all_techs: {lobby.all_techs}")
    print(f"lock_teams: {lobby.lock_teams}")
    print(f"lock_speed: {lobby.lock_speed}")
    print(f"record_game: {lobby.record_game}")
    print(f"allow_cheats: {lobby.allow_cheats}")
    print()
    print("-----------------")

    for idx, player in enumerate(lobby.players):
        if player.number is None:
            continue
        print(f"Processing player {idx}")
        try:
            name = player.name.decode("utf-8").ljust(32)
        except:
            name = f"Player #{player.number}".ljust(32)
        print(f"Number: {player.number}")
        print(f"Name: {name}")
        print(f"Rating: {player.deathmatch_rating} or {player.rating} ")
        print(f"Team: {player.team}")
        print(f"Color: {player.color}")
        print(f"Civ: {player.civ}")
        print(f"AI: {player.ai}")
        print()

    diff, string, teams = lobby.balance_minmax()
    print(f"{diff}:: {string}:: {teams}")

    diff, string, teams = lobby.balance_diff()
    print(f"{diff}:: {string}:: {teams}")
