import wx
from AIEvaluationPanel import AIEvaluationPanel
from ControllerPanel import PlayerInfo
from ControllerPanel import ControllerPanel
from Player import Player

class GUIWindow(wx.Frame):
	"""
	GUIウィンドウ
	"""
	def __init__(self, Player1Info:PlayerInfo, Player2Info:PlayerInfo, AI:Player):
		super().__init__(None, wx.ID_ANY, "Controller")
		self.__RootPanel = wx.Panel(self, wx.ID_ANY)
		self.__RootPanel.SetBackgroundColour("#1f1f1f")
		self.__RootSizer = wx.BoxSizer(wx.VERTICAL)
		self.__AIEvaluationPanel = AIEvaluationPanel(self.__RootPanel, AI)
		self.__RootSizer.Add(self.__AIEvaluationPanel)
		self.__ControllerPanel = ControllerPanel(self.__RootPanel, Player1Info, Player2Info)
		self.__RootSizer.Add(self.__ControllerPanel)
		self.__RootPanel.SetSizer(self.__RootSizer)
		self.__RootPanel.Fit()
		self.Fit()

	def UpdateAIEvaluation(self):
		self.__AIEvaluationPanel.UpdateEvaluation()

	def GetIntentions(self):
		return self.__ControllerPanel.GetIntentions()