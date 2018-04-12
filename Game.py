from Panel import *
from Agent import *
from Window import *
import random as Ran
import numpy as Np
import math

class Game:
	_turn: int #最終ターン数
	_1Pscore: int #1Pの得点
	_2Pscore: int #2Pの得点
	_Panels: list#ステージを構成するパネルのリスト(numpy定義)
	_Agents: list #ステージに存在するエージェントのリスト

	def __init__(self): #ステージ生成
		_turn = Ran.randint(60,120)
		_xLen = Ran.randint(3,12)
		_yLen = Ran.randint(3,12)
		_Panels = Np.zeros(_yLen,_xLen)
		for x in range(math.ceil(_xLen/2)):
			for y in range(math.ceil(_yLen/2)):
				_Panels[y,x] = Ran.randint(-5,5)
				_Panels[_yLen - y,x] = _Panels[y,x]
				_Panels[y,_xLen - x] = _Panels[y,x]
				_Panels[_yLen - y,_xLen - x] = _Panels[y,x]
		Agentx = Ran.randint(0,math.floor(_yLen/2))
		Agenty = Ran.randint(0,math.floor(_xLen/2))
		_Panels[Agenty,Agentx] = 0
		_Panels[_yLen - Agenty,Agentx] = 0
		_Panels[Agenty,_xLen - Agentx] = 0
		_Panels[_yLen - Agenty,_xLen - Agentx] = 0


	def new(): #コンストラクタ呼び出し
		return Game()

	def score(self): #得点計算
		pass

	def main(self):
		#エージェント(4人)の意思([int, int])を保存する変数のリスト
		for turn in range(_turn):
			#Windowからエージェントの移動orパネル操作の意思を入力
			#移動orパネル操作
			self.score() #得点計算
			#盤面の情報をWindowに渡す
