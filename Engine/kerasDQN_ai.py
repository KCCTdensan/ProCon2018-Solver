from Player import Player
from kerasDQN_model import(
    buildModel, train, Evaluate  
)

class kerasDQNPlayer(Player):
    def __init__(self):
        self.GameLog = [] #行動の記録保存先

    def intention(self, Game):#盤面の情報を渡してAgentの動かし方を返す
        self.intentions = searchIntentions(Game) #可能な行動を探す
        self.GameImg = getGameImg(Game) #盤面を画像データに

        self.maxEvalue = 0
        for intention in self.intentions: #評価値が一番高い行動を選択
            self.Q = Evaluate(self.GameImg, intention) #行動の評価値計算
            if self.maxEvalue < self.Q:
                self.maxEvalue = self.Q
                self._Intention = intention
        return self._Intention

    def searchIntention(Game): #可能な行動を探す
        intensions = []
        return intentions

    def getGameImg(self, Game): #盤面を画像に
        GameImg = []
        return GameImg

    def getResult(self):#行動の記録を残す
        pass