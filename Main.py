import wx
from Window import WindowFrame
from AutoFight import AutoFight

def main():
	app = wx.App(False)
	frame = WindowFrame()
	frame.Show()
	app.MainLoop()

def main2():
    A = AutoFight()
    A.AutoFight(1000)

def main3():
	import numpy as np
	from Binary import ReadTrainingDatasFromDirectory
	from Engine.kerasDQN_ai import kerasDQNPlayer

	AI = kerasDQNPlayer(1)
	dir_path=("./bin/TrainingData/")
	TrainingData=ReadTrainingDatasFromDirectory(dir_path)
	train_x, val_x = np.split(TrainingData[0], [int(len(TrainingData[0])/10*9)])
	train_y, val_y = np.split(TrainingData[1], [int(len(TrainingData[1])/10*9)])
	print(TrainingData[0].shape, train_x[0:19000].shape, val_x[0:1000].shape )
	AI.learn(train_x[0:19000], train_y[0:19000], val_x[0:1000], val_y[0:1000])

if __name__ == '__main__':
	main3()