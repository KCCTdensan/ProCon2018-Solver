#from Game import *

class Player():#人，AIの継承用クラス
	def __init__(self):
		self._Intention = [[0, 0, 0], [0, 0, 0]] #2つのエージェントの動かし方

	def intention(self,Game):#盤面の情報を渡してAgentの動かし方を返す
		return self._Intention

	def getResult(self):#試合結果を渡す(学習に使う?)
		return