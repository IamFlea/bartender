<!-- ## Check out dev branch for the new unstable versions! -->

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
> Can I use it in singleplayer/records/multiplayer?

*Yes, yes, no but it works.*

> How does it work?

*Bartender reads memory of the game. (There is no API! Boo at you Forgotten Empires!)*

> Voobly version, or AoE 2 DE version?

*Voobly is possible to do, just replace some offsets :) AoE 2 de nah, the game crashes as soon as you attach the debugger :)*

> Why did you create this addon?

*Age of Empires: II uses UI from the previous century. I just wanted to simplify UI to me and to other players.*

# TODO

Watch for crashes & consistency of displayed data

**UI**
1) Fix lag problems caused by transparency of the window. (In my case, it decreases AoE's FPS to 25) 
2) Make it more user friendly. 

**Mechanics**
1) Detect if the game is a record game or SP/MP game - add training/researches info about other players. (It can be done by comparing three game pointers in `aoc_game.py`, two of them are null while watching recorded game.)
2) It gets laggy if the game loads a lot of data. We need to change the approach used for memory reading. 

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
