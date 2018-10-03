import wx

class AIEvaluationPanel(wx.Panel):
	"""
	AI評価ウィンドウ
	"""
	def __init__(self, Parent:wx.Panel, AI):
		super().__init__(Parent, wx.ID_ANY)
		self.__Sizer = wx.BoxSizer(wx.VERTICAL)
		self.__IntentionText = wx.StaticText(self, wx.ID_ANY)
		self.__IntentionText.SetForegroundColour("#000000")
		self.__Sizer.Add(self.__IntentionText, 0, wx.GROW|wx.CENTER|wx.ALL, border=20)
		self.SetBackgroundColour("#ffffff")
		self.SetSizer(self.__Sizer)
		self.Fit()

		self.__AI = AI

	def IntentionDataToText(self, Intention:list)->str:
		if (Intention[0] == 0) and (Intention[1] == 0):
			return "留"
		Ret = ""
		if Intention[0] == -1:
			Ret += "左"
		elif Intention[0] == 1:
			Ret += "右"
		if Intention[1] == -1:
			Ret += "上"
		elif Intention[1] == 1:
			Ret += "下"
		if Intention[2] == 0:
			Ret += "動"
		else:
			Ret += "返"
		return Ret

	def UpdateEvaluation(self):
		Intentions = self.__AI.intention(None)
		Text1P = "1P : "
		Text2P = "2P : "
		Text1P += self.IntentionDataToText(Intentions[0])
		Text2P += self.IntentionDataToText(Intentions[1])
		ShowText = Text1P + ", " + Text2P
		self.__IntentionText.SetLabelText(ShowText)