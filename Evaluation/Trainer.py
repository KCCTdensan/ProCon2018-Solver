import random as rand
import numpy as np
from EvaluationNetwork import EvaluationNetwork
from EvaluationNetwork import NetworkParamData
from Game import Game

class NetworkInfo:
	def __init__(self, Network:EvaluationNetwork):
		self.Network = Network
		self.NumVictory = 0
		self.NumDefeat = 0

	def Win(self):
		self.NumVictory += 1

	def Lose(self):
		self.NumDefeat += 1

class Trainer():
	NumChildren = 100
	Networks = []

	def __RandomCrossParam(Param1:NetworkParamData, Param2:NetworkParamData)->NetworkParamData:
		NewParam = NetworkParamData()
		for i in range(len(Param1.HiddenLayerParams)):
			NewParam.HiddenLayerParams.append([])
			for j in range(2):
				Rate1 = rand.randint(0, 100) / 100.0
				Rate2 = 1.0 - Rate1
				NewValue = Param1.HiddenLayerParams[i][j] * Rate1 + Param2.HiddenLayerParams[i][j] * Rate2
				NewParam.HiddenLayerParams[i].append(NewValue)
		for i in range(2):
			Rate1 = rand.randint(0, 100) / 100.0
			Rate2 = 1.0 - Rate1
			NewValue = Param1.OutputLayerParam[i] * Rate1 + Param2.OutputLayerParam[i] * Rate2
			NewParam.OutputLayerParam.append(NewValue)
		return NewParam

	def __RandomMutateParam(Param:NetworkParamData)->NetworkParamData:
		NewParam = NetworkParamData()
		for i in range(len(Param.HiddenLayerParams)):
			for j in range(2):
				Delta = rand.randint(0, 100) / 100.0
				NewValue = Param.HiddenLayerParams[i][j] + Delta
				NewParam.HiddenLayerParams[i].append(NewValue)
		for i in range(2):
			Delta = rand.randint(0, 100) / 100.0
			NewValue = Param.OutputLayerParam[i] + Delta
			NewParam.OutputLayerParam.append(NewValue)
		return NewParam

	def __RandomCrossNetwork(Network1:EvaluationNetwork, Network2:EvaluationNetwork)->EvaluationNetwork:
		Ret = EvaluationNetwork()
		Ret.ImportParam(__RandomCrossParam(Network1.ExportParam(), Network2.ExportParam()))
		return Ret

	def __RandomMutateNetwork(Network:EvaluationNetwork)->EvaluationNetwork:
		Ret = EvaluationNetwork()
		Ret.ImportParam(__RandomMutateParam(Network.ExportParam()))
		return Ret

	def CreateNewNetworks()->list:#list of NetworkInfo
		for i in range(NumChildren):
			NewNetwork = EvaluationNetwork()
			NewNetwork.CreateNetwork()
			Networks.append(NetworkInfo(NewNetwork))
		return Networks

	def CrossNetworks(Network1:EvaluationNetwork, Network2:EvaluationNetwork)->list:#list of NetworkInfo
		Networks = []
		for i in range(NumChildren):
			NewNetwork = __RandomCrossNetwork(Network1, Network2)
			Networks.append(NetworkInfo(NewNetwork))
		return Networks

	def MutateNetwork(Network:EvaluationNetwork)->list:#list of NetworkInfo
		Networks = []
		for i in range(NumChildren):
			NewNetwork = __RandomMutateNetwork(Network)
			Networks.append(NetworkInfo(NewNetwork))
		return Networks

	def Battle(Network1:NetworkInfo, Network2:NetworkInfo)->int:
		def SearchState(State:Game, Network:EvaluationNetwork)->list:
			class GameStatenInfo:
				def __init__(self):
					pass

			def EvaluateState(Network:EvaluationNetwork, StateInfo:GameStatenInfo)->float:
				InputList = np.array([])
				return Network.Predict(InputList)

			LegalMoves = []
			for Move in range(LegalMoves):
				pass

		Stage = Game()
		for i in range(120):
			Action1 = SearchState(Stage, Network1.Network)
			Action2 = SearchState(Stage, Network2.Network)
			Stage.action(Action1, Action2)

		if Stage._1Pscore > Stage._2Pscore:
			Network1.Win()
			Network2.Lose()
		elif Stage._1Pscore < Stage._2Pscore:
			Network1.Lose()
			Network2.Win()