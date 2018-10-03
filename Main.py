import wx
from Window import WindowFrame

def main():
	app = wx.App(False)
	frame = WindowFrame()
	frame.Show()
	app.MainLoop()

if __name__ == '__main__':
	main()