import numpy as np
from Panel import *
from Agent import *
from Window import *

class Game:
	_turn: int #最終ターン数
	_1Pscore: int #1Pの得点
	_2Pscore: int #2Pの得点
	_Panels: np.array #ステージを構成するパネルのリスト
	_Agents: list #ステージに存在するエージェントのリスト

	def __init__(self): #ステージ生成
		pass

	def new(): #コンストラクタ呼び出し
		return Game()

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

	def main(self):
		#for turn in _turn:
			#Windowからエージェントの移動orパネル操作の意思を入力
			#移動orパネル操作
			#得点計算
			#盤面の情報をWindowに渡す
		pass