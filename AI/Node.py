from Game import *
import numpy as np

class node:
	NumCallPlay = 100000
	Threshold = 100

	NumTurns = 0
	CntTurns = 0
	NumChildren = 0
	Q = 0.0
	N = 0
	Record = 0

	def __init__(self,CntTurns:char):
		pass
	def IsLeafNode():
		return false
	def ChangeNumTurns(NumTurns:int):
		pass
	def ChangeCntTurns(CntTurns :int):
		pass

class friend_node:
	Children = np.full((9,9),opponent_node())
	Stage :Game

	def __init__(self,ParentNode:opponent_node,Stage:Game,CntTurns:int):
		pass
	def __init__(self,Stage:Game):
		pass
	def Search(self,NumCallPlay:int):
		pass
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


	def Play():
		return 0
	def Selection():
		return 0
	def Expansion():
		pass
	def Evaluation():
		return 0
	def Rollout(NumTurn:int):
		return 0
	def ClearChildNode():
		pass
	def UCB1(Q:float,NChild:int):
		return 0,0

class opponent_node:

	friend_node:friend

	def Play():
		return 0
	def Selection():
		return 0;
	def Expansion():
		pass
	def ClearChildNode():
		pass
	def UCB1(Q:float,NChild:int):
		return 0.0

	def __init__(*ParentNode:friend_node,Intentions,CntTurns:int):
		pass
	def Search(NumCallPlay:):
		pass
	def Result():
		return np.zeros(9,9)
	def ChildNode(IntentionID1,IntentionID2):
		return np.full((9,9),friend_node())
	def ChildNode(IntentionIDs):
		return np.full((9,9),friend_node())

	def PrintChildNodeInfo():
		pass