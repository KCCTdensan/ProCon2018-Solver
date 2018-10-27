import wx
from .AIIndicationDisplayPanel import AIIndicationDisplayPanel
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
			self.__AIIndicationDisplayPanel = AIIndicationDisplayPanel(self.__RootPanel, AI)
			self.__RootSizer.Add(self.__AIIndicationDisplayPanel, 0, wx.GROW)
		else:
			self.__AIIndicationDisplayPanel = None
		# エージェント操作パネル
		self.__ControllerPanel = ControllerPanel(self.__RootPanel, Player1Info, Player2Info)
		self.__RootSizer.Add(self.__ControllerPanel, 0, wx.GROW)
		self.__RootPanel.SetSizer(self.__RootSizer)
		self.__RootPanel.Fit()
		self.Fit()

	def UpdateAIEvaluation(self, Game):
		if self.__AIIndicationDisplayPanel != None:
			self.__AIIndicationDisplayPanel.UpdateEvaluation(Game)

	def GetIntentions(self):
		return self.__ControllerPanel.GetIntentions()

	def ResetIntentions(self):
		self.__ControllerPanel.ResetIntentions()