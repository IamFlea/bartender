from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from aoc_time import *
from ui_consts import *
#font.setBold(True)

class HeaderLabel(QtWidgets.QLabel):
    """docstring for HeaderText"""
    def __init__(self, parent):
        super(HeaderLabel, self).__init__(parent)
        self.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.setFont(font)
        self.setStyleSheet("color: white")
        

class HeaderSP(QtWidgets.QWidget):
    """docstring for HeaderSP"""
    def __init__(self, parent, width):
        super(HeaderSP, self).__init__(parent)
        self.setGeometry(0,0, width, 42)

        self.left = QtWidgets.QWidget(self)
        self.left.setGeometry(394, 3, 490, 20)
        self.bg = QtWidgets.QWidget(self.left)
        self.bg.setStyleSheet("background-image: url(./ui/header_left.png);")
        self.bg.setGeometry(0,0,490,20)

        self.right = QtWidgets.QWidget(self)
        self.right.setGeometry(width - 490-255, 3, 490, 20)
        self.bg2 = QtWidgets.QWidget(self.right)
        self.bg2.setStyleSheet("background-image: url(./ui/header_right.png);")
        self.bg2.setGeometry(0,0,490,20)
        
        
        i = 0
        self.wood = HeaderLabel(self.left)
        self.wood.setGeometry(70*i, 0, 66, 20)
        i += 1
        self.food = HeaderLabel(self.left)
        self.food.setGeometry(70*i, 0, 66, 20)
        i += 1
        self.gold = HeaderLabel(self.left)
        self.gold.setGeometry(70*i, 0, 66, 20)
        i += 1
        self.stone = HeaderLabel(self.left)
        self.stone.setGeometry(70*i, 0, 66, 20)        
        i += 1
        self.fish = HeaderLabel(self.left)
        self.fish.setGeometry(70*i, 0, 66, 20)
        i += 1
        self.trade = HeaderLabel(self.left)
        self.trade.setGeometry(70*i, 0, 66, 20)
        i += 1
        self.idle = HeaderLabel(self.left)
        self.idle.setGeometry(70*i, 0, 66, 20)

        i = 0
        self.relics = HeaderLabel(self.right)
        self.relics.setGeometry(70*i, 0, 66, 20)
        i += 1
        self.civilians = HeaderLabel(self.right)
        self.civilians.setGeometry(70*i, 0, 66, 20)
        i += 1
        self.military = HeaderLabel(self.right)
        self.military.setGeometry(70*i, 0, 66, 20)
        i += 1
        self.kills_daths = HeaderLabel(self.right)
        self.kills_daths.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
        self.kills_daths.setGeometry(70*i, 0, 70+66, 20)
        i += 1
        i += 1
        self.razings = HeaderLabel(self.right)
        self.razings.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
        self.razings.setGeometry(70*i, 0, 70+66, 20)
        

    def load(self, player):
        self.wood.setText(HeaderSP.get_wood(player))
        self.food.setText(HeaderSP.get_food(player))
        self.gold.setText(HeaderSP.get_gold(player))
        self.stone.setText(HeaderSP.get_stone(player))
        self.fish.setText(HeaderSP.get_fish(player))
        self.trade.setText(HeaderSP.get_trade(player))
        self.idle.setText(HeaderSP.get_idle(player))
        ##
        self.relics.setText(HeaderSP.get_relics(player))
        self.civilians.setText(HeaderSP.get_civilians(player))
        self.military.setText(HeaderSP.get_military(player))
        self.kills_daths.setText(HeaderSP.get_kd_ratio(player))
        self.razings.setText(HeaderSP.get_razings(player))

    def get_razings(player):
        razed = int(player.resources.values[player.resources.keys.index("Razings")])
        lost = int(player.resources.values[player.resources.keys.index("Buildings Lost")])
        return f"{razed}/{lost}"
    def get_kd_ratio(player):
        killed = int(player.resources.values[player.resources.keys.index("Units Killed")])
        lost = int(player.resources.values[player.resources.keys.index("Units Lost")])
        return f"{killed}/{lost}"
    def get_military(player):
        return str(len(player.military))

    def get_civilians(player):
        return str(len(player.civilians))

    def get_relics(player):
        #idx = player.resources.keys.index("RelicsCaptured")
        #return str(int(player.resources.values[idx]))
        return str(player.farm_reseeds)

    def get_idle(player):
        result = sum(map(lambda vill: vill.idle, player.civilians))
        time = sum(map(lambda x: x.idle_total_time, player.civilians))
        time = str_idle(time)
        return f"{result} ({time})"

    def get_trade(player):
        amount = int(sum(map(lambda boat: boat.resource[0], player.trade))) 
        count = len(player.trade) - sum(map(lambda x: x.idle, player.trade))
        return f"{amount} ({count})"

    def get_fish(player):
        amount = int(sum(map(lambda boat: boat.resource[0], player.fish)))
        count = len(player.fish) - sum(map(lambda x: x.idle, player.fish))
        return f"{amount} ({count})"

    def get_stone(player):
        vills_with_stone = filter(lambda x : x.resource[1] == 2, player.villagers)
        amount = int(sum(map(lambda vill: vill.resource[0], vills_with_stone)))
        count = len(player.vill_stone) - sum(map(lambda x: x.idle, player.vill_stone))
        return f"{amount} ({count})"
        
    def get_gold(player):
        vills_with_gold = filter(lambda x : x.resource[1] == 3, player.villagers)
        amount = int(sum(map(lambda vill: vill.resource[0], vills_with_gold)))
        count = len(player.vill_gold) - sum(map(lambda x: x.idle, player.vill_gold))
        return f"{amount} ({count})"
    
    def get_food(player):
        vills_with_food = filter(lambda x : x.resource[1] not in [1,2,3], player.villagers)
        amount = int(sum(map(lambda vill: vill.resource[0], vills_with_food)))
        count = len(player.vill_food) - sum(map(lambda x: x.idle, player.vill_food))
        return f"{amount} ({count})"

    def get_wood(player):
        vills_with_wood = filter(lambda x : x.resource[1] == 1, player.villagers)
        amount = int(sum(map(lambda vill: vill.resource[0], vills_with_wood)))
        count = len(player.vill_wood) - sum(map(lambda x: x.idle, player.vill_wood))
        return f"{amount} ({count})"

if __name__ == '__main__':
    import bartender
