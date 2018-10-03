import wx
from ControllerPanel import PlayerInfo
from GUIWindow import GUIWindow
from Player import Player
from AI import Test_ai

class Player_Human():
	def __init__(self, AI:Player):
		self.__Intention = [[int, int, int], [int, int, int]]
		#PlayerInfo("2P-1", "#22b14c", "#82e8a0"), PlayerInfo("2P-2", "#00a2e8", "#75d6ff"))
		Player1Info = PlayerInfo("1P-1", "#ed1c24", "#f78e94")
		Player2Info = PlayerInfo("1P-2", "#ff7f27", "#ffbe93")
		self.__Window = GUIWindow(Player1Info, Player2Info, AI)

	def Think(self):
		self.__Window.UpdateAIEvaluation()

	def intention(self)->list:
		return self.__Window.GetIntentions()

	def getResult(self):
		return

	def showWindow(self):
		self.__Window.Show()
		self.Think()

#TEST
def Test():
	app = wx.App(False)
	h = Player_Human(Test_ai.AI())
	h.showWindow()
	app.MainLoop()

if __name__=="__main__":
	Test()