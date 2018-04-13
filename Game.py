import numpy as np
import random as Ran
import math
from Panel import *
from Agent import *
from Window import *

class Game:
	_1PIntention: [[int, int]]*2
	_2PIntention: [[int, int]]*2 #エージェント(4人)の意思([int, int])を保存する変数のリスト

	def __init__(self): #ステージ生成
		self._turn = Ran.randint(60,120) #最終ターン数
		self._1Pscore = 0 #1Pの得点
		self._2Pscore = 0 #2Pの得点
		self._1PAgents = [[Agenty,Agentx],[_yLen - 1 - y,_xLen - 1 - x]] #ステージに存在する1Pのエージェントのリスト
		self._2PAgents = [[_yLen - 1 - y,x],[y,_xLen - 1 - x]] #ステージに存在する2Pのエージェントのリスト
		self._Panels = np.zeros([_yLen,_xLen]) #ステージを構成するパネルのリスト

		_xLen = Ran.randint(3,12)
		_yLen = Ran.randint(3,12)
		Agentx = Ran.randint(0,math.floor(_yLen/2))
		Agenty = Ran.randint(0,math.floor(_xLen/2))
		for x in range(math.ceil(_xLen/2)):
			for y in range(math.ceil(_yLen/2)):
				_Panels[y,x] = Ran.randint(-5,5)
				_Panels[_yLen - 1 - y,x] = _Panels[y,x]
				_Panels[y,_xLen - 1 - x] = _Panels[y,x]
				_Panels[_yLen - 1 - y,_xLen - 1 - x] = _Panels[y,x]
		_Panels[Agenty,Agentx] = 0
		_Panels[_yLen - 1 - Agenty,Agentx] = 0
		_Panels[Agenty,_xLen - 1 - Agentx] = 0
		_Panels[_yLen - 1 - Agenty,_xLen - 1 - Agentx] = 0

	def score(self): #得点計算
		panelPoint1 = 0
		panelPoint2 = 0
		regionPoint1 = 0
		regionPoint2 = 0
		NumY = len(_Panels)
		NumX = len(_Panels[0])
		searchedPanels = np.zeros_like(_Panels, dtype = np.bool)

		def regionPoint(self, x:int, y:int, player:int)->int:
			if searchedPanels[y][x]:
				return 0
			searchedPanels[y][x] = True
			if (y == 0)or(y == NumY - 1)or(x == 0)or(x == NumX - 1):
				return -1
			if _Panels[y][x].getState() == player:
				return -2
			l = regionPoint(self, x - 1, y, player)
			if l == -1:
				return -1
			elif l == -2:
				return abs(_Panels[y][x].getScore())
			t = regionPoint(self, x, y - 1, player)
			if t == -1:
				return -1
			elif l == -2:
				return abs(_Panels[y][x].getScore())
			r = regionPoint(self, x + 1, y, player)
			if r == -1:
				return -1
			elif l == -2:
				return abs(_Panels[y][x].getScore())
			b = regionPoint(self, x, y + 1, player)
			if b == -1:
				return -1
			elif l == -2:
				return abs(_Panels[y][x].getScore())
			return l + t + r + b

		for y in range(NumY):
			for x in range(NumX):
				p = _Panels[y][x]
				state = p.getState()
				if state == 1:
					panelPoint1 += p.getScore()
				elif state == 2:
					panelPoint2 += p.getScore()
		for y in range(NumY):
			for x in range(NumX):
				if not searchedPanels[y][x]:
					regionPoint1 = regionPoint(self, x, y, 1)
					if regionPoint >= 0:
						break
		for y in range(NumY):
			for x in range(NumX):
				if not searchedPanels[y][x]:
					regionPoint2 = regionPoint(self, x, y, 2)
					if regionPoint >= 0:
						break

	def action(self): #エージェントの意思をみて，実際に移動orパネル操作
		pass

	def main(self):
		for turn in range(_turn):
			#Windowからエージェントの移動orパネル操作の意思を入力
			self.action() #エージェントの意思をみて，実際に移動orパネル操作
			self.score() #得点計算
			#盤面の情報をWindowに渡す