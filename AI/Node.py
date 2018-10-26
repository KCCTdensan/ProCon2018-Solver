from ..Game import *
import numpy as np

class node:
	NumCallPlay = 10000
	NumTurns = 0

	def __init__(self, CntTurns:int):
		self.CntTurns = CntTurns
		self.NumChildren = 0
		self.Q = 0.0
		self.N = 0
		self.Record = 0

	def ChangeNumTurns(self, NumTurns:int):
		pass
	def ChangeCntTurns(self, CntTurns:int):
		pass
	def IsLeafNode():
		return false

class friend_node(node):
	def __init__(self, Stage):
		self.__Stage = Stage
		self.__Children = []
		super.__CntTurns = 0

	def __init__(self, Stage, CntTurns:int):
		self.__Stage = Stage
		self.__Children = []
		super.CntTurns = CntTurns
	
	def Play():
		pass

	def Selection():
		pass

	def Expansion():
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
	def __init__(self, ParentNode:friend_node, IntentionIDs:int, CntTurns:int):
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

	def PrintChildNodeInfo():
		pass