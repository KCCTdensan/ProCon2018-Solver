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
		self.Record = 0.0

	def ChangeCntTurns(self, CntTurns:int):
		self.CntTurns = CntTurns


class friend_node(node):
	def __init__(self, Stage):
		super().__init__(0)
		self.__Stage = Stage
		self.__Children = []
		self.__EvalFlag = True

	def __init__(self, Stage, CntTurns:int):
		super().__init__(CntTurns)
		self.__Stage = Stage
		self.__Children = []
		self.__EvalFlag = True
	
	def Search(self, NumCallPlay:int):
		if self.__EvalFlag:
			self.EvaluateAndExpand()
		for i in range(NumCallPlay):
			self.Select()

	def Result(self):
		Ret = []
		for row in self.__Children:
			tmp = []
			for i in row:
				tmp.append(i.N)
			Ret.append(tmp)
		return Ret
			
	def Play()->float:
		Ret = 0
		if self.__EvalFlag:
			Ret = self.EvalateAndExpand()
		else:
			Ret = self.Select()
		self.Record += Ret
		self.N += 1
		return Ret

	def Select()->float:
		Q_Max = -10.0
		SelectedNode = None
		for row in self.__Children:
			for i in row:
				if i == None:
					continue
				Q_C = self.UCB1(i.Q, i.N)
				if Q_C == None:
					return i.Play()
				if Q_C > Q_Max:
					SelectedNode = i
		if SelectedNode == None:
			self.Q = -1.0
			return -1.0
		return SelectedNode.Play()

	def EvaluateAndExpand()->float:
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
		self.__EvalFlag = False

	def ClearChildNode():
		self.__Children = []

	def ChildNode(IntentionIDs:list)->opponent_node:
		return self.__Children[IntentionIDs[0]][IntentionIDs[1]]

	def NextNode(IntentionIDs:list)->friend_node:
		return self.ChildNode(IntentionIDs[0]).ChildNode(IntentionIDs[1])

	def GetStage():
		return self.__Stage

	def UCB1(Q:float, NChild:int):
		pass

class opponent_node(node):
	def __init__(self, ParentNode:friend_node, IntentionIDs:list, CntTurns:int):
		super().__init__(CntTurns)
		self.__ParentNode = ParentNode
		self.__FriendIDs = IntentionIDs
		self.Expand()

	def Play()->float:
		Ret = self.Select()
		self.N += 1
		self.Record += Ret
		return Ret

	def Select()->float:	
		Q_Max = -10.0
		SelectedNode = None
		for row in self.__Children:
			for i in row:
				if i == None:
					continue
				Q_C = self.UCB1(i.Q, i.N)
				if Q_C == None:
					return i.Play()
				if Q_C > Q_Max:
					SelectedNode = i
		if SelectedNode == None:
			self.Q = -1.0
			return -1.0
		return SelectedNode.Play()

	def Expand():
		for i in range(9):
			self.__Children.append([])
			if not(self.Stage.CanAction(i, 0, 0)):
				self.__Children[i].append(None)
				continue
			for j in range(9):
				if not(self.Stage.CanAction(((i, j), (i, j)), 0)):
					self.__Children[i].append(None)
					continue
				self.__Children[i].append(friend_node(self.ParentNode.GetStage(), self.CntTurns + 1))
				self.NumChildren += 1
		self.__EvalFlag = False

	def ClearChildNode():
		ChildNode = []

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