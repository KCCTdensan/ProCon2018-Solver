import numpy as np
import random as Ran
import math
import copy
from Panel import *
from Agent import *
from Window import *


class Game:
	def __init__(self): #ステージ生成
		self._turn = Ran.randint(60, 120) #最終ターン数
		self._1Pscore = 0 #1Pの得点
		self._2Pscore = 0 #2Pの得点
		#配列yの中に配列xが入る構造。定義時に行の中に列が入り込む、numpy.Zerosの仕様に基づく。
		_xLen = Ran.randint(3, 12)
		_yLen = Ran.randint(3, 12)
		Agentx = Ran.randint(0, (_xLen//2)-1)
		Agenty = Ran.randint(0, (_yLen//2)-1)
		self._1PAgents = [Agent([Agenty, Agentx],1),Agent([_yLen - 1 - Agenty, _xLen - 1 - Agentx],1)] #ステージに存在する1Pのエージェントのリスト
		self._2PAgents = [Agent([_yLen - 1 - Agenty, Agentx],2),Agent([Agenty, _xLen - 1 - Agentx],2)] #ステージに存在する2Pのエージェントのリスト
		self._Panels = [[Panel(0) for i in range(_xLen)]for j in range(_yLen)]
		self.randtype = Ran.randint(0,2);
		
		if self.randtype == 0:
			for y in range(_yLen//2):
				for x in range(_xLen//2):
					PanelsScore = Ran.randint(-5, 5)
					self._Panels[y][x] = Panel(PanelsScore)
					self._Panels[_yLen - 1 - y][x] = copy.copy(self._Panels[y][x])
					self._Panels[y][_xLen - 1 - x] = copy.copy(self._Panels[y][x])
					self._Panels[_yLen - 1 - y][ _xLen - 1 - x] = copy.copy(self._Panels[y][x])
		elif self.randtype == 1:
			for y in range(_yLen):
				for x in range(_xLen//2):
					PanelsScore = Ran.randint(-5, 5)
					self._Panels[y][x] = Panel(PanelsScore)
					self._Panels[y][_xLen - 1 - x] = copy.copy(self._Panels[y][x])
		elif self.randtype == 2:
			for y in range(_yLen//2):
				for x in range(_xLen):
					PanelsScore = Ran.randint(-5, 5)
					self._Panels[y][x] = Panel(PanelsScore)
					self._Panels[_yLen - y - 1][x] = copy.copy(self._Panels[y][x])
		self._Panels[Agenty][Agentx] = Panel(0)
		self._Panels[_yLen - 1 - Agenty][Agentx] = Panel(0)
		self._Panels[Agenty][_xLen - 1 - Agentx] = Panel(0)
		self._Panels[_yLen - 1 - Agenty][_xLen - 1 - Agentx] = Panel(0)
			
	def score(self): #得点計算
		regionPoint1 = 0
		regionPoint2 = 0
		NumY = len(self._Panels)
		NumX = len(self._Panels[0])
		searchedPanels = np.zeros_like(self._Panels, dtype = np.bool)
		self._1Pscore = 0
		self._2Pscore = 0

		def regionPoint(self, x:int, y:int, Team)->int:
			if searchedPanels[y][x]:
				return 0
			searchedPanels[y][x] = True
			if (y == 0)or(y == NumY - 1)or(x == 0)or(x == NumX - 1):
				return -1
			if self._Panels[y][x].getState() == Team:
				return -2
			l = regionPoint(self, x - 1, y, Team)
			if l == -1:
				return -1
			elif l == -2:
				return abs(self._Panels[y][x].getScore())
			t = regionPoint(self, x, y - 1, Team)
			if t == -1:
				return -1
			elif l == -2:
				return abs(self._Panels[y][x].getScore())
			r = regionPoint(self, x + 1, y, Team)
			if r == -1:
				return -1
			elif l == -2:
				return abs(self._Panels[y][x].getScore())
			b = regionPoint(self, x, y + 1, Team)
			if b == -1:
				return -1
			elif l == -2:
				return abs(self._Panels[y][x].getScore())
			return l + t + r + b

		for y in range(NumY):
			for x in range(NumX):
				p = self._Panels[y][x]
				state = p.getState()
				if state == 1:
					self._1Pscore += p.getScore()
				elif state == 2:
					self._2Pscore += p.getScore()
		#for y in range(NumY):
		#	for x in range(NumX):
		#		if not searchedPanels[y][x]:
		#			regionPoint1 = regionPoint(self, x, y, 1)
		#			if regionPoint1 >= 0:
		#				self._1Pscore += regionPoint1
		#for y in range(NumY):
		#	for x in range(NumX):
		#		if not searchedPanels[y][x]:
		#			regionPoint2 = regionPoint(self, x, y, 2)
		#			if regionPoint2 >= 0:
		#				self._2Pscore += regionPoint2

	def action(self,P1Intentions:list, P2Intentions:list): #エージェントの意思をみて，実際に移動orパネル操作
		#引数 P1Intensions:[[x,y],[x,y]]、P2Intentions:[[x,y],[x,y]]

		Intentions = [[P1Intentions[0][1], P1Intentions[0][0]], [P1Intentions[1][1], P1Intentions[1][0]], [P2Intentions[0][1], P2Intentions[0][0]], [P2Intentions[1][1], P2Intentions[1][0]]]
		CurrentPositions = [self._1PAgents[0]._point, self._1PAgents[1]._point, self._2PAgents[0]._point, self._2PAgents[1]._point]
		NextPositions = []
		for i in range(4):
			NextPositions.append([])
			for j in range(2):
				NextPositions[i].append(CurrentPositions[i][j] + Intentions[i][j])
		CanMove = [True, True, True, True]
		Team = [1, 1, 2, 2]
		Agents = [self._1PAgents[0], self._1PAgents[1], self._2PAgents[0], self._2PAgents[1]]		
		NumY = len(self._Panels)
		NumX = len(self._Panels[0])

		#アクション可能か判定
		for i in range(3):
			for j in range(i + 1, 4):
				tmp = not np.allclose(NextPositions[i], NextPositions[j])
				CanMove[i] = CanMove[i]and tmp
				CanMove[j] = CanMove[j]and tmp
		for i in range(4):
			if not CanMove[i]:
				continue
			py = NextPositions[i][0]
			px = NextPositions[i][1]
			CanMove[i] = (0 <= py)and(py < NumY)and(0 <= px)and(px < NumX)

		#移動またはパネルを返す
		for i in range(4):
			if not CanMove[i]:
				continue
			OperatedPanel = self._Panels[NextPositions[i][0]][NextPositions[i][1]]
			State = OperatedPanel.getState()
			if State == 0 or State == Team[i]:
				OperatedPanel.mkcard(Team[i])
				Agents[i].move(Intentions[i])
			else:
				OperatedPanel.rmcard()
		
	def getPanels(self):
		return self._Panels
