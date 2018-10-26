from ..Game import *
import numpy as np

class node():
	NumCallPlay = 10000
	NumTurns = 0

	def __init__(self, CntTurns:int):
		self.CntTurns = CntTurns
		self.NumChildren = 0
		self.Q = 0.0
		self.N = 0
		self.Record = 0

	def ChangeCntTurns(self, CntTurns:int):
		self.CntTurns = CntTurns

	def IsLeafNode():
		return self.NumChildren == 0

class friend_node(node):
	def __init__(self, Stage):
		super().__init__(CntTurns)
		self.__Stage = Stage
		self.__Children = []
		self.EvalFlag = True

	def __init__(self, Stage, CntTurns:int):
		super().__init__(CntTurns)
		self.__Stage = Stage
		self.__Children = []
		self.__EvalFlag = True
	
	def Play()->int:
		Ret = 0
		if selif.__EvalFlag:
			Ret = self.Evalation()
		else:
			if self.IsLeafNode():
				self.Expansion()
			Ret = self.Selection()


		return Ret

	def Selection()->int:
		Q_Max = -10.0
		SelectedNode = None
		for i in self.__Children:
			for j in i:
				if j == None:
					continue
				Q_C = self.UCB1(j.Q, j.N)
				if Q_C == None:
					return j.Play()
				if Q_C > Q_Max:
					SelectedNode = j
		if SelectedNode == None:
			self.Q = -1.0
			return -1
		return SelectedNode.Play()

	def Expansion():
		for i in range(9):
			self.__Children.append([])
			if not(self.Stage.CanAction(i, 0, 0)):
				self.__Children[i].append(None)
				continue
			for j in range(9):
				if not(self.Stage.CanAction((i, j), 0)):
					self.__Children[i].append(None)
					continue
				self.__Children[i].append(opponent_node(self, [i, j], self.CntTurns + 1))
				self.NumChildren += 1

	def Result(self):
		return np.zeros(9,9)
	def ChildNode(IntentionID1,IntentionID2):
		return np.full((9,9),opponent_node())
	def ChildNode(SelectIntentionIDs):
		return (9,9),opponent_node()
	def UpdateCurrentNode(SelectIntentionIDs):
		return np.full((9,9),friend_node())
	def NextNode():
		return np.full((9,9),friend_node())
	def GetStage():
		Stage

	def PrintStage():
		pass
	def PrintChildNodeInfo():
		pass

	def Evaluation():
		pass

	def ClearChildNode():
		pass

	def UCB1(Q:float, NChild:int):
		pass

	def Search(self, NumCallPlay:int):
		pass

	def Result(self)->list:
		pass

	def ChildNode(IntentionID1, IntentionID2):
		pass

	def ChildNode(IntentionIDs:list):
		pass

	def UpdateCurrentNode(SelectIntentionIDs:list):
		pass

	def NextNode(SelectIntentionIDs:list):
		pass

	def GetStage():
		pass

	def PrintStage():
		pass

	def PrintChildNodeInfo():
		pass

class opponent_node(node):
	def __init__(self, ParentNode:friend_node, IntentionIDs:list, CntTurns:int):
		pass

	def Play():
		pass

	def Selection():
		pass

	def Expansion():
		pass

	def ClearChildNode():
		pass

	def UCB1(Q:float, NChild:int):
		pass

	def Search(NumCallPlay:int):
		pass

	def Result()->list:
		pass

	def ChildNode(IntentionID1:int, IntentionID2:int)->friend_node:
		pass

	def ChildNode(IntentionIDs:list)->friend_node:
		pass
	def Result():
		return np.zeros(9,9)
	def ChildNode(IntentionID1,IntentionID2):
		return np.full((9,9),friend_node())
	def ChildNode(IntentionIDs):
		return np.full((9,9),friend_node())

	def PrintChildNodeInfo():
		pass