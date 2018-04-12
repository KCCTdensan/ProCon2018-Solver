from Panel import *
from Agent import *
from Window import *

class Game:
	_turn: int #最終ターン数
	_1Pscore: int #1Pの得点
	_2Pscore: int #2Pの得点
	_Panels: list #ステージを構成するパネルのリスト
	_1PAgents: list
	_2PAgents: list #ステージに存在する2Pのエージェントのリスト
	_1PIntention: [[int, int]]*2
	_2PIntention: [[int, int]]*2 #エージェント(4人)の意思([int, int])を保存する変数のリスト

	def __init__(self): #ステージ生成
		pass

	def new(): #コンストラクタ呼び出し
		return Game()

	def score(self): #得点計算
		pass

	def action(self): #エージェントの意思をみて，実際に移動orパネル操作
		pass

	def main(self):
		for turn in range(_turn):
			#Windowからエージェントの移動orパネル操作の意思を入力
			self.action() #エージェントの意思をみて，実際に移動orパネル操作
			self.score() #得点計算
			#盤面の情報をWindowに渡す