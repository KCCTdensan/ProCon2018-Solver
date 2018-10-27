import numpy as np
import os
import subprocess
import random as Ran
import math
import copy
import pickle
from pyzbar.pyzbar import decode
from PIL import Image
from .Panel import *
from .Agent import *
from .Window import *
from .intention import *
from .position import *

class intention_info:
	def __init__(self):
		self.Delta = intention(0)
		self.ExpectedPosition = position()
		self.NextPosition = position()
		self.CanAct = 0

class Game:
	#zbarのインストールが必要 URL: http://zbar.sourceforge.net/download.html

	def __init__(self):
		#QRコード読み取りステージ生成部分
		image = 'test.jpg' #QRコードの画像
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
		self._gamecount=1 #試合回数（ファイル番号）
		while os.path.isfile("./Log/log"+str(self._gamecount)+".pickle"): #もうすでにその試合回数（ファイル番号）のログが存在すれば
			self._gamecount+=1 #試合回数（ファイル番号） = 試合回数（ファイル番号） + 1

		self._turn = 0 #ターン数
		self._lastTurn = Ran.randint(60, 120) #最終ターン数
		self._1PTileScore = 0 #1Pのタイルポイント
		self._2PTileScore = 0 #2Pのタイルポイント
		self._1PRegionScore = 0 #1Pの領域ポイント
		self._2PRegionScore = 0 #1Pの領域ポイント

		"""
		#ランダムステージ作成部分
		#ステージの縦*横(_yLen*_xLen)
		_xLen = Ran.randint(3, 12)
		_yLen = Ran.randint(3, 12)
		self._XLen = _xLen
		self._YLen = _yLen
		_yLen2 = -(- _yLen//2)
		_xLen2 = -(- _xLen//2)
		#1Pの1人目のエージェントのx,y座標
		Agentx = Ran.randint(0, (_xLen//2)-1)
		Agenty = Ran.randint(0, (_yLen//2)-1)
		self._1PAgents = [Agent([Agenty, Agentx],1),Agent([_yLen - 1 - Agenty, _xLen - 1 - Agentx],1)] #ステージに存在する1Pのエージェントのリスト
		self._2PAgents = [Agent([_yLen - 1 - Agenty, Agentx],2),Agent([Agenty, _xLen - 1 - Agentx],2)] #ステージに存在する2Pのエージェントのリスト
		self.Agents = [[self._1PAgents[0], self._1PAgents[1]], [self._2PAgents[0], self._2PAgents[1]]]
		self.Agents4 = [self._1PAgents[0], self._1PAgents[1], self._2PAgents[0], self._2PAgents[1]]
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
		"""

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
		
	def canAction(self, Intention, AgentNum):#アクション可能か判定
		Agent = self.Agents4[AgentNum]
		CurrentPosition = np.append(Agent.getPoint(), 0)
		action = Intention[AgentNum][2]
		actionPosition = CurrentPosition + Intention[AgentNum]

		#map内かどうかを確認
		py = actionPosition[0]
		px = actionPosition[1]
		NumY = len(self._Panels)
		NumX = len(self._Panels[0])
		if not ((0 <= py) and (py < NumY) and (0 <= px) and (px < NumX)):return False

		OperatedPanel = self._Panels[actionPosition[0]][actionPosition[1]]
		if action == 0:#移動の場合、敵パネルがないかどうか、パネル除去しようとしてる人がいないかどうか
			if OperatedPanel.getState() + Agent.getTeam()==3: return False
			for i,agent in enumerate(self.Agents4):
				if not agent is Agent:
					if np.allclose(agent.getPoint(),np.array([actionPosition[0],actionPosition[1]])) and Intention[i][2] == 1:
						return False
		elif action == 1:#除去の場合、パネルがあるかどうか、パネル除去してる人がいないかどうか
			if CurrentPosition[0] == actionPosition[0] and CurrentPosition[1] == actionPosition[1]:
				return False
			for i,agent in enumerate(self.Agents4):
				if not agent is Agent:
					if np.allclose(agent.getPoint(),np.array([actionPosition[0],actionPosition[1]])) and Intention[i][2] == 1:
						return False
		return True

	def action(self, PlayerIntentions:list): #エージェントの意思をみて，実際に移動orパネル操作
		#引数 PlayerIntentions[[x,y,z],[x,y,z],[x,y,z],[x,y,z]] Player1:前2つ Player2:後2つ x,y:座標 z:0で移動 1でパネル除去

		Intentions = [[PlayerIntentions[0][1], PlayerIntentions[0][0],PlayerIntentions[0][2]], [PlayerIntentions[1][1], PlayerIntentions[1][0],PlayerIntentions[1][2]], [PlayerIntentions[2][1], PlayerIntentions[2][0],PlayerIntentions[2][2]], [PlayerIntentions[3][1], PlayerIntentions[3][0],PlayerIntentions[3][2]]]

		for i in range(len(Intentions)):
			if(not self.canAction(Intentions, i)):Intentions[i]=[0,0,0]

		def clearOverlap(PlayerIntentions):#action先の重複をなくす
			CurrentPositions = [self._1PAgents[0]._point, self._1PAgents[1]._point, self._2PAgents[0]._point, self._2PAgents[1]._point]
			
			#action先の座標を出す
			actionPositions = []
			for i in range(4):
				actionPositions.append([])
				for j in range(2):
					actionPositions[i].append(CurrentPositions[i][j] + PlayerIntentions[i][j])
			
			Overlap = False
			for i in range(3): #移動後のAgent同士の座標被りを調べる
				for j in range(i + 1, 4):
					if(np.allclose(actionPositions[i], actionPositions[j])):
						PlayerIntentions[i]=[0,0,0]
						PlayerIntentions[j]=[0,0,0]#行動が被っているAgentのIntentionを[0,0,0]に
						Overlap = True
			if(not Overlap):return PlayerIntentions #action先の被りがなかった場合、return PlayerIntentions)
			return clearOverlap(PlayerIntentions)
		
		Intentions = clearOverlap(Intentions)

		#移動またはパネルを返す
		
		CurrentPositions = [self._1PAgents[0]._point, self._1PAgents[1]._point, self._2PAgents[0]._point, self._2PAgents[1]._point]
		Agents = [self._1PAgents[0], self._1PAgents[1], self._2PAgents[0], self._2PAgents[1]]

		#action先の座標を出す
		actionPositions = []
		for i in range(4):
			actionPositions.append([])
			for j in range(2):
				actionPositions[i].append(CurrentPositions[i][j] + Intentions[i][j])

		for i in range(4):
			OperatedPanel = self._Panels[actionPositions[i][0]][actionPositions[i][1]]
			if Intentions[i][2] == 0:#移動
				OperatedPanel.mkcard(Agents[i].getTeam())
				Agents[i].move([Intentions[i][0],Intentions[i][1]])
			elif Intentions[i][2] == 1: #除去
				OperatedPanel.rmcard()

		logfile = open("./Log/log"+str(self._gamecount)+".pickle","ab") #ログファイル出力準備
		pickle.dump(self,logfile) #gameobjectバイナリ出力
		pickle.dump(Intentions,logfile) #Intentionsバイナリ出力
		logfile.close

		self._turn+=1 #ターン経過
	
	def readMatchLog(self,num): #指定された試合のログを呼び出す

		self.printMatchLog(num)

		try:
			logfile = open("./Log/log"+str(num)+".pickle","rb") #ログファイル入力準備
		except FileNotFoundError:
			print("log"+str(num)+".pickleがなくて開けません")
			return 
		try:
			bin = pickle.load(logfile)
		except EOFError:
			print("EOFerror log"+str(num)+".pickleのログがないです")
			logfile.close
			return

		game_logs =[]
		intention_logs = []
		result = 0

		while not type(bin) is int:
			try:
				game_logs.append(bin)
				bin = pickle.load(logfile)
				intention_logs.append(bin)
				bin = pickle.load(logfile)
			except EOFError:
				print("EOFerror log"+str(num)+".pickleのログが最後まで取れていない可能性があります")
				logfile.close
				return game_logs,intention_logs

		result = bin
		logfile.close
		return game_logs,intention_logs,result

	def printMatchLog(self,num): #指定された試合のログをprintする 
		try:
			logfile = open("./Log/log"+str(num)+".pickle","rb") #ログファイル入力準備
		except FileNotFoundError:
			print("log"+str(num)+".pickleがなくて開けません")
			return 
		try:
			bin = pickle.load(logfile)
		except EOFError:
			print("EOFerror log"+str(num)+".pickleのログがないです")
			logfile.close
			return

		turncount = 1

		while not type(bin) is int:
			try:
				print(str(turncount)+"ターン目")
				print("Game")
				print(bin)
				bin = pickle.load(logfile)
				print("Intentions")
				print(bin)
				bin = pickle.load(logfile)
				turncount+=1
			except EOFError:
				print("EOFerror log"+str(num)+".pickleのログが最後まで取れていない可能性があります")
				logfile.close
				return
		
		print("試合結果")
		print(bin)
		if bin == 0:
			print("引き分け")
		elif bin == 1:
			print("1Pチーム勝利")
		elif bin == 2:
			print("2Pチーム勝利")

		logfile.close

	def rewindOneTurn(self):
		if not self.readMatchLog(self._gamecount) is None:
			games,intentions = self.readMatchLog(self._gamecount)
		else:
			return self

		if len(games) <= 1:
			print("一手戻れません（一番最初のターンになってる）")
			return self

		rewindGame = games[-2]

		os.remove("./Log/log"+str(self._gamecount)+".pickle")

		logfile = open("./Log/log"+str(self._gamecount)+".pickle","ab")

		for game,intention in zip(games[:-1],intentions[:-1]):
			pickle.dump(game,logfile) #gameobjectバイナリ出力
			pickle.dump(intention,logfile) #Intentionsバイナリ出力
		
		logfile.close

		return rewindGame

	def getPanels(self):
		return self._Panels

	def getPoints(self)->list:
		return [self._1PTileScore, self._1PRegionScore, self._2PTileScore, self._2PRegionScore]

	def getAgents(self)->list:
		return [self._1PAgents[0], self._1PAgents[1], self._2PAgents[0], self._2PAgents[1]]

	def endGame(self):
		logfile = open("./Log/log"+str(self._gamecount)+".pickle","ab") #ログファイル出力準備
		if self._turn==self._lastTurn:
			pickle.dump(self.getWinner(),logfile)
			logfile.close
			return True
		else: return False

	def getWinner(self):
		Player1Score = self._1PTileScore + self._1PRegionScore
		Player2Score = self._2PTileScore + self._2PRegionScore
		if Player1Score == Player2Score: return 0
		elif Player1Score > Player2Score: return 1
		elif Player1Score < Player2Score: return 2

	def Move(self,Infos,Team,AgentNo):
		self.NumCall = 0;
		#すでに移動不可とわかっている場合
		if (Infos[Team][AgentNo].CanAct == -1):
			return false;
		#座標外への移動の試行やとどまる手など、移動可能かどうかがすぐに確定する場合
		if(CanActionOne(Agents[Team][AgentNo].getPosition(),Infos[Team][AgentNo].Delta) == -1):
			return false
		elif(CanActionOne(Agents[Team][AgentNo].getPosition(),Infos[Team][AgentNo].Delta) == 1):
			return true

		#目標座標の重複や他エージェントの位置に移動しようとした場合などを判定
		for t in range(2):
			for a in range(2):
				#自分のエージェントとは比較しない
				if ((t == Team) and (a == AgentNo)):
					continue
				#他エージェントと目標座標が重複していた場合
				if ((Infos[Team][AgentNo].ExpectedPosition.x == Infos[t][a].ExpectedPosition.x)and(Infos[Team][AgentNo].ExpectedPosition.y == Infos[t][a].ExpectedPosition.y)):
					Infos[Team][AgentNo].CanAct = -1
					Infos[t][a].CanAct = -1
					return false

				#他エージェントの位置と目標座標が重複していた場合
				if ((Infos[Team][AgentNo].ExpectedPosition.x == Infos[t][a].NextPosition.x)and(Infos[Team][AgentNo].ExpectedPosition.y == Infos[t][a].NextPosition.y)):
					Infos[Team][AgentNo].CanAct = -1
					return false

				#他エージェントの現在の位置が目標座標と重複していた場合
				if ((Infos[Team][AgentNo].ExpectedPosition.x == Agents[t][a].GetPosition().x)and(Infos[Team][AgentNo].ExpectedPosition.y == Agents[t][a].GetPosition().y)):
				
					#自エージェントの現在の位置が目標座標と重複していた場合
					if ((Infos[t][a].ExpectedPosition.x == Agents[Team][AgentNo].GetPosition().x)and(Infos[t][a].ExpectedPosition.y == Agents[Team][AgentNo].GetPosition().y)):
						Infos[Team][AgentNo].CanAct = -1
						Infos[t][a].CanAct = -1
						return false

					#他エージェントが移動できる場合
					if (Move(Infos,t,a)):
						NumCall -=1
						Infos[Team][AgentNo].CanAct = 1;
						return true

					#他エージェントが移動できない場合
					Infos[Team][AgentNo].CanAct = -1;
					return false
		return true

	def CanActionAll(self, Intentions:list)->list:
		Infos = []
		Result = np.full((2,2), bool)
		for t in range(2):
			Infos.append([])
			for a in range(2):
				Infos[t].append(intention_info())
				Infos[t][a].Delta = copy.copy(Intentions[t][a])
				Infos[t][a].ExpectedPosition.x = self.Agents[t][a]._point[0] + Intentions[t][a].DeltaX
				Infos[t][a].ExpectedPosition.y = self.Agents[t][a]._point[1] + Intentions[t][a].DeltaY
				ExpectedPosState = self._Panels[Infos[t][a].ExpectedPosition.y][Infos[t][a].ExpectedPosition.x].getState();
				if (ExpectedPosState != t)and(ExpectedPosState != -1):
					Infos[t][a].NextPosition = copy.copy(self.Agents[t][a]._point)
				else:
					Infos[t][a].NextPosition = copy.copy(Infos[t][a].ExpectedPosition)
				Infos[t][a].CanAct = 0
		for t in range(2):
			for a in range(2):
				Result[t][a] = Move(Infos, t, a);

	def CanActionAll_ID(self, IntentionIDs:list)->list:
		return CanActionAll(self, [[intention(IntentionIDs[0][0]), intention(IntentionIDs[0][1])], [intention(IntentionIDs[1][0]), intention(IntentionIDs[1][1])]])

	def CanActionTeam(self, Intentions:list, TeamNo:int)->bool:
		if (self.CanActionOne(Intentions[0], TeamNo, 0) == -1)or(self.CanActionOne(Intentions[1], TeamNo, 1)):
			return False
		if sum(self.Agents[TeamNo][0].getPosition(), Intentions[0]) == sum(self.Agents[TeamNo][1].getPosition(), Intentions[1]):
			return False
		if (sum(self.Agents[TeamNo][0].getPosition(), Intentions[0]) == self.Agents[TeamNo][1].getPosition())and(sum(self.Agents[TeamNo][1].getPosition(), Intentions[1]) == self.Agents[TeamNo][0].getPosition()):
			return False
		return True

	def CanActionOne(self, Intention:intention, TeamNo:int, AgentNo:int)->int:
		if (Intention.DeltaX == 0)and(Intention.DeltaY == 0):
			return 1
		Pos = sum(self.Agents[TeamNo][AgentNo].getPosition(), Intention)
		if((0 <= Pos.x)and(Pos.x < self._XLen))and((0 <= Pos.y)and(Pos.y < self._YLen)):
			return 0
		else:
			return -1