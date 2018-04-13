import numpy as np
from Panel import *
from Agent import *
from Window import *

class Game:
	_turn: int #最終ターン数
	_1PpanelScore: int #1Pの得点
	_1PregionScore: int #1Pの得点
	_2PpanelScore: int #2Pの得点
	_2PregionScore: int #2Pの得点
	_Panels: np.array #ステージを構成するパネルのリスト
	_Agents: list #ステージに存在するエージェントのリスト

	def __init__(self): #ステージ生成
		self.Panels = np.array([\
			[0, 0, 0, 0, 0, 0, 0],\
			[0, 0, 0, 1, 0, 0, 0],\
			[0, 0, 1, 0, 0, 0, 0],\
			[0, 0, 0, 0, 0, 0, 0],\
			[0, 0, 0, 0, 0, 0, 0],\
			[0, 0, 0, 0, 0, 0, 0],\
			[0, 0, 0, 0, 0, 0, 0],\
			[0, 0, 0, 0, 0, 0, 0],\
			]) #???

	def new(): #コンストラクタ呼び出し
		return Game()

	def score(self): #得点計算
		panelPoint1 = 0
		panelPoint2 = 0
		regionPoint1 = 0
		regionPoint2 = 0
		self.NumY = len(self.Panels)
		self.NumX = len(self.Panels[0])
		searchedPanels = [np.zeros_like(self.Panels, dtype = np.bool), np.zeros_like(self.Panels, dtype = np.bool)]

		def regionPoint(self, x:int, y:int, player:int)->int:
			if searchedPanels[player - 1][y][x]:
				return 0
			searchedPanels[player - 1][y][x] = True
			if (y == 0)or(y == self.NumY - 1)or(x == 0)or(x == self.NumX - 1):
				return -1
			if self.Panels[y][x] == player:
				return -2
			l = regionPoint(self, x - 1, y, player)
			if l == -1:
				return -1
			elif l == -2:
				return abs(self.Panels[y][x].getScore())
			t = regionPoint(self, x, y - 1, player)
			if t == -1:
				return -1
			elif l == -2:
				return abs(self.Panels[y][x].getScore())
			r = regionPoint(self, x + 1, y, player)
			if r == -1:
				return -1
			elif l == -2:
				return abs(self.Panels[y][x].getScore())
			b = regionPoint(self, x, y + 1, player)
			if b == -1:
				return -1
			elif l == -2:
				return abs(self.Panels[y][x].getScore())
			return l + t + r + b

		for y in range(self.NumY):
			for x in range(self.NumX):
				p = self.Panels[y][x]
				state = p
				if state == 1:
					panelPoint1 += p.getScore()
				elif state == 2:
					panelPoint2 += p.getScore()
		for y in range(self.NumY):
			for x in range(self.NumX):
				if not searchedPanels[0][y][x]:
					regionPoint1 = regionPoint(self, x, y, 1)
					if regionPoint1 >= 0:
						break
		for y in range(self.NumY):
			for x in range(self.NumX):
				if not searchedPanels[1][y][x]:
					regionPoint2 = regionPoint(self, x, y, 2)
					if regionPoint2 >= 0:
						break
		self.panelScore1P = panelPoint1
		self.regionScore1P = regionPoint1
		self.panelScore2P = panelPoint2
		self.regionScore2P = regionPoint2

	def printScore(self): #デバッグ用
		return print(self.panelScore1P, self.regionScore1P, self.panelScore1P, self.regionScore2P)

	def printPanel(self): #デバッグ用
		print(self.Panels)

	def main(self):
		#for turn in _turn:
			#Windowからエージェントの移動orパネル操作の意思を入力
			#移動orパネル操作
			#得点計算
			#盤面の情報をWindowに渡す
		pass