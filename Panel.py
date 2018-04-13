class Panel:
	def __init__(self, score:int): #パネル生成
		self._score = score #パネルが持つ点数
		self._state = 0 #パネルの状態(0が中立，1が1P，2が2P)
	
	def mkcard(self, team:int): #パネルにカードを置く(team:チーム)
		self._state = team

	def rmcard(self): #パネルに置いているカードを除去する
		self._state = 0
