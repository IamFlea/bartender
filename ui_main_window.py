from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from ui_icon import IconCooldownCount
from ui_icon_civ import IconCiv
from ui_icon_research import IconResearch
from collections import OrderedDict
from ui_header_sp import HeaderSP
from ui_research import ResearchBar
from ui_icon_army import IconArmy
from ui_icon_waypoint import IconWaypoint
import time

class BartenderWindow(QtWidgets.QMainWindow):
    #UPDATE_WINDOW_MS = 16 # 60 FPS 
    UPDATE_WINDOW_MS = 33 # 30 FPS

    def __init__(self, game, width, height):
        super(BartenderWindow, self).__init__()
        self.game = game
        self.setWindowTitle("Bartender")
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.width = width
        self.height = height
        #self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)
        self.setGeometry(0,0,width,height)
        IconCooldownCount.game = game
        #####
        # Constructions
        self.w_construction = QtWidgets.QWidget(self)
        self.w_construction.setGeometry(5,250,42*8, 42*4)
        self.w_construction.icons = OrderedDict()
        # docks
        self.w_docks = QtWidgets.QWidget(self)
        self.w_docks.setGeometry(5,height-217 - 42*0,width-10, 42)
        self.w_docks.icons = OrderedDict()
        # barracks
        self.w_barracks = QtWidgets.QWidget(self)
        self.w_barracks.setGeometry(5,height-217 - 42*1,42*10, 42)
        self.w_barracks.icons = OrderedDict()
        # archeries
        self.w_archery = QtWidgets.QWidget(self)
        self.w_archery.setGeometry(5,height-217 - 42*2,42*10, 42)
        self.w_archery.icons = OrderedDict()
        # stables
        self.w_stables = QtWidgets.QWidget(self)
        self.w_stables.setGeometry(5,height-217 - 42*3,42*10, 42)
        self.w_stables.icons = OrderedDict()
        # siege
        self.w_siege = QtWidgets.QWidget(self)
        self.w_siege.setGeometry(5,height-217 - 42*4,42*10, 42)
        self.w_siege.icons = OrderedDict()
        # castles
        self.w_castles = QtWidgets.QWidget(self)
        self.w_castles.setGeometry(5,height-217 - 42*5,42*10, 42)
        self.w_castles.icons = OrderedDict()
        # monastries
        self.w_monastries = QtWidgets.QWidget(self)
        self.w_monastries.setGeometry(5,height-217 - 42*6,42*10, 42)
        self.w_monastries.icons = OrderedDict()
        # more more stuff
        self.w_markets = QtWidgets.QWidget(self)
        self.w_markets.setGeometry(5,height-217 - 42*7,42*10, 42)
        self.w_markets.icons = OrderedDict()
        # more more stuff
        self.w_tc = QtWidgets.QWidget(self)
        self.w_tc.setGeometry(5,height-217 - 42*7 - 62,42*10, 62)
        self.w_tc.icons = OrderedDict()

        # more more stuff
        self.w_research_done = QtWidgets.QWidget(self)
        #self.w_research_done.width = width//2 - 80
        self.w_research_done.width = width - 160 - 5
        self.w_research_done.setGeometry(5,36,self.w_research_done.width, 62)
        self.w_research_done.icons = OrderedDict()
        
        self.w_research = QtWidgets.QWidget(self)
        self.w_research.setGeometry(width - 150 - 5 , 36, 150, 42*10)
        self.w_research.icons = OrderedDict()

        #### HEADER ####
        self.w_header = HeaderSP(self, width)
        #### Footer ####
        self.w_army = QtWidgets.QWidget(self)
        self.w_army.setGeometry(width//2 + 110, height - 140, 42*11, 42*3)
        #self.w_army.setStyleSheet("background: black")
        self.w_army.icons = OrderedDict()
        self.w_leadpoint = QtWidgets.QWidget(self)
        self.w_leadpoint.setGeometry(0, 32, self.width, self.height-32-175)
        self.w_leadpoint.icons = OrderedDict()
        self.show()
        # Updating stuff
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.load)
        self.timer.start(BartenderWindow.UPDATE_WINDOW_MS)


    def load(self):
        r = self.game.update()
        if not r:
            r = self.close()
        player = self.game.player
        self.w_header.load(player)


        self.load_constructions(self.w_construction, player.constructions, showidle=False)
        self.load_buildings(self.w_docks, player.docks, showidle=False)
        self.load_buildings(self.w_barracks, player.barracks, showidle=False)
        self.load_buildings(self.w_archery, player.archery, showidle=False)
        self.load_buildings(self.w_stables, player.stables, showidle=False)
        self.load_buildings(self.w_siege, player.siege, showidle=False)
        self.load_buildings(self.w_castles, player.castle, showidle=False)
        self.load_buildings(self.w_monastries, player.monastery, showidle=False)
        self.load_buildings(self.w_markets, player.market, showidle=False)
        self.load_buildings(self.w_tc, player.town_centers, showidle=True)
        self.load_researches(self.w_research, player.research.progression, player)
        self.load_researches_done(self.w_research_done, player.research.done, player)
        self.load_army(self.w_army, player)
        self.load_selected(player.selected, self.w_leadpoint)
        #    self.w_army.show()
    def load_selected(self, selected, widget):
        # if we want to clear icons . 
        for icon in widget.icons:
            widget.icons[icon].delete = True

        # Need to transform the screen into game tiles
        width = (self.width)/ 90 # Transform the width to the ratio. We got squares now
        height = (self.height - 32 - 175)/45 # UI height contains a bar (32px) and bottom UI (175px)
        
        #print(width, height, width/height)
        c_w = width/2
        c_h = height/2
        # Some weird math. I have no theoretical idea how it works. But hey, it works!
        gx, gy = self.game.screen_position
        c_a = gx+c_w + gy+c_w
        c_b = -gx-c_h + gy-c_h +2
        c_c = gx-c_w + gy-c_w
        c_d = -gx+c_h + gy+c_h +1

        for unit in selected:
            x, y = unit.position
            xy = x+y
            xy_diff = y-x
            if c_a > xy and c_b < xy_diff and c_c < xy and c_d > xy_diff:
                #print("ON SCREEN")
                pass
            else:
                if unit not in widget.icons:
                    widget.icons[unit] = IconWaypoint(widget, unit)

                #print("NOT ON SCREEN")
                tx, ty = x-gx, y-gy
                k = abs(tx/ty)/2 if abs(tx) < abs(ty) else 1 - abs(ty/tx)/2 # might divide by zero
                if tx < 0 and ty < 0:
                    #print("LEFT", k)
                    widget.icons[unit].update_left(k)
                elif tx < 0 and ty > 0:
                    k = 1 - k
                    widget.icons[unit].update_bottom(k)
                elif tx > 0 and ty > 0:
                    k = 1 - k
                    #print("RIGHT", k)
                    widget.icons[unit].update_right(k)
                else: # tx > 0
                    #print("TOP", k)
                    widget.icons[unit].update_top(k)
                
                widget.icons[unit].delete = False
        # stupid way how to get rid of not selcted units
        remove_list = []
        for icon in widget.icons:
            if widget.icons[icon].delete:
                remove_list += [icon]
        if remove_list:
            # Remove the stuff..
            for i in remove_list:
                widget.icons[i].deleteLater()
                del widget.icons[i]

        #exit(1)    
            


    def load_army(self, widget, player):
        for icon in widget.icons:
            widget.icons[icon].delete = True
        for unit_id in player.army:
            units = player.army[unit_id]
            if unit_id not in widget.icons:
                x = 10 - len(widget.icons)//3
                y = len(widget.icons)%3
                widget.icons[unit_id] = IconArmy(widget, x, y, player, units)
                #print(x,y)
            else:
                widget.icons[unit_id].update(units)
            widget.icons[unit_id].delete = False
        # stupid way how to get rid of delted buildings...
        remove_list = []
        for icon in widget.icons:
            if widget.icons[icon].delete:
                remove_list += [icon]
        if remove_list:
            # Remove the stuff..
            for i in remove_list:
                widget.icons[i].deleteLater()
                del widget.icons[i]
            # And update the position
            for i, ptr in enumerate(widget.icons):
                x = 10 -i//3
                y = i%3
                widget.icons[ptr].update_position(x, y)

        
        
    def load_researches(self, widget, researches, player):
        for icon in widget.icons:
            widget.icons[icon].delete = True
        for tech in researches:
            id, icon, time, total_time, cooldown = tech
            if id not in widget.icons:
                x = 0
                y = len(widget.icons)
                widget.icons[id] = ResearchBar(widget, x, y, player, icon, time, total_time, cooldown)
            else:
                # just update the icon..
                widget.icons[id].update(time, total_time, cooldown)
            widget.icons[id].delete = False
        # stupid way how to get rid of delted buildings...
        remove_list = []
        for icon in widget.icons:
            if widget.icons[icon].delete:
                remove_list += [icon]
        if remove_list:
            # Remove the stuff..
            for i in remove_list:
                widget.icons[i].deleteLater()
                del widget.icons[i]
            # And update the position
            for i, ptr in enumerate(widget.icons):
                x = 0
                y = i
                widget.icons[ptr].update_position(x, y)


    def load_researches_done(self, widget, researches, player):
        # Check researches if any update
        update = False

        for tech, *_ in researches:
            if tech not in widget.icons:
                update = True
                break
        if update:
            # Clear all icons
            for k in widget.icons:
                widget.icons[k].deleteLater()
            # Remove it in dictionary
            widget.icons.clear()
            # Load new icons
            for i, research in enumerate(reversed(researches), start=1): # sorted by the newest to the latest
                # unpack the list
                tech, icon, time, *_ = research 
                # set new position
                x = self.w_research_done.width - 42*i
                y = 0
                # load icons
                widget.icons[tech] = IconResearch(widget, x, y, player, icon, time)

        

    def load_constructions(self, widget, buildings, showidle=False):
        # if we want to clear icons . 
        for icon in widget.icons:
            widget.icons[icon].delete = True
        # load new icons
        for building in buildings:
            if building not in widget.icons:
                # new building -> add icon into dictionary
                #x = len(widget.icons)
                #y = 0
                x = len(widget.icons) % 8
                y = len(widget.icons) // 8
                # Dont add wall icons, if the wall isn't build yet.
                if building.udata.class_ == 27 and building.construction == float("inf"):
                    continue
                widget.icons[building] = IconCooldownCount(widget, x, y, building, showidle)
            else:
                # just update the icon..
                widget.icons[building].update_building()
            # Handling for deleting icons 
            widget.icons[building].delete = False
            # If we build a big walls it spawns a lot of icons..  
            # this command hides a wall icon if any villager hadn't been building the wall last 5 seconds 
            if building.udata.class_ == 27 and building.construction == float("inf") and building.idle_time > 3000:
                widget.icons[building].delete = True
        # stupid way how to get rid of delted buildings...
        remove_list = []
        for icon in widget.icons:
            if widget.icons[icon].delete:
                remove_list += [icon]
        if remove_list:
            # Remove the stuff..
            for i in remove_list:
                widget.icons[i].deleteLater()
                del widget.icons[i]
            # And update the position
            for i, ptr in enumerate(widget.icons):
                #x = i
                #y = 0
                x = (i) % 8
                y = (i) // 8
                widget.icons[ptr].update_position(x, y)

    def load_buildings(self, widget, buildings, showidle=False):
        # if we want to clear icons . 
        for icon in widget.icons:
            widget.icons[icon].delete = True
        # load new icons
        for building in buildings:
            if building.construction:
                continue
            if building not in widget.icons:
                # new building -> add icon into dictionary
                x = len(widget.icons)
                y = 0
                #x = len(self.icons) % 10
                #y = len(self.icons) // 10
                widget.icons[building] = IconCooldownCount(widget, x, y, building, showidle)
            else:
                # just update the icon..
                widget.icons[building].update_building()
            # Handling for deleting icons 
            widget.icons[building].delete = False
        # stupid way how to get rid of delted buildings...
        remove_list = []
        for icon in widget.icons:
            if widget.icons[icon].delete:
                remove_list += [icon]
        if remove_list:
            # Remove the stuff..
            for i in remove_list:
                widget.icons[i].deleteLater()
                del widget.icons[i]
            # And update the position
            for i, ptr in enumerate(widget.icons):
                x = i
                y = 0
                #x = (i) % 10
                #y = (i) // 10
                widget.icons[ptr].update_position(x, y)

        
if __name__ == '__main__':
    import bartender