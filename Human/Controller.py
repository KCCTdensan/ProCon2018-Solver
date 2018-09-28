import wx

class PlayerInfo:
	def __init__(self, Label:str, Color:str, SelectColor:str):
		self.Label = Label
		self.Color = Color
		self.SelectColor = SelectColor

class ControllerFrame(wx.Frame):
	"""
	コントローラ・パネル
	"""
	class PlayerPanel(wx.Panel):
		"""
		プレイヤー・パネル
		"""
		class ButtonPanel(wx.Panel):
			"""
			ボタン・パネル
			"""
			def __init__(self, Parent:wx.Panel, Color:str, SelectColor:str):
				super().__init__(Parent, wx.ID_ANY)
				self.__sizerButton = wx.GridSizer(rows=3, cols=3, gap=(0, 0))
				self.__Intention = [0, 0]
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
					self.__sizerButton.Add(self.__listButton[i])
					self.Bind(wx.EVT_BUTTON, self.OnButton, id=ID)

				self.SetSizer(self.__sizerButton)

			def OnButton(self, e:wx.Event):
				Button = e.GetEventObject()
				self.ResetIntention()
				for iAction in range(len(self.__listButton)):
					if Button == self.__listButton[iAction]:
						self.__Intention = [iAction % 3 - 1, iAction // 3 - 1]
				Button.SetBackgroundColour(self.__SelectColor)

			def GetIntention(self)->list:
				return self.__Intention.copy()

			def ResetIntention(self):
				self.__listButton[self.__Intention[0] + 1 + (self.__Intention[1] + 1) * 3].SetBackgroundColour(self.__Color)
				self.__Intention = [0, 0]
				
		def __init__(self, Parent:wx.Panel, Label:str, Color:str, SelectColor:str):
			super().__init__(Parent, wx.ID_ANY)
			self.__sizerPlayer = wx.BoxSizer(wx.VERTICAL)

			#コントローラのラベルを作成
			self.__textPlayer = wx.StaticText(self, wx.ID_ANY, Label, style=wx.TE_CENTER)
			self.__textPlayer.SetForegroundColour("#ffffff")
			self.__sizerPlayer.Add(self.__textPlayer, 0, wx.GROW|wx.BOTTOM, border=10)

			#ボタン・パネルを作成
			self.__panelButton = self.ButtonPanel(self, Color, SelectColor)
			self.__sizerPlayer.Add(self.__panelButton)
			
			self.SetSizer(self.__sizerPlayer)
			#self.SetBackgroundColour("#1f1f1f")

		def GetIntention(self)->list:
			return self.__panelButton.GetIntention()

		def ResetIntention(self):
			self.__panelButton.ResetIntention()

	def __init__(self, PlayerInfos:list):
		super().__init__(None, wx.ID_ANY, "Human Controller")

		self.__panelRoot = wx.Panel(self, wx.ID_ANY)
		self.__panelRoot.SetBackgroundColour("#1f1f1f")

		self.__sizerController = wx.BoxSizer(wx.HORIZONTAL)

		#プレイヤー数分のプレイヤー・パネルを作成
		self.__panelPlayers = []
		for i in range(2):
			self.__panelPlayers.append(self.PlayerPanel(self.__panelRoot, PlayerInfos[i].Label, PlayerInfos[i].Color, PlayerInfos[i].SelectColor))
			self.__sizerController.Add(self.__panelPlayers[i], 0, flag=wx.GROW|wx.ALL, border=20)
		
		self.__panelRoot.SetSizer(self.__sizerController)
		self.__panelRoot.Fit()

		self.Fit()
		self.Update()

	def GetIntentions(self)->list:
		return [self.__panelPlayers[0].GetIntention(), self.__panelPlayers[1].GetIntention()]

	def ResetIntentions(self):
		for p in self.__panelPlayers:
			p.ResetIntention()