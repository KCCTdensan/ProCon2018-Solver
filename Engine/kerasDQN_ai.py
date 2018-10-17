import random
import numpy as np
from .Player import Player
from .kerasDQN_model import(
    buildModel, train, Evaluate  
)

class kerasDQNPlayer(Player):
    def __init__(self, team):
        self._team = team
        self._model = buildModel()
        self._GAMMA = 0.01
        self._EPSILON = 0.3
        self._GameImgLog = [] #盤面の記録保存先
        self._GameIntentionLog = [] #行動の記録保存先

    def intention(self, Game):#盤面の情報を渡してAgentの動かし方を返す
        intentions = searchIntentions(Game) #可能な行動を全て探す
        GameImg = getGameImg(Game) #盤面を画像データに
        goodIntention = np.zeros((2, 3), int) 

        if(random.random() < self._EPSILON):
            #ランダムに行動を選択
            goodIntention = intentions[random.randint(0,len(intentions))]
        else:
            #評価値が一番高い行動を選択
            maxEvalue = -1
            for intention in intentions: 
                Evalue = Evaluate(self._model, GameImg, intention) #行動の評価値計算
                if(maxEvalue < Evalue):
                    maxEvalue = Evalue
                    goodIntention = intention

        self._GameImgLog += GameImg #盤面と行動を記録
        self._GameIntentionLog += goodIntention
        return goodIntention

    def searchIntention(self, Game): #可能な行動を全て探す
        intentions = []
        for i in range(-1, 1):
            for j in range(-1, 1):
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

    def getGameImg(Game): #盤面を画像に
        GameImg = np.zeros((12, 12, 2), int)
        Panels = Game.getPanels()
        for i in range(len(Panels)):
            for j in range(len(Panels[0])):
                Panel = Panels[i][j]
                GameImg[i][j][0] = Panel.getScore()
                if(Panel.getState() != 0):
                    GameImg[i][j][1] = Panel.getState()*Panel.getSurrounded()[Panel.getstate()-1]
        return GameImg

    def learn(self, reword):#対戦データを学習
        Qs = [reword]
        for i in range(len(self._GameImgLog)-1):
            Q.insert(0, self._GAMMA*Q[i])

        model = buildModel()
        model.compile(
            loss="mean_squared_error",
            optimizer="adam"
            )
        if(os.path.isfile("./checkpoint/model_params")):
            model.load_weights("./checkpoint/model_params")
        model.summary()

        train(
            model,
            self._GameImgLog,
            self._GameIntentionLog,
            self._GameImgLog[0],
            self._GameIntentionLog[0],
            Qs,
            10000,
            )

    def outputLog(self, reword):#行動の記録を残す
        pass