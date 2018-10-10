from Player import Player
from kerasDQN_model import(
    buildModel, train, Evaluate  
)

class kerasDQNPlayer(Player):
    def __init__(self):
        self._model = buildModel()
        self._GameLog = [] #行動の記録保存先

    def intention(self, Game):#盤面の情報を渡してAgentの動かし方を返す
        self._intentions = searchIntentions(Game) #可能な行動を全て探す
        self._GameImg = getGameImg(Game) #盤面を画像データに

        self._maxEvalue = 0
        for intention in self._intentions: #評価値が一番高い行動を選択
            self.Q = Evaluate(self._model, self._GameImg, intention) #行動の評価値計算
            if self._maxEvalue < self.Q:
                self._maxEvalue = self.Q
                self._Intention = intention
        self._GameLog += [self._GameImg, self._Intention] #盤面と行動を記録
        return self._Intention

    def searchIntention(Game): #可能な行動を全て探す
        intensions = []
        return intentions

    def getGameImg(self, Game): #盤面を画像に
        GameImg = []
        return GameImg

    def getResult(self):#行動の記録を残す
        pass