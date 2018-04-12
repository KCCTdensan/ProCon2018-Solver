class Panel:
	_score: int #パネルが持つ点数
	_state: int #パネルの状態(0が中立，1が1P，2が2P)
	
	def __init__(self, score:int): #パネル生成
		self._score = score
		self._state = 0
	
	def new(score:int): #コンストラクタ呼び出し
		return Panel(score)

	def mkcard(self, team:int): #パネルにカードを置く(team:チーム)
		self._state = team

	def rmcard(self): #パネルに置いているカードを除去する
		self._state = 0
