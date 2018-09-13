from ui_icon import Icon


class IconOffscreenUnit(Icon):
    """docstring for IconOffscreenUnit"""

    def __init__(self, parent, obj):
        super(IconOffscreenUnit, self).__init__(parent, 0, 0, game_object=obj, idle_time=False, dont_change_icon=True,
                                                highlight_selected=False)

    def update_bottom(self, k):
        w = self.parent.width() - 42
        h = self.parent.height() - 42
        self.setGeometry(w * k, h, 42, 42)
        self.show()

    def update_right(self, k):
        w = self.parent.width() - 42
        h = self.parent.height() - 42
        self.setGeometry(w, h * k, 42, 42)
        self.show()

    def update_top(self, k):
        w = self.parent.width() - 42
        self.setGeometry(w * k, 0, 42, 42)
        self.show()

    def update_left(self, k):
        h = self.parent.height() - 42
        self.setGeometry(0, h * k, 42, 42)
        self.show()


if __name__ == '__main__':
    pass
