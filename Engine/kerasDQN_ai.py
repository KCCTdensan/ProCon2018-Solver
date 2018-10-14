import random
import numpy as np
from Player import Player
from kerasDQN_model import(
    buildModel, train, Evaluate  
)

class kerasDQNPlayer(Player):
    def __init__(self):
        self._model = buildModel()
        self._GAMMA = 0.01
        self._EPSILON = 0.3
        self._GameImgLog = [] #盤面の記録保存先
        self._GameIntentionLog = [] #行動の記録保存先

    def intention(self, Game):#盤面の情報を渡してAgentの動かし方を返す
        self._intentions = searchIntentions(Game) #可能な行動を全て探す
        self._GameImg = getGameImg(Game) #盤面を画像データに
        self._Intention = [[0, 0, 0],[0 ,0 ,0]]

        if(random.random() < self._EPSILON):
            #ランダムに行動を選択
            self._Intention = self._intentions[random.randint(0,len(self._intentions))]
        else:
            #評価値が一番高い行動を選択
            self._maxEvalue = -1
            for intention in self._intentions: 
                self.Evalue = Evaluate(self._model, self._GameImg, intention) #行動の評価値計算
                if(self._maxEvalue < self.Evalue):
                    self._maxEvalue = self.Evalue
                    self._Intention = intention

        self._GameImgLog += self._GameImg #盤面と行動を記録
        self._GameIntentionLog += self._Intention
        return self._Intention

    def searchIntention(Game): #可能な行動を全て探す
        intensions = []
        return intentions

    def getGameImg(self, Game): #盤面を画像に
        GameImg = np.zeros((14, 14, 2))
        Panels = Game.getPanels()
        for i in range(len(Panels)):
            for j in range(len(Panels[0])):
                Panel = Panels[i][j]
                GameImg[i][j][0] = Panel.getScore()
                if(Panel.getstate != 0):
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