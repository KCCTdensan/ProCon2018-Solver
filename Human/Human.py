import wx
from Controller import ControllerFrame
from Controller import PlayerInfo

class Player_Human():
	def __init__(self):
		self.__Intention = [[int, int, int], [int, int, int]]
		PlayerInfos = (PlayerInfo("1P-1", "#ed1c24", "#f78e94"), PlayerInfo("1P-2", "#ff7f27", "#ffbe93"))#, PlayerInfo("2P-1", "#22b14c", "#82e8a0"), PlayerInfo("2P-2", "#00a2e8", "#75d6ff"))
		self.__Window = ControllerFrame(PlayerInfos)

	def intension(self)->list:
		return self.__Window.GetIntentions()

	def getResult(self):
		return

	def showWindow(self):
		self.__Window.Show()

#TEST
def Test():
	app = wx.App(False)
	h = Player_Human()
	h.showWindow()
	app.MainLoop()

if __name__=="__main__":
	Test()