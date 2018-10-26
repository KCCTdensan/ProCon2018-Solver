from .Game import *
#from .kerasDQN_ai import kerasDQNPlayer
import numpy as np
from .intention import *

class node():
	NumCallPlay = 10000
	NumTurns = 80

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
		self.__DQN = kerasDQNPlayer(1)

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
				if i == None:
					tmp.append(0)
					continue
				tmp.append(i.N)
			Ret.append(tmp)
		return Ret
			
	def Play(self)->float:
		Ret = 0
		if self.__EvalFlag:
			Ret = self.EvalateAndExpand()
		else:
			Ret = self.Select()
		self.Record += Ret
		self.N += 1
		self.Q = self.Record / N
		return Ret

	def Select(self)->float:
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

	def EvaluateAndExpand(self)->float:
		#Policy, Value = self.__DQN.evaluate(self.__Stage)
		for i in range(9):
			self.__Children.append([])
			if not(self.__Stage.CanActionOne(intention().from_action_id(i), 0, 0)):
				self.__Children[i].append(None)
				continue
			for j in range(9):
				if not(self.__Stage.CanActionTeam([intention().from_action_id(i),intention().from_action_id(j)], 0)):
					self.__Children[i].append(None)
					continue
				self.__Children[i].append(opponent_node(self, [intention().from_action_id(i),intention().from_action_id(j)], self.CntTurns + 1))
				self.__Children[i][j].Q = Policy[i][j]
				self.NumChildren += 1
		self.__EvalFlag = False
		return Value

	def ClearChildNode(self):
		self.__Children = []

	def ChildNode(self, IntentionIDs:list):
		return self.__Children[IntentionIDs[0]][IntentionIDs[1]]

	def NextNode(self, IntentionIDs:list):
		return self.ChildNode(IntentionIDs[0]).ChildNode(IntentionIDs[1])

	def GetStage(self):
		return self.__Stage

	def UCB1(self, Q:float, NChild:int):
		if NChild == 0:
			return None
		return Q + sqrt(2.0 * log(self.N) / NChild)

class opponent_node(node):
	def __init__(self, ParentNode:friend_node, IntentionIDs:list, CntTurns:int):
		super().__init__(CntTurns)
		self.__ParentNode = ParentNode
		self.__Children = []
		self.__FriendIDs = IntentionIDs
		self.Expand()

	def Play()->float:
		Ret = self.Select()
		self.Record += Ret
		self.N += 1
		self.Q = self.Record / N
		return Ret

	def Select(self)->float:	
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

	def Expand(self):
		for i in range(9):
			self.__Children.append([])
			if not(self.__ParentNode.GetStage().CanActionOne(intention().from_action_id(i), 1, 0)):
				self.__Children[i].append(None)
				continue
			for j in range(9):
				if not(self.__ParentNode.GetStage().CanActionAll([[self.__FriendIDs[0], self.__FriendIDs[1]], [intention().from_action_id(i),intention().from_action_id(j)]])):
					self.__Children[i].append(None)
					continue
				self.__Children[i].append(friend_node(self.ParentNode.GetStage(), self.CntTurns + 1))
				self.NumChildren += 1

	def ClearChildNode():
		ChildNode = []

	def UCB1(self, Q:float, NChild:int):
		if NChild == 0:
			return None
		return -Q + sqrt(2.0 * log(self.N) / NChild)

	def Result(self)->list:
		Ret = []
		for row in self.__Children:
			tmp = []
			for i in row:
				if i == None:
					tmp.append(0)
					continue
				tmp.append(i.N)
			Ret.append(tmp)
		return Ret

	def ChildNode(self, IntentionIDs:list)->friend_node:
		return self.__Children[IntentionIDs[0]][IntentionIDs[1]]