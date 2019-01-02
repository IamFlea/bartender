from collections import OrderedDict
from math import sin
from time import time

from PyQt5 import QtWidgets

from aoc_research import Technology
from ui_icon import Icon
from ui_icon_consts import *
from ui_widget import QOverlayWidget


class IconList(QOverlayWidget):
    """docstring for IconList"""
    DEFAULT_COLS = 5
    DEFAULT_ROWS = 2

    def __init__(self, name, parent):
        super(IconList, self).__init__(name, parent)
        self.name = name
        self.y_margin = 0
        self.right_margin = 0
        self.set_geomatry_by_grid(IconList.DEFAULT_COLS, IconList.DEFAULT_ROWS)
        self.show_idle_time = False
        self.aggr = True
        self.game_obj_f = lambda: []
        self.timer_f = lambda obj: ""
        self.top_text_f = lambda obj: ""
        self.bottom_text_f = lambda obj: ""
        self.list = OrderedDict()
        self.max_pulse = 0
        self.max_blink = 0

    def set_y_margin(self, boolean):
        if self.aggr:
            return
        self.show_idle_time = boolean
        self.y_margin = IDLE_COUNTER_HEIGHT + SPACE_BETWEEN_COUNTER_AND_ICON if self.show_idle_time else 0
        self.set_geomatry_by_grid(self.cols, self.rows)
        if self.parent.game_running:
            self.check_icons([])

    def set_right_margin(self, boolean):
        if self.aggr:
            return
        self.add_width = boolean
        self.right_margin = SPACE_BETWEEN_ICON_AND_BAR + RESEARCH_BAR_WIDTH if boolean else 0
        self.set_geomatry_by_grid(self.cols, self.rows)
        if self.parent.game_running:
            self.check_icons([])

    def set_geomatry_by_grid(self, cols, rows):
        new_width = cols * (ICON_SIZE_PX + self.right_margin)
        new_height = rows * (ICON_SIZE_PX + self.y_margin)
        self.rows = rows
        self.cols = cols
        self.setGeometry(self.x(), self.y(), new_width, new_height)

    def resize(self, position):
        # Position of mouse cursor
        x, y = position.x(), position.y()
        # Set new rows/cols
        cols = (x // (ICON_SIZE_PX + self.right_margin)) if (x // (ICON_SIZE_PX + self.right_margin)) > 0 else 1
        rows = (y // (ICON_SIZE_PX + self.y_margin)) if (y // (ICON_SIZE_PX + self.y_margin)) > 0 else 1
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

    def check_icons(self, game_objects, aggr=True):  # maybe better name of this function
        # Set all icons to be removed from the bar
        for obj in self.list:
            self.list[obj].delete_me = True

        # Iterate through the list of objects
        for obj in game_objects:
            if obj not in self.list:  # Check if the object is new -> create it
                self.list[obj] = Icon(self, 0, 0, obj, self.show_idle_time, aggr)
                if self.right_margin != 0:  # and type(obj) is Technology
                    self.list[obj].set_right_margin(True)

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
                yield dictionary[key][0]  # returns first item in aggregate list

    def blinking(self, obj):
        return obj.idle and int(time()) % 2 and obj.idle_time < self.max_blink * 1000

    def pulsing(self, obj):
        if not self.aggr and obj.idle and obj.idle_time < self.max_pulse * 1000:
            return 155 + 50 * sin(time() * 4)
        else:
            return 255

    def check_tech(self, widget, obj):
        # This function should be called if margin is 0 
        if self.right_margin == 0:
            return
        try:
            widget.tech_frame
        except AttributeError:
            widget.tech_frame = QtWidgets.QWidget(widget)
            widget.tech_frame.setStyleSheet("background: black")
            widget.tech_bg = QtWidgets.QWidget(widget)
            widget.tech_bg.setStyleSheet("background: silver")
            widget.tech_progress = QtWidgets.QWidget(widget)
            widget.tech_frame.show()
            widget.tech_bg.show()
            widget.tech_progress.show()
            widget.tech_label = QtWidgets.QLabel(widget)
            widget.tech_label.setFont(bar_font)
            widget.tech_label.show()
            widget.tech_label.raise_()

        widget.tech_frame.setGeometry(RESEARCH_BAR_X, RESEARCH_BAR_Y, RESEARCH_BAR_WIDTH, RESEARCH_BAR_HEIGHT)
        widget.tech_bg.setGeometry(RESEARCH_BAR_X + 2, RESEARCH_BAR_Y + 2, RESEARCH_BAR_WIDTH - 4,
                                   RESEARCH_BAR_HEIGHT - 4)
        widget.tech_label.setGeometry(RESEARCH_BAR_X + 4, RESEARCH_BAR_Y + 2, RESEARCH_BAR_WIDTH - 4,
                                      RESEARCH_BAR_HEIGHT - 4)

        percentage = obj.time / obj.total_time
        width = RESEARCH_BAR_WIDTH - 4
        width = int(width * percentage)
        widget.tech_progress.setGeometry(RESEARCH_BAR_X + 2, RESEARCH_BAR_Y + 2, width, RESEARCH_BAR_HEIGHT - 4)
        widget.tech_progress.setStyleSheet("background: grey")
        widget.tech_label.setText(f"{int(obj.cooldown)} s")

    def update(self):
        game_objects = self.game_obj_f()
        # Check if we aggregate or not
        if game_objects and type(game_objects[0]) is list:
            # Aggregate
            game_objects = self.get_aggregate_dictionary(game_objects)
            if not self.aggr:
                # Init
                self.check_icons([], True)
                self.aggr = True
            self.check_icons(game_objects, True)
        else:
            # DO NOT Aggregate
            if self.aggr:
                # Init 
                self.check_icons([], True)
                self.aggr = False
            self.check_icons(game_objects, False)
        # Update the position of all objects 
        for i, obj in enumerate(self.list):
            self.list[obj].set_position(*self.set_xy(i))
            # Update texts and redraw it
            self.list[obj].timer_text = self.timer_f(obj)
            self.list[obj].top_text = self.top_text_f(obj)
            self.list[obj].bottom_text = self.bottom_text_f(obj)
            if type(obj) is not Technology:
                self.list[obj].blink = self.blinking(obj)
                self.list[obj].opacity = self.pulsing(obj)
            else:
                self.check_tech(self.list[obj], obj)

            self.list[obj].redraw()


if __name__ == '__main__':
    pass
