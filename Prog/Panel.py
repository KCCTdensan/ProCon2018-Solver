class Panel:
	def __init__(self, score:int): #パネル生成
		self._score = score #パネルが持つ点数
		self._state = 0 #パネルの状態(0:中立，1:1P，2:2P)
		self._surrounded = [False, False] #パネルが囲まれているか(False:囲まれていない, True:パネルに囲まれている)

	
	def mkcard(self, team:int): #パネルにカードを置く(team:チーム)
		self._state = team


	def rmcard(self): #パネルに置いているカードを除去する
		self._state = 0


	def getScore(self):
		return self._score


	def getState(self):
		return self._state


	def getSurrounded(self)->list:
		return self._surrounded


	def setSurrounded(self, team:int, surrounded:bool):
		self._surrounded[team] = surrounded
