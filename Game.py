from Panel import *
from Agent import *
from Window import *

class Game:
	_turn: int #最終ターン数
	_1Pscore: int #1Pの得点
	_2Pscore: int #2Pの得点
	_Panels: list #ステージを構成するパネルのリスト
	_Agents: list #ステージに存在するエージェントのリスト

	def __init__(self): #ステージ生成
		pass

	def new(): #コンストラクタ呼び出し
		return Game()

	def score(self): #得点計算
		pass

	def main(self):
		#for turn in _turn:
			#Windowからエージェントの移動orパネル操作の意思を入力
			#移動orパネル操作
			#得点計算
			#盤面の情報をWindowに渡す
		pass
