# Bartender
A window addon to game called Age of Empires II (HD). The addon displays additional information of the game, such as buildings, currently researched technologies, or training units.

Bartender can be divided into five parts.
1) It displays information about your villagers, ships and trade on the top of your screen. Also, you can find there K/D ratios of units and buildings.
2) Researched technologies are shown right below the top bar. Currently researching technologies are next to it.
3) Buildings waiting for the construction or buildings that are currently constructed are displayed below the chat window.
4) Military Buildings (including TC, docks and monastries) are shown on bottom left. Each icon represents a building. The icon changes to currently trained unit or researched technology. Moreover it shows the time in seconds when it will complete the training or the research. The bottom number is a queue.
5) If small army is selected. You can see your army composition on the bottom.

Did I tell you that it highlights selected building?

![](http://flea.name/data/scrot.png)


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
> That is not possible. Contact some administrators of Voobly.


# TODO
1) User Interface is just porotyped need to be reworked.
2) Fix lag problems caused by transparency of the window. (In my case, it decreases AoE's FPS to 25)
3) Colourfull icons (Yay!).
4) Record game version.
5) Add on the side of screen selected units (showing the way where are the units).
6) Show which and how much units are selected (6 villagers, 3 militia -> Icons with number).
7) Fix crashes.
8) Make display unclickable.
9) Hide display when AoE2HD is not the foreground window.
10) Make starting and quitting bartender easier (wait for AoE2HD to be started and ingame, quit bartender when AoE2HD was closed).


# Known Limitations
1) Needs update when the AoE2HD version changes.


# License
Bartender, Copyright (C) 2018 Flea, blk_panther

This program (located in this folder) is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.
