import wx
from .AIEvaluationPanel import AIEvaluationPanel
from .PlayingCardsPanel import PlayingCardsPanel
from .ControllerPanel import ControllerPanel

class ControllerFrame(wx.Frame):
	"""
	GUIウィンドウ
	"""
	def __init__(self, Player1Info, Player2Info, AI):
		super().__init__(None, wx.ID_ANY, "Controller")
		self.__RootPanel = wx.Panel(self, wx.ID_ANY)
		self.__RootPanel.SetBackgroundColour("#1f1f1f")
		self.__RootSizer = wx.BoxSizer(wx.VERTICAL)
		
		# AI指示表示パネル
		if AI != None:
			self.__AIEvaluationPanel = AIEvaluationPanel(self.__RootPanel, AI)
			self.__RootSizer.Add(self.__AIEvaluationPanel, 0, wx.GROW)
		else:
			self.__AIEvaluationPanel = None

		# トランプ情報表示パネル
		self.__PlayingCardsPanel = PlayingCardsPanel(self.__RootPanel, AI)
		self.__RootSizer.Add(self.__PlayingCardsPanel, 0, wx.GROW)
		
		# エージェント操作パネル
		self.__ControllerPanel = ControllerPanel(self.__RootPanel, Player1Info, Player2Info)
		self.__RootSizer.Add(self.__ControllerPanel, 0, wx.GROW)
		self.__RootPanel.SetSizer(self.__RootSizer)
		self.__RootPanel.Fit()
		self.Fit()

	def UpdateAIEvaluation(self, Game):
		if self.__AIEvaluationPanel != None:
			self.__AIEvaluationPanel.UpdateEvaluation(Game)
		self.__PlayingCardsPanel.UpdatePlayingCardsInfo(Game)

	def GetIntentions(self):
		return self.__ControllerPanel.GetIntentions()

	def ResetIntentions(self):
		self.__ControllerPanel.ResetIntentions()