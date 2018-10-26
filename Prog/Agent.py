import numpy as np
from position import *

class Agent:
	def __init__(self, point:[int, int], team:int): #エージェント生成(point:座標,team:チーム)
		self._point = np.array(point) #座標
		self._team = team #所属チーム(1or2)

	def move(self,vector:[int, int]): #エージェントを動かす(vector:方向)
		self._point += np.array(vector)

	def getPoint(self):
		return self._point

	def getTeam(self):
		return self._team

	def getPosition(self):
		_position = position()
		_position.x = self._point[0]
		_position.y = self._point[1]
		return _position