import wx

class PlayingCardsPanel(wx.Panel):
	"""
	トランプ情報表示ウィンドウ
	"""
	def __init__(self, Parent: wx.Panel, AI):
		super().__init__(Parent, wx.ID_ANY)
		self.__Sizer = wx.BoxSizer(wx.VERTICAL)

		self.__PlayingCardsText = wx.StaticText(self, wx.ID_ANY)
		self.__PlayingCardsText.SetForegroundColour("#000000")
		self.__Sizer.Add(self.__PlayingCardsText, 0, wx.GROW|wx.CENTER|wx.ALL, border = 20)

		self.SetBackgroundColour("#ffffff")
		self.SetSizer(self.__Sizer)
		self.Fit()
		
		self.__AI = AI


	# 「JOKER &」
	def IntentionDataToText(self, Intention: list) -> str:
		info = ""
		if (Intention[0] == 0) and (Intention[1] == 0): # 停留
			info += "5"
		elif Intention[0] == -1: # 左側
			if Intention[1] == -1: # 上
				info += "3"
			elif Intention[1] == 1: # 下
				info +=  "9"
			else: # 左
				info +=  "6"
		elif Intention[0] == 1: # 右側
			if Intention[1] == -1: # 上
				info +=  "1"
			elif Intention[1] == 1: # 下
				info +=  "7"
			else: # 右
				info +=  "4"

		return info


	def UpdatePlayingCardsInfo(self):
		Intentions = self.__AI.intention(None)
		Text1P = "1P : "
		Text2P = "2P : "
		Text1P += self.IntentionDataToText(Intentions[0])
		Text2P += self.IntentionDataToText(Intentions[1])
		ShowText = Text1P + ", " + Text2P
		self.__PlayingCardsText.SetLabelText(ShowText)
