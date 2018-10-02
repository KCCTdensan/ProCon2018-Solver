import wx

class PlayerInfo:
	def __init__(self, Label:str, ButtonColor:str, ButtonSelectColor:str):
		self.Label = Label
		self.Color = ButtonColor
		self.SelectColor = ButtonSelectColor

class IntentionKeysPanel(wx.Panel):
	"""
	方向キー・パネル
	"""
	def __init__(self, Parent:wx.Panel, Color:str, SelectColor:str):
		super().__init__(Parent, wx.ID_ANY)
		self.__Sizer = wx.GridSizer(rows=3, cols=3, gap=(0, 0))
		self.__Intention = [0, 0, 0]
		self.__listButton = []
		self.__Color = Color
		self.__SelectColor = SelectColor
		#それぞれのボタンを作成
		ButtonCollection = ("左上", "上", "右上", "左", "留まる", "右", "左下", "下", "右下")
		ButtonSize = (50, 50)
		for i in range(len(ButtonCollection)):
			ID = wx.NewId()
			self.__listButton.append(wx.Button(self, ID, ButtonCollection[i], size=ButtonSize))
			self.__listButton[i].SetBackgroundColour(Color)
			self.__listButton[i].SetForegroundColour("#ffffff")
			self.__Sizer.Add(self.__listButton[i])
			self.Bind(wx.EVT_BUTTON, self.__OnButton, id=ID)
			self.SetSizer(self.__Sizer)

	def __OnButton(self, e:wx.Event):
		Button = e.GetEventObject()
		self.ResetIntention()
		for iAction in range(len(self.__listButton)):
			if Button == self.__listButton[iAction]:
				self.__Intention = [iAction % 3 - 1, iAction // 3 - 1, 0]#修正必須
		Button.SetBackgroundColour(self.__SelectColor)

	def GetIntention(self)->list:
		return self.__Intention.copy()

	def ResetIntention(self):
		self.__listButton[self.__Intention[0] + 1 + (self.__Intention[1] + 1) * 3].SetBackgroundColour(self.__Color)
		self.__Intention = [0, 0, 0]

class PlayerPanel(wx.Panel):
	"""
	プレイヤー・パネル
	"""			
	def __init__(self, Parent:wx.Panel, Label:str, Color:str, SelectColor:str):
		super().__init__(Parent, wx.ID_ANY)
		self.__Sizer = wx.BoxSizer(wx.VERTICAL)

		#コントローラのラベルを作成
		self.__LabelText = wx.StaticText(self, wx.ID_ANY, Label, style=wx.TE_CENTER)
		self.__LabelText.SetForegroundColour("#ffffff")
		self.__Sizer.Add(self.__LabelText, 0, wx.GROW|wx.BOTTOM, border=10)

		#ボタン・パネルを作成
		self.__IntentionKeysPanel = self.IntentionKeysPanel(self, Color, SelectColor)
		self.__Sizer.Add(self.__IntentionKeysPanel)
		
		self.SetSizer(self.__Sizer)
		self.Fit()

	def GetIntention(self)->list:
		return self.__IntentionKeysPanel.GetIntention()

	def ResetIntention(self):
		self.__IntentionKeysPanel.ResetIntention()

class ControllerPanel(wx.Panel):
	"""
	コントローラ・パネル
	"""
	def __init__(self, Parent:wx.Panel, Player1Info:PlayerInfo, Player2Info:PlayerInfo):
		super().__init__(Parent, wx.ID_ANY)
		self.__Sizer = wx.BoxSizer(wx.HORIZONTAL)

		#プレイヤー1のパネルを作成
		self.__Player1Panel = PlayerPanel(self, Player1Info.Label, Player1Info.Color, Player1Info.SelectColor)
		self.__Sizer.Add(self.__Player1Panel, wx.GROW|wx.ALL, border=20)

		#プレイヤー2のパネルを作成
		self.__Player2Panel = PlayerPanel(self, Player2Info.Label, Player2Info.Color, Player2Info.SelectColor)
		self.__Sizer.Add(self.__Player2Panel, wx.GROW|wx.ALL, border=20)	

		self.SetSizer(self.__Sizer)
		self.Fit()

	def GetIntentions(self)->list:
		return [self.__Player1Panel.GetIntention(), self.__Player2Panel.GetIntention()]

	def ResetIntentions(self):
		self.__Player1Panel.ResetIntention()
		self.__Player2Panel.ResetIntention()