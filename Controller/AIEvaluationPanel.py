import wx

class AIEvaluationPanel(wx.Panel):
	"""
	AI評価ウィンドウ
	"""
	def __init__(self, Parent:wx.Panel, AI):
		super().__init__(Parent, wx.ID_ANY)
		self.__AI = AI