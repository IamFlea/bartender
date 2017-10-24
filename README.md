# Bartender
A window addon to game called Age of Empires II (HD). The addon parses usefull information of the game screen such as time, resources, or currentelly researched technologies; and shows time bars of researched technologies with remaining time and analyzes gathered/spend wood, food, gold, or stone per minute.

![Image](http://flea.name/data/image.png)

# Dependencies

Requires Python 3.6+

 - numpy
 - Pillow
 - opencv-python
 - pypiwin32
 - cx_Freeze (for build only)

```pip install numpy, Pillow, opencv-python, pypiwin32, cx_Freeze```

# Build
```python setup.py build```

# Usage
1) Run bartender `python bartender.py` or `bartender.exe`
2) Run AoE II
3) Make sure that you have only one screen on
4) Set AoE II to be maximized
5) Left click on the Bartender and set AoE dataset with [End] key
6) Run the game
7) If you don't have the time shown on top left corner, press [F11] in game
8) Press [Esc] to quit Bartender.

# FAQ

*How does it work?*

Bartender takes a screenshot and parses the resources, game time, and researched technologies from the screeshot. Then it prints the usefull information in a window.

*Why does it use `BitBlc()` function for taking screenshot?*

Indeed, `PrintWindow()` would be better. However, it returned black screen on my desktop.

# Known bugs
- If the research is started in a laggy game, it may not show the research bar.
- If the research is cancelled in a game, it is not cancelled in the bartender. 
