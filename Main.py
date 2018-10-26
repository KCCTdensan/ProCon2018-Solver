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

if __name__ == '__main__':
	main()