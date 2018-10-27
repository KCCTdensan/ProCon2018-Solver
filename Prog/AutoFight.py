from Game import Game
from Engine.Test_ai import AI
from Engine.kerasDQN_ai import kerasDQNPlayer

class AutoFight():
	def __init__(self):
		self._AI1 = kerasDQNPlayer(1)
		self._AI2 = AI()
		self._WinNum = 0

	def play(self):
		_Game = Game()
		while (not _Game.endGame()):
			Intentions1 = self._AI1.intention(_Game)
			Intentions2 = self._AI2.intention(_Game)
			_Game.action([Intentions1[0], Intentions1[1], Intentions2[0], Intentions2[1]])
			_Game.score()
			Winner = _Game.getWinner()
			Scores = _Game.getPoints()
			print("Winner :" + str(Winner))
			print("1PTileScore : "+str(Scores[0]))
			print("1PRegionScore : "+str(Scores[1]))
			print("2PTileScore : "+str(Scores[2]))
			print("2PRegionScore : "+str(Scores[3]))
			if Winner == 1: 
				self._WinNum += 1
				#self._AI1.learn(1)
			#elif Winner == 2: self._AI1.learn(-1)
			#elif Winner == 0: self._AI1.learn(0)

def AutoFight(self, num):
	for i in range(num):
		self.play()
		print("Win:"+str(self._WinNum)+"/"+str(i+1))
