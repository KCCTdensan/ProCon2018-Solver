import numpy
from Panel import *
from Agent import *
from Game import *
from Node import *

class tree_search_ai:
	__init__(self,Stage)
	CurrentNode = friend_node(Stage)

def NumTurns(NumTurns:char):
	ChangeNumTurns(NumTurns);

def BestMove(IntentionIDs[NumTeams][stage.NumAgents]:action_id):
	for intentions in IntentionIDs:
		for i in intentinos:
			i = -1

	CurrentNode.Search(NumCallPlay);
	CurrentNode.Result(Result);
	Max = 0;
	for i in range(ID_MaxID):
		for i in range(ID_MaxID):
			if Max < Result[i][j]:
				Max = Result[i][j]
				IntentionIDs[Team_1P][0] = i
				IntentionIDs[Team_1P][1] = j

	Ret = Result[IntentionIDs[Team_1P][0]][IntentionIDs[Team_1P][1]]

	CurrentNode.ChildNode(IntentionIDs[Team_1P]).Search(NumCallPlay)
	CurrentNode.ChildNode(IntentionIDs[Team_1P]).Result(Result)
	Max = 0;
	for i in range(ID_MaxID):
		for j in range(ID_MaxID):
			if Max < Result[i][j]:
				Max = Result[i][j]
				IntentionIDs[Team_2P][0] = i
				IntentionIDs[Team_2P][1] = j
	return Ret;

def Move(IntentionIDs[NumTeams][stage::NumAgents]:action_id):
	CurrentNode = CurrentNode.UpdateCurrentNode(IntentionIDs)

def GetStage():
	return CurrentNode.GetStage()

def PrintStage():
	CurrentNode.PrintStage()
