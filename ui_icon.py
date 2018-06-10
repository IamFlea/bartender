# Class inherience
from ui_icon_graphics import IconGraphics
# For typecheck
from aoc_object_building import Building
from aoc_object_building_research import BuildingResearch
from aoc_object_building_queue import UnitQueue
from aoc_object_unit import Unit
from aoc_object_primitive import Primitive
from aoc_research import Research
from aoc_object_clist import Attack, Armor


def numtoss(number):
    if number == 0:
        return ""
    tostr = lambda x: str(int(x))
    if number < 1:
        # Get tenths 
        tenths = tostr(number*10)
        return "." + tenths 
    if number >= 10000:
        number /= 1000
        return tostr(number) + "k"
    elif number >= 1000:
        number2 = (number%1000)/100
        number /= 1000
        return tostr(number) + "." + tostr(number2)+ "k"
    return tostr(number)



class Icon(IconGraphics):
    """Adapter? between the Icon and GameObjects """
    def __init__(self, parent, x, y, game_object=None, idle_time = True):
        """
        @param parent  - parent widget
        @param x, y    - position in the grid i.e [0,0] [0,1] .. [1,2].. 
        """
        super(Icon, self).__init__(parent, x, y, idle_time)
        self.object = game_object if game_object is not list else game_object[0]
        self.show_training = True
        self.show_research = True
        self.highlight_selected = True

        self.bottom_text = ""
        self.top_text = ""
        self.idle_time_text = ""

    def queue_size(self):
        pass

    @property
    def icon(self):
        # Save self.object into temporary variable
        obj = self.object
        # Check the type
        if type(obj) is Building:
            directory = "/icons/buildings/"
            filename = str(obj.udata.icon).zfill(3) + ".bmp"
            if obj.queue and self.show_training: 
                obj = obj.queue
            elif obj.research and self.show_research:
                obj = obj.research
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
        return directory + filename 

    @property
    def color(self):
        return str(self.object.owner.color.color)

    @property
    def frame_color(self):
        if self.highlight_selected and self.object in self.object.owner.selected:
            return ""
        else:
            return self.color

    def get_queue(self):
        if self.object.queue:
            return str(self.object.queue.length)
        else:
            return ""

    def get_carrying(self):
        # returns amount and type
        if type(self.object) is Unit:
            return str(int(self.object.resource[0])), str(Primitive.ResourceTable[self.object.resource[1]][:1])
        else:
            return "", ""

    def get_cooldown(self):
        cooldown = self.object.construction # None if standing
        if self.object.training:
            cooldown = self.object.training.cooldown
        elif self.object.research:
            cooldown = self.object.research.cooldown
        return numtoss(cooldown) if cooldown is not None else ""

    def get_max_hp(self):
        return numtoss(self.object.udata.max_hp)

    def get_hp(self):
        return numtoss(self.object.hp)

    def get_construction(self):
        try:
            return numtoss(self.object.construction)
        except:
            return ""


    def get_attack(self, type="4 - Base Melee", display_blacksmith=False):
        attack_type = Attack.BONUS_CLASS.index(type)
        for type, amount in self.object.udata.attack:
            if attack_type == type:
                if display_blacksmith:
                    d = self.object.udata.attack.displayed
                    return str(d) + "+" + str(amount-d)                    
                else:
                    return str(amount)
        return ""


    def get_armor(self, type="4 - Base Melee", display_blacksmith=False):
        armor_type = Armor.BONUS_CLASS.index(type)
        for type, amount in self.object.udata.armor:
            if armor_type == type:
                if display_blacksmith:
                    d = self.object.udata.armor.displayed
                    return str(d) + "+" + str(amount-d)
                else:
                    return str(amount)
        return ""

    def get_pierce_armor(self, type="3 - Base Pierce", display_blacksmith=False):
        armor_type = Armor.BONUS_CLASS.index(type)
        for type, amount in self.object.udata.armor:
            if armor_type == type:
                if display_blacksmith:
                    d = self.object.udata.armor.displayed_pierce
                    return str(d) + "+" + str(amount-d)
                else:
                    return str(amount)
        return ""
                
    def get_armors(self):
        return self.get_armor() + "/" + self.get_pierce_armor()
    """
    def update(self):
        self.bottom_text = self.get_queue()
        self.top_text = self.get_cooldown()
        self.redraw()
    """



if __name__ == '__main__':
    import bartender

