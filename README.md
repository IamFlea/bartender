# Bartender
A window addon to game called Age of Empires II (HD). The addon displays additional information of the game, such as buildings, currently researched technologies, or training units.

![Screenshot](https://i.imgur.com/JWsTbWB.jpg)

Bartender is customizable overlay and it can be divided into four parts. 

1) **Bartender's Research Panels** displays current researches and researched technologies.
2) **Bartender's Offscreen Unit Icons** shows you unit which are out of the screen. Its icon is shown on the side of screen displaying the object location.
3) **Bartender's Info Panels** gives you statistics about *your* villagers, ships and trade on the top of your screen. It can display the sum of carrying resources and amount of villagers (or other units) gathering the resource. It shows you idle units. Furthermore, it provides K/D ratios of units and buildings, amount of civilians and military, number of owning relics, and reseed farms.
4) **Bartender's Bars** provides you information about your civilization. Each bar can show you different things. One bar may provide you data about your buildings, other one about your army composition. Some buildings may change the icon to currently trained unit or researched technology. Moreover, it shows the time in seconds when it will complete the training or the research, or it can show you the length of training queue, or the number of garissoned units, current HP, attack etc. Furthermore, you can filter these icons. See the next image.




# Dependencies
- [Python 3.6](https://www.python.org/downloads/ "Download Python | Python.org")
- [PyQt5](https://www.riverbankcomputing.com/software/pyqt/download5/) (pip3 install PyQt5)
- [pywin32](https://pypi.org/project/pywin32/) (pip3 install pywin32)


# FAQ
*Can I use it in singleplayer/records/multiplayer?*
> Yes, yes, maybe.

*How does it work?*
> Bartender reads memory of the game. (There is no API! Boo at you Forgotten Empires!)

*Voobly version?*
> I don't play on Voobly. Also, I think this won't be possible to use it in MP there.

*Why did you create this addon?*
> Age of Empires: II uses engine from the previous century. I just wanted to simplify UI to me and to other players.

*This is cheating!*
> It is not. Bartender does not provide you information about your enemy. 

# TODO

Watch for crashes & consistency of displayed data

**UI**
1) Fix lag problems caused by transparency of the window. (In my case, it decreases AoE's FPS to 25) 

**Mechanics**
1) IMPORTANT: Find out when the game is in the score screen! 
2) Detect if the game is a record game or SP/MP game - add training/researches info about other players.
3) Improve performance of `Player`'s method `__analyze_objects__()` in file `aoc_player.py`. (Maybe not needed) 
4) Fix warnings during hiding overlay when AoE2HD is not the foreground window. (Maybe not needed)

**This file**
1) Update screenshots.
2) Add a UI explenation.

# Known Limitations
1) Needs update when the AoE2HD version changes.

# License
Bartender, Copyright (C) 2018 Flea, blk_panther

This program (located in this folder) is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.
