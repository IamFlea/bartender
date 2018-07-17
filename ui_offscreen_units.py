from collections import defaultdict

from PyQt5 import QtWidgets, QtCore, Qt, QtGui

from aoc_object_consts import GROUPS
from ui_icon_offscreen_unit import IconOffscreenUnit
class OverlayOffscreenUnits(QtWidgets.QWidget):
    def __init__(self, parent):
        super(OverlayOffscreenUnits, self).__init__(parent)
        self.parent = parent
        self.get_icons = lambda : {}
        # Sets the widget to be on the whole gamescreen. 
        self.icons = {}
        self.update_position()

    def update_position(self):
        self.setGeometry(0,32,self.parent.width(),self.parent.height()-32-175)

    def set_movable(self, *arg):
        # This widget is not movable!
        pass

    def update(self):
        for icon in self.icons:
            self.icons[icon].delete = True
        new_icons = self.get_icons()

        
        # Need to transform the screen into game tiles
        width = (self.width())/ 90 # Transform the width to the ratio. We got squares now
        height = (self.height())/45 # UI height contains a bar (32px) and bottom UI (175px)
        
        #print(width, height, width/height)
        c_w = width/2
        c_h = height/2
        # Some weird math. I have no theoretical idea how it works. But hey, it works!
        gx, gy = self.parent.game.screen_position
        c_a = gx+c_w + gy+c_w
        c_b = -gx-c_h + gy-c_h +2
        c_c = gx-c_w + gy-c_w
        c_d = -gx+c_h + gy+c_h +1
        for game_obj in new_icons:
            x, y = game_obj.position
            xy = x+y
            xy_diff = y-x
            if c_a > xy and c_b < xy_diff and c_c < xy and c_d > xy_diff:
                #print("ON SCREEN")
                pass
            else:
                group = defaultdict(str, GROUPS)[game_obj.group]
                if game_obj not in self.icons:
                    self.icons[game_obj] = IconOffscreenUnit(self, game_obj)
                    self.icons[game_obj].bottom_text = group
                    self.icons[game_obj].redraw()
                elif group != self.icons[game_obj].bottom_text:
                    self.icons[game_obj].bottom_text = group
                    self.icons[game_obj].redraw()
                


                #print("NOT ON SCREEN")
                tx, ty = x-gx, y-gy
                k = abs(tx/ty)/2 if abs(tx) < abs(ty) else 1 - abs(ty/tx)/2 # might divide by zero
                if tx < 0 and ty < 0:
                    #print("LEFT", k)
                    self.icons[game_obj].update_left(k)
                elif tx < 0 and ty > 0:
                    k = 1 - k
                    self.icons[game_obj].update_bottom(k)
                elif tx > 0 and ty > 0:
                    k = 1 - k
                    #print("RIGHT", k)
                    self.icons[game_obj].update_right(k)
                else: # tx > 0
                    #print("TOP", k)
                    self.icons[game_obj].update_top(k)
                
                self.icons[game_obj].delete = False
        # stupid way how to get rid of not selcted units
        remove_list = []
        for icon in self.icons:
            if self.icons[icon].delete:
                remove_list += [icon]
        if remove_list:
            # Remove the stuff..
            for i in remove_list:
                self.icons[i].deleteLater()
                del self.icons[i]
        #print(self.icons)
if __name__ == '__main__':
    import bartender