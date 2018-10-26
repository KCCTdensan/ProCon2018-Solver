from .Player import Player
from .Node import friend_node

class KA_31(Player):#人，AIの継承用クラス
	def __init__(self):
		self.__Intention = [[0, 0, 0], [0, 0, 0]] #2つのエージェントの動かし方

	def __ActionIDToIntention(self, Value:int)->list:
		if Value == 1:
			return [-1, -1, 0]
		if Value == 2:
			return [0, -1, 0]
		if Value == 3:
			return [1, -1, 0]
		if Value == 4:
			return [-1, 0, 0]
		if Value == 5:
			return [1, 0, 0]
		if Value == 6:
			return [-1, 1, 0]
		if Value == 7:
			return [0, 1, 0]
		if Value == 8:
			return [1, 1, 0]
		return [0, 0, 0]

	def intention(self, Game)->list:#盤面の情報を渡してAgentの動かし方を返す
		CurrentNode = friend_node(Game, 0)
		CurrentNode.Search(1000)
		Result = CurrentNode.Result()
		Selected_i = 0
		Selected_j = 0
		for i in range(len(Result)):
			for j in range(len(Result[0])):
				if (Result[Selected_i] < Result[i])and(Result[Selected_j] < Result[j]):
					Selected_i = i
					Selected_j = j
		self.__Intention = [self.__ActionIDToIntention(i), self.__ActionIDToIntention(j)]
		return self.__Intention