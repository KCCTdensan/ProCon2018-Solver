import random
from .Player import Player

class AI(Player):
    def intention(self,Game):#盤面の情報を渡してAgentの動かし方を返す
        self._Intention = [[random.randint(-1, 1), random.randint(-1, 1), random.randint(0, 1)], [random.randint(-1, 1), random.randint(-1, 1), random.randint(0, 1)]]
        return self._Intention