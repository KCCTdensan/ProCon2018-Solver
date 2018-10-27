def main():
    import wx
    from Prog.Window import WindowFrame
    app = wx.App(False)
    frame = WindowFrame()
    frame.Show()
    app.MainLoop()

def main2():
    from Prog.AutoFight import AutoFight
    A = AutoFight()
    A.AutoFight(1000)

def main3():
	import numpy as np
	from Prog.Binary import ReadTrainingDatasFromDirectory
	from Prog.Engine.kerasDQN_ai import kerasDQNPlayer

	AI = kerasDQNPlayer(1)
	dir_path=("./bin/")
	TrainingData=ReadTrainingDatasFromDirectory(dir_path)
	train_x, val_x = np.split(TrainingData[0], [int(len(TrainingData[0])/10*9)])
	train_y1, val_y1 = np.split(TrainingData[1], [int(len(TrainingData[1])/10*9)])
	train_y2, val_y2 = np.split(TrainingData[2], [int(len(TrainingData[2])/10*9)])
	AI.learn(train_x, train_y1, train_y2, val_x, val_y1, val_y2)

if __name__ == '__main__':
	main()