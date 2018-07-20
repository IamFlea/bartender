from ui_iconlist import IconList

from aoc_time import str_time
class ResearchList(IconList):
    """docstring for ResearchList"""
    def __init__(self, name, parent):
        super(ResearchList, self).__init__(name, parent)
        self.parent = parent

    def load_game(self):
        self.techs = self.parent.game.pov.research.done
        self.game_obj_f = lambda: self.parent.game.pov.research.done

    def set_magical_timer(self, boolean):
        self.set_y_margin(boolean)
        
        if boolean:
            self.timer_f = lambda obj: str_time(obj.time)
            print("Timer is set")
        else:
            self.timer_f = lambda obj: ""



if __name__ == '__main__':
    import bartender
        