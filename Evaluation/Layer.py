import numpy as np
import math

class Layer():
	def sigmoid(Array:np.ndarray):
		return np.vectorize(lambda x: 1.0/(1.0 + math.exp(-x)))(Array)

	def relu(Array:np.ndarray):
		return np.maximum(Array, 0)

	def Forward(self, InputData:np.ndarray):
		pass

class InputLayer(Layer):
	def __init__(self, NumUnits:int):
		self.NumUnits = NumUnits

	def SetNextLayer(self, NextLayer:Layer):
		self.NextLayer = NextLayer

	def Forward(self, InputData:np.ndarray):
		return self.NextLayer.Forward(InputData)

class HiddenLayer(Layer):
	def __init__(self, NumPrevUnits:int, NumUnits:int):
		self.NumPrevUnits = NumPrevUnits
		self.NumUnits = NumUnits
		self.Weights = np.random.random_sample((NumPrevUnits, NumUnits))
		self.Biases = -np.random.random_sample((NumUnits))

	def SetNextLayer(self, NextLayer:Layer):
		self.NextLayer = NextLayer

	def Forward(self, InputData:np.ndarray):
		return self.NextLayer.Forward(Layer.relu(np.dot(InputData, self.Weights)) + self.Biases)

	def SetParam(self, Weights:np.ndarray, Biases:np.ndarray):
		self.Weights = Weights
		self.Biases = Biases

	def GetParam(self)->list:
		return [self.Weights, self.Biases]

class OutputLayer(Layer):
	def __init__(self, NumPrevUnits:int):
		self.NumPrevUnits = NumPrevUnits
		self.Weights = np.random.random_sample((NumPrevUnits))
		self.Bias = -np.random.random_sample()

	def Forward(self, InputData:np.ndarray):
		return Layer.sigmoid(np.dot(InputData, self.Weights) + self.Bias)

	def SetParam(self, Weights:np.ndarray, Bias:float):
		self.Weights = Weights
		self.Bias = Bias

	def GetParam(self)->list:
		return [self.Weights, self.Bias]