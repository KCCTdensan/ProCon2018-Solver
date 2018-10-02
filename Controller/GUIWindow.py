import wx
from AIEvaluationPanel import AIEvaluationPanel
from ControllerPanel import PlayerInfo
from ControllerPanel import ControllerPanel
from Player import Player

class GUIWindow(wx.Frame):
	"""
	GUIウィンドウ
	"""
	def __init___(self, Player1Info:PlayerInfo, Player2Info:PlayerInfo, AI:Player):
		super().__init__(None, wx.ID_ANY, "Controller")
		self.__RootPanel = wx.Panel(self, wx.ID_ANY)
		self.__RootPanel.SetBackgroundColour("#1f1f1f")
		self.__RootSizer = wx.BoxSizer(wx.VERTICAL)
		self.__AIEvaluationPanel = AIEvaluationPanel(AI)
		self.__RootSizer.Add(self.__AIEvaluationPanel)
		self.__ControllerPanel = ControllerPanel()
		self.__RootSizer.Add(self.__ControllerPanel)
		self.__RootPanel.SetSizer(self.__RootSizer)
		self.__RootPanel.Fit()
		self.Fit()

	def GetIntentions(self):
		return self.__ControllerPanel.GetIntentions()