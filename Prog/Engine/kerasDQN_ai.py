import random
import os
import numpy as np
from .Player import Player
from keras.models import load_model
from .kerasDQN_model import(
	buildModel, train, predict  
)

class kerasDQNPlayer(Player):
	def __init__(self, team):
		self._team = team
		if(self._team==1):self._enemyteam = 2
		elif(self._team==2):self._enemyteam = 1
		self._model = buildModel()

        #if(os.path.isfile("./checkpoint/model_.h5")):
            #self._model.load_weights("./checkpoint/model_.h5")
        
    def intention(self, Game):#盤面の情報を渡してAgentの動かし方を返す
        GameImg = self.getGameImg(Game) #盤面を画像データに
        Agents = Game.getAgents()
        myAgentsPoint = [Agents[self._team*2-2].getPoint(), Agents[self._team*2-1].getPoint()]

        #評価値が一番高い行動を選択
        maxEvalue = -1
        Agent1ActionID = 0
        Agent2ActionID = 0
        Policies, Evalues = predict(self._model, GameImg)
        Policies = np.reshape(Policies, (9, 9))#行動の評価値計算
        for i in range(len(Policies)):
            for j in range(len(Policies[0])):
                if Policies[i][j] > maxEvalue:
                    maxEvalue = Policies[i][j]
                    Agent1ActionID = j
                    Agent2ActionID = i
        print(Agent1ActionID, Agent2ActionID)
        goodIntention = []
        IntentionVectors = [self.actionIDtoVector(Agent1ActionID), self.actionIDtoVector(Agent2ActionID)]
        for i in range(2):
            intentions_mv = np.zeros((4, 3), int)
            intentions_rm = np.zeros((4, 3), int)
            intentions_mv[self._team*2-2+i]=IntentionVectors[i] + [0]
            intentions_rm[self._team*2-2+i]=IntentionVectors[i] + [0]
            if(Game.canAction(intentions_mv, self._team*2-2+i)):goodIntention.append(IntentionVectors[i] + [0])
            elif(Game.canAction(intentions_rm, self._team*2-2+i)):goodIntention.append(IntentionVectors[i] + [1])
            else:goodIntention.append([0,0,0])
              
	def getGameImg(self, Game): #盤面を画像に
		GameImg = np.zeros((10, 12, 12), int)
		Panels = Game.getPanels()
		Agents = Game.getAgents()
		xlen = len(Panels[0])
		ylen = len(Panels)

		"""
		[0]パネルの有無
		[1]パネルのポイント
		[2]味方エージェント1の有無
		[3]味方エージェント2の有無
		[4]味方パネルの有無
		[5]味方パネルに囲まれた領域
		[6]相手エージェント1の有無
		[7]相手エージェント2の有無
		[8]相手パネルの有無
		[9]相手パネルに囲まれた領域
		"""
		for i in range(len(Panels)):
			for j in range(len(Panels[0])):
				GameImg[0][i][j] = 1
				GameImg[1][i][j] = Panels[i][j].getScore() 
				if(Panels[i][j].getState()==self._team):GameImg[4][i][j] = 1 
				elif(Panels[i][j].getState()==self._enemyteam):GameImg[8][i][j] = 1
				if(Panels[i][j].getSurrounded()[self._team -1]):GameImg[5][i][j] = 1
				if(Panels[i][j].getSurrounded()[self._enemyteam -1]):GameImg[9][i][j] = 1
		for i in range(len(Agents)):
			point = Agents[i].getPoint()
			if(Agents[i].getTeam()==self._team):
				GameImg[2+i%2][point[0]][point[1]]=1
			elif(Agents[i].getTeam()==self._enemyteam):
				GameImg[6+i%2][point[0]][point[1]]=1
		return GameImg

	def actionIDtoVector(self, Value):
		if Value == 1:
			return [-1, -1]
		if Value == 2:
			return [0, -1]
		if Value == 3:
			return [1, -1]
		if Value == 4:
			return [-1, 0]
		if Value == 5:
			return [1, 0]
		if Value == 6:
			return [-1, 1]
		if Value == 7:
			return [0, 1]
		if Value == 8:
			return [1, 1]
		return [0, 0]

    def actionIDtoVector(self, Value):
        if Value == 1:
            return [-1, -1]
        if Value == 2:
            return [0, -1]
        if Value == 3:
            return [1, -1]
        if Value == 4:
            return [-1, 0]
        if Value == 5:
            return [1, 0]
        if Value == 6:
            return [-1, 1]
        if Value == 7:
            return [0, 1]
        if Value == 8:
            return [1, 1]
        return [0, 0]

	def evaluate(self, Game):
		return predict(self._model, self.getGameImg(Game))