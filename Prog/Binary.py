import numpy as np
import os

def ReadTrainingData(FileName:str)->list:
	All = np.fromfile(FileName, np.int32)
	Inputs = []
	for i in range(10):
		Inputs.append(All[i * 12 * 12 : (i + 1) * 12 * 12].reshape((12, 12)))
	OutputPolicy = All[10 * 12 * 12 : 10 * 12 * 12 + 9 * 9].reshape((9, 9))
	OutputValue = All[-1]
	return [Inputs, OutputPolicy, OutputValue]

def ReadTrainingDatasFromDirectory(Path:str):
	Files = os.listdir(Path)
	InputList = []
	OutputPolicyList = []
	OutputValueList = []
	for x in Files:
		if os.path.isfile(Path + x):
			TrainingDataList = ReadTrainingData(Path + x)
			InputList.append(TrainingDataList[0])
			OutputPolicyList.append(TrainingDataList[1])
			OutputValueList.append(TrainingDataList[2])
	InputArray = np.array(InputList)
	OutputPolicyArray = np.array(OutputPolicyList)
	OutputValueArray = np.array(OutputValueList)
	return [InputArray, OutputPolicyArray, OutputValueArray]