from collections import OrderedDict

from ui_resize import QResizableWidget
from ui_icon import Icon
from ui_icon_consts import *

class IconList(QResizableWidget):
    """docstring for IconList"""
    DEFAULT_COLS = 5
    DEFAULT_ROWS = 2

    def __init__(self, parent, game_objects):
        super(IconList, self).__init__(parent)
        self.set_show_idle_time(False)
        self.set_geomatry_by_grid(IconList.DEFAULT_COLS, IconList.DEFAULT_ROWS)
        self.game_obj = game_objects
        self.list = OrderedDict()
        for i, obj in enumerate(game_objects):
            x,y = self.set_xy(i)
            self.list[obj] = Icon(self, x, y, obj, self.show_idle_time)
            self.list[obj].show()

            #print(obj.udata.name)
    def set_show_idle_time(self, boolean)
        self.show_idle_time = boolean
        self.y_margin = IDLE_COUNTER_HEIGHT + SPACE_BETWEEN_COUNTER_AND_ICON if self.show_idle_time else 0
        self.set_geomatry_by_grid(self.cols, self.rows)
            
    def set_geomatry_by_grid(self, cols, rows):
        new_width = cols * ICON_SIZE_PX
        new_height = rows * (ICON_SIZE_PX + self.y_margin)
        self.rows = rows
        self.cols = cols
        self.setGeometry(self.x(), self.y(), new_width, new_height)

    def resize(self, position):
        # Position of mouse cursor
        x, y = position.x(), position.y()
        # Set new rows/cols
        cols = (x//ICON_SIZE_PX) if (x//ICON_SIZE_PX) > 0 else 1
        rows = (y//(ICON_SIZE_PX + self.y_margin)) if (y//(ICON_SIZE_PX + self.y_margin)) > 0 else 1
        # Set geometry
        self.set_geomatry_by_grid(cols, rows)

    def set_xy(self, index):
        if self.expand_index == 0:
            # Right, bottom
            x = index % self.cols
            y = index // self.cols
        elif self.expand_index == 1:
            # Right and up
            x = index % self.cols
            y = self.rows - index // self.cols - 1
        elif self.expand_index == 2:
            # Left Down
            x = self.cols - index % self.cols - 1 
            y = index // self.cols
        elif self.expand_index == 3:
            # Left Up
            x = self.cols - index % self.cols - 1 
            y = self.rows - index // self.cols - 1
            ###############################################
        elif self.expand_index == 4:
            # Down Left
            x = self.cols - index // self.rows - 1 
            y = index % self.rows
        elif self.expand_index == 5:
            # Up Left
            x = self.cols - index // self.rows - 1 
            y = self.rows - index % self.rows - 1
        elif self.expand_index == 6:
            # Down Right
            x = index // self.rows
            y = index % self.rows
        elif self.expand_index == 7:
            # Up Rihgt
            x = index // self.rows
            y = self.rows - index % self.rows - 1
        return x, y
        print("waat")
        return 0, 0


    def update(self):
        #print(len(self.game_obj))
        for obj in self.list:
            self.list[obj].delete_me = True
        for obj in self.game_obj:
            if obj not in self.list:
                x, y = self.set_xy(len(self.list))
                self.list[obj] = Icon(self, x, y, obj, self.show_idle_time)
            self.list[obj].delete_me = False
            #self.list[obj].bottom_text, self.list[obj].top_text = self.list[obj].get_carrying()
            #self.list[obj].bottom_text, self.list[obj].top_text = self.list[obj].get_max_hp(), self.list[obj].get_hp()
            #self.list[obj].bottom_text, self.list[obj].top_text = self.list[obj].get_construction(), self.list[obj].get_hp()
            #a = self.list[obj].get_armors()
            #b = self.list[obj].get_attack()
            self.list[obj].bottom_text, self.list[obj].top_text = "", ""
            self.list[obj].redraw()
        removes = []
        for obj in self.list:
            if self.list[obj].delete_me:
                removes += [obj]
        for obj in removes:
            self.list[obj].deleteLater()
            del self.list[obj]

                

        



if __name__ == '__main__':
    import bartender
        
        