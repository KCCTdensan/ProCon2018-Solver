import wx
from Prog.Window import WindowFrame
#from Prog.AutoFight import AutoFight

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
	dir_path=("./bin/")
	TrainingData=ReadTrainingDatasFromDirectory(dir_path)
	train_x, val_x = np.split(TrainingData[0], [int(len(TrainingData[0])/10*9)])
	train_y, val_y = np.split(TrainingData[1], [int(len(TrainingData[1])/10*9)])
	AI.learn(train_x, train_y, val_x, val_y)

if __name__ == '__main__':
	main()