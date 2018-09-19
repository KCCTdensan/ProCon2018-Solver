import numpy as np
import os
import subprocess
import random as Ran
import math
import copy
from pyzbar.pyzbar import decode
from PIL import Image
from Panel import *
from Agent import *
from Window import *


class Game:
	#zbarのインストールが必要 URL: http://zbar.sourceforge.net/download.html

	def __init__(self):
		#QRコード読み取りステージ生成部分
		"""
		image = 'test.png' #QRコードの画像
		data = decode(Image.open(image))	#QRコードのデータ全体
		QRtext = str(data).split('\'')[1]	#QRコードのテキスト部分
		_yLen = int(QRtext.split(':')[0].split(' ')[0])	#ステージの縦*横(_yLen*_xLen)
		_xLen = int(QRtext.split(':')[0].split(' ')[1])
		Agentx = int(QRtext.split(':')[_yLen+1].split(' ')[0])-1	#1Pの1人目のエージェントのx,y座標
		Agenty = int(QRtext.split(':')[_yLen+1].split(' ')[1])-1
		self._1PAgents = [Agent([Agenty, Agentx],1),Agent([_yLen - 1 - Agenty, _xLen - 1 - Agentx],1)] #ステージに存在する1Pのエージェントのリスト
		self._2PAgents = [Agent([_yLen - 1 - Agenty, Agentx],2),Agent([Agenty, _xLen - 1 - Agentx],2)] #ステージに存在する2Pのエージェントのリスト		
		self._Panels = [[Panel(0) for i in range(_xLen)]for j in range(_yLen)] #パネルの配列の作成
		#パネルのスコア設定
		for y in range(_yLen):
			PanelsScores = QRtext.split(':')[y+1]
			for x in range(_xLen):
				PanelScore = int(PanelsScores.split(' ')[x])
				self._Panels[y][x] = Panel(PanelScore)
		"""
		self._turn = Ran.randint(60, 120) #最終ターン数
		self._1PTileScore = 0 #1Pのタイルポイント
		self._2PTileScore = 0 #2Pのタイルポイント
		self._1PRegionScore = 0 #1Pの領域ポイント
		self._2PRegionScore = 0 #1Pの領域ポイント

		#ランダムステージ作成部分
		#ステージの縦*横(_yLen*_xLen)
		_xLen = Ran.randint(3, 12)
		_yLen = Ran.randint(3, 12)
		_yLen2 = -(- _yLen//2)
		_xLen2 = -(- _xLen//2)
		#1Pの1人目のエージェントのx,y座標
		Agentx = Ran.randint(0, (_xLen//2)-1)
		Agenty = Ran.randint(0, (_yLen//2)-1)
		self._1PAgents = [Agent([Agenty, Agentx],1),Agent([_yLen - 1 - Agenty, _xLen - 1 - Agentx],1)] #ステージに存在する1Pのエージェントのリスト
		self._2PAgents = [Agent([_yLen - 1 - Agenty, Agentx],2),Agent([Agenty, _xLen - 1 - Agentx],2)] #ステージに存在する2Pのエージェントのリスト
		self.randtype = Ran.randint(0,2)	#左右対称、または上下対称、または上下左右対称
		self._Panels = [[Panel(0) for i in range(_xLen)]for j in range(_yLen)]	#パネルの配列の作成

		#パネルのスコア設定
		if self.randtype == 0: 
			for y in range(_yLen2): 
				for x in range(_xLen2):
					PanelsScore = Ran.randint(0,16)
					IsNegative = Ran.randint(0,9)
					if IsNegative == 0:
						PanelsScore = -PanelsScore
					self._Panels[y][x] = Panel(PanelsScore)
					self._Panels[_yLen - 1 - y][x] = Panel(PanelsScore)
					self._Panels[y][_xLen - 1 - x] = Panel(PanelsScore)
					self._Panels[_yLen - 1 - y][ _xLen - 1 - x] = Panel(PanelsScore)
		elif self.randtype == 1:
			for y in range(_yLen):
				for x in range(_xLen2):
					PanelsScore = Ran.randint(0,16)
					IsNegative = Ran.randint(0,9)
					if IsNegative == 0:
						PanelsScore = -PanelsScore
					self._Panels[y][x] = Panel(PanelsScore)
					self._Panels[y][_xLen - 1 - x] = Panel(PanelsScore)
		elif self.randtype == 2:
			for y in range(_yLen2):
				for x in range(_xLen):
					PanelsScore = Ran.randint(0,16)
					IsNegative = Ran.randint(0,9)
					if IsNegative == 0:
						PanelsScore = -PanelsScore
					self._Panels[y][x] = Panel(PanelsScore)
					self._Panels[_yLen - y - 1][x] = Panel(PanelsScore)

	def UpdatePanelSurrounded(self):
		NumY = len(self._Panels)
		NumX = len(self._Panels[0])
		checkedPanel = np.zeros((2, NumY, NumX), dtype = int)

		def set(x:int, y:int, team:int, surrounded:bool):
			if self._Panels[y][x].getState() == team + 1:
				self._Panels[y][x].setSurrounded(team, False)
				return
			if checkedPanel[team][y][x] == 2:
				return

			checkedPanel[team][y][x] = 2
			
			self._Panels[y][x].setSurrounded(team, surrounded)

			if x > 0:
				set(x - 1, y, team, surrounded)
			if y > 0:
				set(x, y - 1, team, surrounded)
			if x < NumX - 1:
				set(x + 1, y, team, surrounded)
			if y < NumY - 1:
				set(x, y + 1, team, surrounded)

		def check(x:int, y:int, team:int)->int:
			panelState = self._Panels[y][x].getState()
			if panelState == team + 1:
				return 1
			if checkedPanel[team][y][x] != 0:
				return -1
			
			checkedPanel[team][y][x] = 1

			if (x == 0) or (x == NumX - 1) or (y == 0) or (y == NumY - 1):
				set(x, y, team, False)
				return 0
			
			l = check(x - 1, y, team)
			if l == 0:
				return 0
			t = check(x, y + 1, team)
			if t == 0:
				return 0
			r = check(x + 1, y, team)
			if r == 0:
				return 0
			b = check(x, y - 1, team)
			if b == 0:
				return 0

			if (l == -1) and (t == -1) and (r == -1) and (b == -1):
				return -1
			else:
				return 1

		for t in range(2):
			for y in range(NumY):
				for x in range(NumX):
					if checkedPanel[t][y][x] == 0:
						ret = check(x, y, t)
						if ret == 1:
							set(x, y, t, True)
			
	def score(self): #得点計算
		regionPoint1 = 0
		regionPoint2 = 0
		NumY = len(self._Panels)
		NumX = len(self._Panels[0])
		self._1PTileScore = 0
		self._2PTileScore = 0
		self._1PRegionScore = 0
		self._2PRegionScore = 0

		self.UpdatePanelSurrounded()

		for y in range(NumY):
			for x in range(NumX):
				panel = self._Panels[y][x]
				panelState = panel.getState()
				panelScore = panel.getScore()
				panelSurrounded = panel.getSurrounded()
				if panelState == 0:
					if panelSurrounded[0]:
						self._1PRegionScore += abs(panelScore)
					if panelSurrounded[1]:
						self._2PRegionScore += abs(panelScore)
				elif panelState == 1:
					self._1PTileScore += panelScore
				elif panelState == 2:
					self._2PTileScore += panelScore

	def action(self, PlayerIntentions:list): #エージェントの意思をみて，実際に移動orパネル操作
		#引数 PlayerIntentions[[x,y,z],[x,y,z],[x,y,z],[x,y,z]] Player1:前2つ Player2:後2つ x,y:座標 z:0で移動 1でパネル除去

		Intentions = [[PlayerIntentions[0][1], PlayerIntentions[0][0],PlayerIntentions[0][2]], [PlayerIntentions[1][1], PlayerIntentions[1][0],PlayerIntentions[1][2]], [PlayerIntentions[2][1], PlayerIntentions[2][0],PlayerIntentions[2][2]], [PlayerIntentions[3][1], PlayerIntentions[3][0],PlayerIntentions[3][2]]]
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
				CanMove[i] = CanMove[i] and tmp
				CanMove[j] = CanMove[j] and tmp
		for i in range(4):
			if not CanMove[i]:
				continue
			py = NextPositions[i][0]
			px = NextPositions[i][1]
			CanMove[i] = (0 <= py) and (py < NumY) and (0 <= px) and (px < NumX)

		#移動またはパネルを返す
		for i in range(4):
			if not CanMove[i]:
				continue
			OperatedPanel = self._Panels[NextPositions[i][0]][NextPositions[i][1]]
			State = OperatedPanel.getState()
			if Intentions[i][2] == 0:
				if (State == 0) or (State == Team[i]):
					OperatedPanel.mkcard(Team[i])
					Agents[i].move(Intentions[i])
			else:
				if not State == 0:
					OperatedPanel.rmcard()
		
	def getPanels(self):
		return self._Panels

	def getPoints(self)->list:
		return [self._1PTileScore, self._1PRegionScore, self._2PTileScore, self._2PRegionScore]