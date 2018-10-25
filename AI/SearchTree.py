import numpy
from Panel import *
from Agent import *
from Game import *

class tree_search_ai:
	__init__(self,stage &Stage)
	CurrentNode = new friend_node(Stage);

tree_search_ai::~tree_search_ai()
{
	delete CurrentNode;
	CurrentNode = nullptr;
}

void tree_search_ai::NumTurns(unsigned char NumTurns)
{
	node::ChangeNumTurns(NumTurns);
}

int tree_search_ai::BestMove(action_id(&IntentionIDs)[NumTeams][stage::NumAgents])
{
	int Result[ID_MaxID][ID_MaxID];
	int Ret;

	for(team_no t = 0; t < NumTeams; ++t)
	{
		for(char a = 0; a < stage::NumAgents; ++a)
		{
			IntentionIDs[t][a] = -1;
		}
	}

	CurrentNode->Search(node::NumCallPlay);
	CurrentNode->Result(Result);
	int Max = 0;
	for (action_id i = 0; i < ID_MaxID; ++i)
	{
		for (action_id j = 0; j < ID_MaxID; ++j)
		{
			if (Max < Result[i][j])
			{
				Max = Result[i][j];
				IntentionIDs[Team_1P][0] = i;
				IntentionIDs[Team_1P][1] = j;
			}
		}
	}
	/*if(IntentionIDs[Team_1P][0] == -1)
	{
		IntentionIDs[Team_1P][0] = ID_Stay;
		IntentionIDs[Team_1P][1] = ID_Stay;
	}*/

	Ret = Result[IntentionIDs[Team_1P][0]][IntentionIDs[Team_1P][1]];

	CurrentNode->ChildNode(IntentionIDs[Team_1P])->Search(node::NumCallPlay);
	CurrentNode->ChildNode(IntentionIDs[Team_1P])->Result(Result);
	Max = 0;
	for (action_id i = 0; i < ID_MaxID; ++i)
	{
		for (action_id j = 0; j < ID_MaxID; ++j)
		{
			if (Max < Result[i][j])
			{
				Max = Result[i][j];
				IntentionIDs[Team_2P][0] = i;
				IntentionIDs[Team_2P][1] = j;
			}
		}
	}
	/*if(IntentionIDs[Team_2P][0] == -1)
	{
		IntentionIDs[Team_2P][0] = ID_Stay;
		IntentionIDs[Team_2P][1] = ID_Stay;
	}*/

	return Ret;
}

void tree_search_ai::Move(action_id(&IntentionIDs)[NumTeams][stage::NumAgents])
{
	CurrentNode = CurrentNode->UpdateCurrentNode(IntentionIDs);
}

const stage& tree_search_ai::GetStage()const
{
	return CurrentNode->GetStage();
}

void tree_search_ai::PrintStage()const
{
	CurrentNode->PrintStage();
}
