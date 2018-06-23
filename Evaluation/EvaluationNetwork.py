import numpy as np
import pickle
from Layer import Layer
from Layer import InputLayer
from Layer import HiddenLayer
from Layer import OutputLayer

class NetworkParamData():
	#HiddenLayerParams	[[Weights:np.ndarray, Biases:np.ndarray], [Weights:np.ndarray, Biases:np.ndarray], ..., [Weights:np.ndarray, Biases:np.ndarray]]
	#OutputLayerParam	[Weights:np.ndarray, Bias:float]
	def __init__(self):
		self.HiddenLayerParams = []
		self.OutputLayerParam = []

	def LoadParamFromFile(self, FileName:str):
		with open(FileName, 'r') as f:
			pickle.dump(self, f)

	def SaveParamToFile(self, FileName:str):
		with open(FileName, 'w') as f:
			pickle.dump(self, f)

class EvaluationNetwork():
	NumInputLayerUnits = 3
	NumHiddenLayerUnits = 10
	NumHiddenLayers = 3

	def CreateNetwork(self):
		self.Layers = []
		self.NumLayerUnits = []
		self.Layers.append(InputLayer(EvaluationNetwork.NumInputLayerUnits))
		self.NumLayerUnits.append(EvaluationNetwork.NumInputLayerUnits)
		for i in range(NumHiddenLayers):
			self.Layers.append(HiddenLayer(self.NumLayerUnits[i], EvaluationNetwork.NumHiddenLayerUnits))
			self.NumLayerUnits.append(EvaluationNetwork.NumHiddenLayerUnits)
		self.Layers.append(OutputLayer(self.NumLayerUnits[NumHiddenLayers]))

		for i in range(NumHiddenLayers + 1):
			self.Layers[i].SetNextLayer(self.Layers[i + 1])

	def Predict(self, InputData:np.ndarray)->float:
		return self.Layers[0].Forward(InputData)

	def ImportParam(self, Data:NetworkParamData):
		CreateNetwork(self, len(Data.HiddenParams))
		for i in range(NumHiddenLayers):
			self.Layers[i + 1].SetParam(Data.HiddenLayerParams[i][0], Data.HiddenLayerParams[i][1])
		self.Layers[NumHiddenLayers + 1].SetParam(Data.OutputLayerParam[0], Data.OutputLayerParam[1])

	def ExportParam(self)->NetworkParamData:
		Ret = NetworkParamData()
		for i in range(1, NumHiddenLayers + 1):
			Ret.HiddenLayerParams.append(self.Layers[i].GetParam())
		Ret.OutputLayerParam = self.Layers[NumHiddenLayers + 1].GetParam()