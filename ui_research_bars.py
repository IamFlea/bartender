from ui_iconlist import IconList


class ResearchBars(IconList):
    # docstring for ResearchBars fff
    DEFAULT_COLS = 1
    DEFAULT_ROWS = 5

    def __init__(self, name, parent):
        super(ResearchBars, self).__init__(name, parent)
        self.aggr = False
        self.parent = parent
        self.game_obj_f = lambda: parent.game.pov.research.progression
        self.set_geomatry_by_grid(ResearchBars.DEFAULT_COLS, ResearchBars.DEFAULT_ROWS)
        self.top_text_f = lambda obj: str(int(obj.cooldown))

    def set_magical_bar(self, boolean):
        self.set_right_margin(boolean)
        if boolean:
            self.top_text_f = lambda obj: ""
        else:
            self.top_text_f = lambda obj: str(int(obj.cooldown))


if __name__ == '__main__':
    pass
