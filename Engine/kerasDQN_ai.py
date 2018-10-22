import random
import os
import numpy as np
from .Player import Player
from .kerasDQN_model import(
    buildModel, train, Evaluate  
)
import tensorflow as tf
from keras.backend.tensorflow_backend import set_session

class kerasDQNPlayer(Player):
    def __init__(self, team):
        self._team = team
        self._model = buildModel()
        self._GAMMA = 0.01
        self._EPSILON = 0.3 
        self._GameImgLog = [] #盤面の記録保存先
        self._GameIntentionLog = [] #行動の記録保存先
        self._maxQs = []

        #GPU使用率決定
        self._config = tf.ConfigProto()
        self._config.gpu_options.per_process_gpu_memory_fraction = 0.6 #freememory/totalmemory
        set_session(tf.Session(config=self._config))

    def intention(self, Game):#盤面の情報を渡してAgentの動かし方を返す
        intentions = self.searchIntentions(Game) #可能な行動を全て探す
        GameImg = self.getGameImg(Game) #盤面を画像データに
        goodIntention = np.zeros((2, 3), int) 

        #評価値が一番高い行動を選択
        maxEvalue = -1
        for intention in intentions: 
            Evalue = Evaluate(self._model, GameImg, intention) #行動の評価値計算
            if(maxEvalue < Evalue):
                maxEvalue = Evalue
                goodIntention = intention

        if(random.random() < self._EPSILON):
            #ランダムに行動を選択
            goodIntention = intentions[random.randint(0,len(intentions)-1)]

        self._GameImgLog.append(GameImg) #盤面と行動を記録
        self._GameIntentionLog.append(goodIntention)
        self._maxQs.append(maxEvalue)
        return goodIntention

    def searchIntentions(self, Game): #可能な行動を全て探す
        intentions = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                intentions.append([i,j,0])
                intentions.append([i,j,1])

        pairintentions = []
        for i in intentions:
            for j in intentions:
                pairintentions.append([i, j])
        return pairintentions

        for pairintention in pairintentions:
            Game.canAction(pairintention[0], self._team-1)
            Game.canAction(pairintention[1], self._team)
        return intentions

    def getGameImg(self, Game): #盤面を画像に
        GameImg = np.zeros((12, 12, 2), int)
        Panels = Game.getPanels()
        for i in range(len(Panels)):
            for j in range(len(Panels[0])):
                Panel = Panels[i][j]
                GameImg[i][j][0] = Panel.getScore()
                if(Panel.getState()== 0):pass
                elif(Panel.getState() == self._team):
                    GameImg[i][j][1] = 1
                elif(Panel.getState() != self._team):
                    GameImg[i][j][1] = 3
                if((Panel.getSurrounded()==[True, False]) | (Panel.getSurrounded()==[False, True])):
                    GameImg[i][j][1] += 1
        return GameImg

    def getAllReward(self, reward):#総報酬の計算
        #報酬rのリストを作成
        turn = len(self._GameImgLog)
        rs = np.zeros(turn)
        rs[len(rs)-1] = reward

        Rs = np.hstack(rs.reshape([-1,1])).astype(float)
        for i in range(turn-1):
            Rs[i] = self._GAMMA * (rs[i] + self._maxQs[i+1] - self._maxQs[i])
        Rs[turn-1] = reward
        return Rs.reshape([-1,1])

    def learn(self, reward, train_x1=None, train_x2=None, train_y=None):#対戦データを学習
        xImgs = np.array(self._GameImgLog).reshape([-1,12,12,2])
        xIntentions = np.array(self._GameIntentionLog).reshape([-1,2,3])
        yRs = self.getAllReward(reward)

        if((train_x1!=None)&(train_x2!=None)&(train_y!=None)):
            xImgs = np.array(train_x1).reshape([-1,12,12,2])
            xIntentions = np.array(train_x2).reshape([-1,2,3])
            yRs = np.array(train_y).reshape([-1,1])

        self._model.compile(
            loss="mean_squared_error",
            optimizer="adam"
            )
        if(os.path.isfile("./checkpoint/model_params")):
            model.load_weights("./checkpoint/model_params")

        train(
            self._model,
            #train_data 
            xImgs, 
            xIntentions,
            yRs,
            #val_data
            xImgs, 
            xIntentions,
            yRs,
            100,
            )

    def outputLog(self, reword):#行動の記録を残す
        pass