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
        self.y_margin = 0 
        self.set_geomatry_by_grid(IconList.DEFAULT_COLS, IconList.DEFAULT_ROWS)
        self.show_idle_time = False
        self.aggr = True
        self.game_obj_f = lambda: []
        self.timer_f = lambda obj: ""
        self.top_text_f = lambda obj: ""
        self.bottom_text_f = lambda obj: ""
        self.list = OrderedDict()
        for i, obj in enumerate(game_objects):
            x,y = self.set_xy(i)
            self.list[obj] = Icon(self, x, y, obj, self.show_idle_time, self.aggr)
            self.list[obj].show()
           
            
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

    def check_icons(self, game_objects, aggr=True): # maybe better name of this function
        # Set all icons to be removed from the bar
        for obj in self.list:
            self.list[obj].delete_me = True
        # Iterate through the list of objects
        for obj in game_objects:
            if obj not in self.list: # Check if the object is new -> create it
                self.list[obj] = Icon(self, 0, 0, obj, self.show_idle_time, aggr)
            # Object is used -> do not delete it
            self.list[obj].delete_me = False
        # Iterate through the objects which do have `delete_me == True`.
        for obj in list(filter(lambda x, d=self.list: d[x].delete_me, self.list)):
            self.list[obj].deleteLater()
            del self.list[obj]

    def get_aggregate_dictionary(self, dictionary):
        for key in dictionary:
            if dictionary[key]:
                first_obj = dictionary[key][0]
                first_obj.list = dictionary[key]
                yield dictionary[key][0] # returns first item in aggregate list

    def update(self):
        game_objects = self.game_obj_f()
        if game_objects and type(game_objects[0]) is list:
            game_objects = self.get_aggregate_dictionary(game_objects)
            if not self.aggr:
                self.check_icons([], True)
                self.aggr = True
            self.check_icons(game_objects, True)
        else:
            if self.aggr:
                self.check_icons([], True)
                self.aggr = False
            self.check_icons(game_objects, False)
        # Update the position of all objects 
        for i, obj in enumerate(self.list):
            self.list[obj].set_position(* self.set_xy(i))
            # Update texts and redraw it
            self.list[obj].timer_text = self.timer_f(obj)
            self.list[obj].top_text = self.top_text_f(obj)
            self.list[obj].bottom_text = self.bottom_text_f(obj)
            self.list[obj].redraw()

        



if __name__ == '__main__':
    import bartender
        
        