import numpy as np

class Agent:
	_point: np.array([int, int]) #座標
	_team: int #所属チーム

	def __init__(self, point:[int, int], team:int): #エージェント生成(point:座標,team:チーム)
		self._point = np.array(point)
		self._team = team

	def new(point:[int, int], team:int): #コンストラクタ呼び出し(point:座標,team:チーム)
		return Agent(point,team)

	def move(self,vector:[int, int]): #エージェントを動かす(vector:方向)
		self._point += np.array(vector)