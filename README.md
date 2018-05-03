# Bartender
A window addon to game called Age of Empires II (HD). The addon displays additional information of the game, such as buildings, currently researched technologies, or training units.

**Check out dev branch for the new unstable versions!**

Bartender can be divided into five parts.
1) It displays information about your villagers, ships and trade on the top of your screen. Also, you can find there K/D ratios of units and buildings.
2) Researched technologies are shown right below the top bar. Currently researching technologies are next to it.
3) Buildings waiting for the construction or buildings that are currently constructed are displayed below the chat window.
4) Military Buildings (including TC, docks and monastries) are shown on bottom left. Each icon represents a building. The icon changes to currently trained unit or researched technology. Moreover, it shows the time in seconds when it will complete the training or the research. The bottom number is a queue. Furthermore, the selected building is highlighted.
5) You can see your army composition on the bottom and how much units are selected.
6) If the selected object is out of the screen, bartender shows its icon on the side of screen displaying the object location.

![Screenshot](https://i.imgur.com/JWsTbWB.jpg)


# Dependencies
- [Python 3.6](https://www.python.org/downloads/ "Download Python | Python.org")
- [PyQt5](https://www.riverbankcomputing.com/software/pyqt/download5/) (pip3 install PyQt5)


# FAQ
*Can I use it in singleplayer/records/multiplayer?*
> Yes, yes, maybe.

*How does it work?*
> Bartender reads memory of the game. (There is no API! Boo at you Forgotten Empires!)

*Why did you create this addon?*
> I just wanted to simplify my gameplay.

*Voobly version?*
> That is not possible. Contact some administrators of Voobly and tell them about Bartender. Maybe they will agree to use it in multiplayer or record games.


# TODO

Watch for crashes & consistency of displayed data

**UI**
1) Rework User Interface.
2) This version requires 1920x1080 resolution; make it avaliable for larger/smaller resolutions.
3) Make an UI for managing bartender - quitting, or settings.
4) Fix lag problems caused by transparency of the window. (In my case, it decreases AoE's FPS to 25) 
5) Make overlay unclickable.
6) Hide overlay when AoE2HD is not the foreground window.

**Mechanics**
1) Detect if the game is a record game or SP/MP game.
2) Record game version - add training/researches info about other players.
3) Improve performance of `Player`'s method `__analyze_objects__()` in file `aoc_player.py`
4) Improve performance of obtaining `rating` in file `aoc_lobby.py`. Use a different approach to getting the rating number (screenshot + number classifier).
5) Fix a bug when `inf` is printed while a villager is constructing a building 
6) In `pymemory.py`, check pointers if they points to allocated addresses. (should fix big crashes)

**This file**
1) Update screenshot.

# Known Limitations
1) Needs update when the AoE2HD version changes.
2) Requires 1920x1080-ish resolution

# License
Bartender, Copyright (C) 2018 Flea, blk_panther

This program (located in this folder) is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.
