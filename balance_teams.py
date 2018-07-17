"""Provide the function balance_teams() to calculate balanced teams."""
from collections import Counter
from itertools import combinations
import sys


def balance_teams(ratings, premade_teams=None):
    """Calculate balanced teams based on (rating) numbers.

    Supports 2-8 players (1v1 to 4v4).
    Expects a list with an even number of up to 8 values,
    raises a TypeError when not supplied with a list of integers and
    raises a ValueError when supplied numbers are violating this rule.
    Raises a ValueError when premade_teams are more than ratings.
    Raises a ValueError when premade_teams are already full or too many.
    Raises a ValueError if premade_teams contains not only 0, 1 and 3.
    Returns a list (values are integers):
    [[Teams], Difference, [Team1 numbers], [Team2 numbers]]
    Optimal team balancing (bruteforce up to 35 teams for 8 players).
    If a second parameter (list with values 0, 1 or 2; no more values
    than ratings) is supplied, it will balance 0 within already
    supplied teams 1 and 2.
    """
    if premade_teams is None:
        premade_teams = []
    if not isinstance(ratings, list) or not isinstance(premade_teams, list):
        raise TypeError("Only lists are supported.")
    if (not all(isinstance(elem, int) for elem in ratings) or
            not all(isinstance(elem, int) for elem in premade_teams)):
        raise TypeError("Only a list of natural numbers (integers) is supported.")
    num_players = len(ratings)
    if len(ratings) > 8:
        raise ValueError("No more than 8 players are supported.")
    if len(ratings) == 0:
        raise ValueError("Please provide ratings.")
    if num_players % 2 != 0:
        raise ValueError("Only an even number of players is supported.")
    team_num = int(num_players/2)
    if len(ratings) < len(premade_teams):
        raise ValueError("Premade teams can not be more than ratings.")
    if not all(i >= 0 and i <= 2 for i in premade_teams):
        raise ValueError("Premade teams list can only contain 0, 1 or 2.")
    count1 = premade_teams.count(1)
    count2 = premade_teams.count(2)
    if count1 == team_num or count2 == team_num:
        raise ValueError("Premade team is already full.")
    if count1 > team_num or count2 > team_num:
        raise ValueError("Premade team is too big for player count.")

    premade1 = [ratings[i] for i, e in enumerate(premade_teams) if e == 1]
    premade2 = [ratings[i] for i, e in enumerate(premade_teams) if e == 2]
    premade = False if (premade1 == [] and premade2 == []) else True
    if premade:
        premade1_counter = Counter(premade1)
        premade2_counter = Counter(premade2)
    team1 = []
    team2 = []
    # Only half of every possible combination is needed because the other half
    # would redundantly calculate B vs A when A vs B was already calculated.
    max_num_of_combinations = {2: 0, 4: 2, 6: 9, 8: 34}
    combi = enumerate(combinations(ratings, team_num))
    difference = None
    for i, tm1 in combi:
        tm2 = list(ratings)
        for k in range(0, team_num):
            tm2.remove(tm1[k])
        # If premade_teams are not contained in this iteration of combi -> continue
        if premade:
            t1_counter = Counter(tm1)
            t2_counter = Counter(tm2)
            # premade1 and premade2 are not contained in tm1 and tm2 or in tm2 and tm1
            # need to check for all (multiple same) values -> use Counter not set
            if not ((not premade1_counter - t1_counter and not premade2_counter - t2_counter) or
                    (not premade1_counter - t2_counter and not premade2_counter - t1_counter)):
                continue
        diff = abs(sum(tm1)-sum(tm2))
        if (difference is None) or (diff < difference):
            difference = diff
            team1 = tm1
            team2 = tm2
        if i == max_num_of_combinations[num_players] or diff == 0:
            break
    team = []
    team1 = list(team1)
    tm1 = team1.copy()
    for elem in ratings:
        if elem in tm1:
            team.append(1)
            tm1.remove(elem)
        else:
            team.append(2)
    return [team, difference, team1, team2]


def _main():
    # Parse parameters and call balance_teams() if called directly
    args = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else ""
    try:
        team = balance_teams(args)
        print("Teams: " + ''.join(str(e) for e in team[0]))
        print(f"Difference: {team[1]}")
        print(f"Team1: {team[2]} Team2: {team[3]}")
    except (TypeError, ValueError) as err:
        print(err)


if __name__ == '__main__':
    _main()
