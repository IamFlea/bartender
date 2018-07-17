# Class inherience
from ui_icon_graphics import IconGraphics
# For typecheck
from aoc_object_building import Building
from aoc_object_building_research import BuildingResearch
from aoc_object_building_queue import UnitQueue
from aoc_object_unit import Unit
from aoc_object_primitive import Primitive
from aoc_research import Research

class Icon(IconGraphics):
    """Adapter? between the Icon and GameObjects """
    def __init__(self, parent, x, y, game_object=None, idle_time = True, dont_change_icon = False, highlight_selected=False):
        """
        @param parent  - parent widget
        @param x, y    - position in the grid i.e [0,0] [0,1] .. [1,2].. 
        """
        super(Icon, self).__init__(parent, x, y, idle_time)
        self.object = game_object if game_object is not list else game_object[0]

        self.show_training = not dont_change_icon  # Huh? Refactor later.
        self.show_research = not dont_change_icon  
        self.highlight_selected = not dont_change_icon or highlight_selected

        self.bottom_text = ""
        self.top_text = ""
        self.timer_text = ""



    @property
    def icon(self):
        # Save self.object into temporary variable
        obj = self.object
        # Check the type
        if type(obj) is Building:
            directory = "/icons/buildings/"
            filename = str(obj.udata.icon).zfill(3) + ".bmp"
            if obj.research and self.show_research:
                obj = obj.research
            elif obj.queue and self.show_training: 
                obj = obj.queue
        if type(obj) in [Unit, Primitive]:
            directory = f"/icons/units/color_{self.color}/"
            filename = str(obj.udata.icon).zfill(3) + ".bmp"
        if type(obj) is UnitQueue:
            directory = f"/icons/units/color_{self.color}/"
            filename = str(obj[0][1]).zfill(3) + ".bmp"
        if type(obj) is Research:
            directory = "/icons/researches/"
            filename = str(obj.icon).zfill(3) + ".bmp"
        if type(obj) is BuildingResearch:
            directory = "/icons/researches/"
            filename = str(obj.icon).zfill(3) + ".bmp"
        #print(obj.name)
        return directory + filename 

    @property
    def color(self):
        return str(self.object.owner.color.color)

    @property
    def frame_color(self):
        if self.highlight_selected and self.object.selected:
            return ""
        else:
            return self.color



if __name__ == '__main__':
    import bartender

