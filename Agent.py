class Agent:
	_point: (int, int) #座標
	_team: int #所属チーム

	def __init__(self, point, team): #エージェント生成(point:座標,team:チーム)
		pass

	def new(point,team): #コンストラクタ呼び出し(point:座標,team:チーム)
		return Agent(point,team)

	def move(self,vector): #エージェントを動かす(vector:方向)
		pass
