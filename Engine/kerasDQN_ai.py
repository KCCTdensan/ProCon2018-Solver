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

        #GPU使用率決定
        self._config = tf.ConfigProto()
        self._config.gpu_options.per_process_gpu_memory_fraction = 0.6 #freememory/totalmemory
        set_session(tf.Session(config=self._config))

    def intention(self, Game):#盤面の情報を渡してAgentの動かし方を返す
        GameImg = self.getGameImg(Game) #盤面を画像データに

        #評価値が一番高い行動を選択
        maxEvalue = -1
        Agent1Intention = 0
        Agent2Intention = 0
        print(Evaluate(self._model, GameImg)) 
        Evalues = Evaluate(self._model, GameImg).reshape(9, 9) #行動の評価値計算
        for i in Evalues:
            for j in Evalues[0]:
                if Evalues[i][j] > maxEvalue:
                    Agent1Intention = i
                    Agent2Intention = j

        return goodIntention

    def getGameImg(self, Game): #盤面を画像に
        GameImg = np.random.rand(10, 12, 12)
        print(GameImg)
        Panels = Game.getPanels()
        return GameImg

    def learn(self, train_x, train_y, val_x, val_y):#対戦データを学習
        self._model.compile(
            loss="mean_squared_error",
            optimizer="adam"
            )
        #if(os.path.isfile("./checkpoint/model_params")):
        #    model.load_weights("./checkpoint/model_params")

        train(
            self._model,
            #train_data 
            train_x, 
            train_y,
            #val_data
            val_x, 
            val_y,
            1000,
            )
