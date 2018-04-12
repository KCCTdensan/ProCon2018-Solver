class Panel:
	_score: int #パネルが持つ点数
	_state: int #パネルの状態
	
	def __init__(self, score): #パネル生成
		pass
	
	def new(score): #コンストラクタ呼び出し
		return Panel(score)

	def mkcard(self, team): #パネルにカードを置く(team:チーム)
		pass

	def rmcard(self): #パネルに置いているカードを除去する
		pass
