import random
import os
import numpy as np
from .Player import Player

class NomalSearch(Player):
    def __init__(self, team):
        self._team = team
        if(self._team==1):self._enemyteam = 2
        elif(self._team==2):self._enemyteam = 1

        #if(os.path.isfile("./checkpoint/model_params")):
        #    model.load_weights("./checkpoint/model_params")

    def intention(self, Game):#�Ֆʂ̏���n����Agent�̓���������Ԃ�
        #GameImg = self.getGameImg(Game) #�Ֆʂ��摜�f�[�^��
        Agents = Game.getAgents()
        myAgentsPoint = [Agents[team*2-2].getPoint(), Agents[team*2-1].getPoint()]

        #�]���l����ԍ����s����I��
        maxEvalue = -1
        Agent1ActionID = 0
        Agent2ActionID = 0
        #Policies, Evalues = predict(self._model, GameImg).reshape(9, 9) #�s���̕]���l�v�Z
		
        for i in range(len(Policies)):
            for j in range(len(Policies[0])):
                if Policies[i][j] > maxEvalue:
                    Agent1ActionID = j
                    Agent2ActionID = i

        goodIntention = []
        IntentionVectors = [actionIDtoVector(Agent1ActionID), actionIDtoVector(Agent2ActionID)]
        for i in range(2):
            x = myAgentsPoint[i][0]+IntentionVectors[i][0]
            y = myAgentsPoint[i][1]+IntentionVectors[i][1]
            if(Game.getPanels()[x][y].getState()==self._enemyteam):
                goodIntention.append(IntentionsVector[i].append(1))
            else:
                goodIntention.append(IntentionsVector[i].append(0))
        return goodIntention

    def getGameImg(self, Game): #�Ֆʂ��摜��
        GameImg = np.zeros((10, 12, 12), int)
        Panels = Game.getPanels()
        Agents = Game.getAgents()
        xlen = len(Panels[0])
        ylen = len(Panels)

        """
        [0]�p�l���̗L��
        [1]�p�l���̃|�C���g
        [2]�����G�[�W�F���g1�̗L��
        [3]�����G�[�W�F���g2�̗L��
        [4]�����p�l���̗L��
        [5]�����p�l���Ɉ͂܂ꂽ�̈�
        [6]����G�[�W�F���g1�̗L��
        [7]����G�[�W�F���g2�̗L��
        [8]����p�l���̗L��
        [9]����p�l���Ɉ͂܂ꂽ�̈�
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

    def actionIDtoVector(Value):
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

    def learn(self, train_x, train_y1, train_y2, val_x, val_y1, val_y2):#�ΐ�f�[�^���w�K
        
        train(
            self._model,
            #train_data 
            train_x, 
            train_y1,
            train_y2,
            #val_data
            val_x, 
            val_y1,
            val_y2,
            50000,
            )

    def evaluate(self, Game):
        return predict(self._model, self.getGameImg(Game))