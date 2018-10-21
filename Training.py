from Game import Game
from Engine.Test_ai import AI
from Engine.kerasDQN_ai import kerasDQNPlayer

class Training():
    def __init__(self):
        self._AI1 = kerasDQNPlayer(1)
        self._AI2 = AI()

    def play(self):
        _Game = Game()
        while(not _Game.endGame()):
            Intentions1 = self._AI1.intention(_Game)
            Intentions2 = self._AI2.intention(_Game)
            _Game.action([Intentions1[0], Intentions1[1], Intentions2[0], Intentions2[1]])
        Winner = _Game.getWinner()
        print("Winner :" + str(Winner))
        if Winner == 1: self._AI1.learn(1)
        elif Winner == 2: self._AI1.learn(-1)
        elif Winner == 0: self._AI1.learn(0)
    
    def train(self, num):
        for i in range(num):self.play() 
