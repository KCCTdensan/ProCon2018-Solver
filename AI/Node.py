from Game import *

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
	def ChangeNumTurns(self,NumTurns:char):
		pass
	def ChangeCntTurns(self,CntTurns :char):
		pass
	def IsLeafNode():
		return false

class friend_node:
	*Children[ID_MaxID][ID_MaxID] : opponent_node
	Stage :Game

	def __init__(self,Stage):
		pass
	def __init__(self,Stage,CntTurns:char):
		pass
	def Search(self,NumCallPlay:int):
		pass
	def Result(self,Result[ID_MaxID][ID_MaxID]):
		pass
	def ChildNode(IntentionID1,IntentionID2):
		pass
	def ChildNode(action_id[stage::NumAgents]):
		pass
	def UpdateCurrentNode(action_id(&SelectIntentionIDs)[NumTeams][stage::NumAgents]):
		pass
	def NextNode(action_id[NumTeams][stage::NumAgents]):
		pass
	def GetStage();
		pass
	def PrintStage():
		pass
	def PrintChildNodeInfo():
		pass


	def Play():
		pass
	def Selection():
		pass
	def Expansion():
		pass
	def Evaluation():
		pass
	def Rollout(NumTurn:int):
		pass
	def ClearChildNode():
		pass
	def UCB1(Q:float,NChild:int):
		pass

class opponent_node:

	friend_node:friend

	def Play():
		pass
	def Selection():
		pass
	def Expansion():
		pass
	def ClearChildNode():
		pass
	def UCB1(float Q, int NChild):
		pass

	def opponent_node(*ParentNode,Intentions[stage::NumAgents]:action_id,CntTurns:char)
		pass
	def Search(NumCallPlay:int):
		pass
	def Result(Result[ID_MaxID][ID_MaxID]:int[][]):
		pass
	def ChildNode(action_id IntentionID1, action_id IntentionID2):
		pass
	def ChildNode(action_id(&IntentionIDs)[stage::NumAgents]):
		pass

	def PrintChildNodeInfo():
		pass