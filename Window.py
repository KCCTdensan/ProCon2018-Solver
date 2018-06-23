import wx
from Game import Game
from Panel import Panel

class PlayerInfo:
	def __init__(self, Label:str, Color:str, SelectColor:str):
		self.Label = Label
		self.Color = Color
		self.SelectColor = SelectColor
		
ID_BUTTON = []
ID_GO:int
ColorPanelBkgnd = "#5f5f5f"
ColorPanel1PRegion = "#af5f5f"
ColorPanel2PRegion = "#5f8faf"
ColorPanel1P2PRegion = "#a349a4"
ColorPanel1PTile = "#8e2f2f"
ColorPanel2PTile = "#2f5f8e"
PlayerInfos = (PlayerInfo("1P-1", "#ed1c24", "#f78e94"), PlayerInfo("1P-2", "#ff7f27", "#ffbe93"), PlayerInfo("2P-1", "#22b14c", "#82e8a0"), PlayerInfo("2P-2", "#00a2e8", "#75d6ff"))
NumPlayers = len(PlayerInfos)

class WindowFrame(wx.Frame):
	"""
	メインウィンドウ
	"""
	class StagePanel(wx.Panel):
		"""
		ステージ・パネル
		"""
		class PanelPanel(wx.Panel):
			"""
			パネル・パネル
			"""
			def __init__(self, Parent:wx.Panel, StagePanel:Panel):
				super().__init__(Parent, wx.ID_ANY, size=(40, 40))
				self.sizerPanel = wx.BoxSizer(wx.VERTICAL)

				#パネルに点数を表示
				font = wx.Font(20, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_LIGHT)
				self.text = wx.StaticText(self, wx.ID_ANY, str(StagePanel.getScore()))
				self.text.SetFont(font)
				self.text.Center()
				self.text.SetForegroundColour("#ffffff")
				self.sizerPanel.Add(self.text, flag=wx.GROW)

				self.SetSizer(self.sizerPanel)

		def __init__(self, Parent:wx.Panel, Panels:list):
			super().__init__(Parent, wx.ID_ANY)
			self.sizerStage = wx.GridSizer(rows=len(Panels), cols=len(Panels[0]), gap=(0, 0))

			#それぞれのプレイヤーの現在位置を示す枠パネルを作成
			self.listPanelPosition = []
			for ip in range(NumPlayers):
				self.listPanelPosition.append(wx.Panel(self, wx.ID_ANY, size=(50, 50)))
				self.listPanelPosition[ip].SetBackgroundColour(PlayerInfos[ip].Color)
				
			#パネル・パネルを作成
			self.listPanelPanel = []
			for iy in range(len(Panels)):
				self.listPanelPanel.append([])
				for ix in range(len(Panels[0])):
					self.listPanelPanel[iy].append(self.PanelPanel(self, Panels[iy][ix]))
					self.sizerStage.Add(self.listPanelPanel[iy][ix], 0, wx.ALL, border=5)

			self.SetSizer(self.sizerStage)
			self.Fit()

		def PanelPosition(self, x, y)->tuple:
			PanelPos = list(self.listPanelPanel[y][x].GetPosition())
			return (PanelPos[0] - 5, PanelPos[1] - 5)

		def Update(self, Agents:list, Panels:list):
			#現在位置を示す枠パネルの更新
			for ip in range(NumPlayers):
				Point = Agents[ip]._point
				self.listPanelPosition[ip].SetPosition(self.PanelPosition(Point[1], Point[0]))

			#ステージのパネルの更新
			for iy in range(len(Panels)):
				for ix in range(len(Panels[0])):
					State = Panels[iy][ix].getState()
					if State == 0:
						Surrounded = Panels[iy][ix].getSurrounded()
						if not Surrounded[0] and not Surrounded[1]:
							self.listPanelPanel[iy][ix].SetBackgroundColour(ColorPanelBkgnd)
						elif Surrounded[0] and not Surrounded[1]:
							self.listPanelPanel[iy][ix].SetBackgroundColour(ColorPanel1PRegion)
						elif not Surrounded[0] and Surrounded[1]:
							self.listPanelPanel[iy][ix].SetBackgroundColour(ColorPanel2PRegion)
						elif Surrounded[0] and Surrounded[1]:							
							self.listPanelPanel[iy][ix].SetBackgroundColour(ColorPanel1P2PRegion)
					elif State == 1:						
						self.listPanelPanel[iy][ix].SetBackgroundColour(ColorPanel1PTile)
					elif State == 2:						
						self.listPanelPanel[iy][ix].SetBackgroundColour(ColorPanel2PTile)

	class PointPanel(wx.Panel):
		"""
		ポイント・パネル
		"""
		def __init__(self, Parent:wx.Panel):
			super().__init__(Parent, wx.ID_ANY)
			
			font = wx.Font(15, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_LIGHT)
			self.sizerPoint = wx.BoxSizer(wx.VERTICAL)
			self.text1PTilePoint = wx.StaticText(self, wx.ID_ANY, "1P Tile Point : 000")
			self.text1PTilePoint.SetForegroundColour("#ffffff")
			self.text1PTilePoint.SetFont(font)
			self.text1PRegionPoint = wx.StaticText(self, wx.ID_ANY, "1P Region Point : 000")
			self.text1PRegionPoint.SetForegroundColour("#ffffff")
			self.text1PRegionPoint.SetFont(font)
			self.text2PTilePoint = wx.StaticText(self, wx.ID_ANY, "2P Tile Point : 000")
			self.text2PTilePoint.SetForegroundColour("#ffffff")
			self.text2PTilePoint.SetFont(font)
			self.text2PRegionPoint = wx.StaticText(self, wx.ID_ANY, "2P Region Point : 000")
			self.text2PRegionPoint.SetForegroundColour("#ffffff")
			self.text2PRegionPoint.SetFont(font)

			self.sizerPoint.Add(self.text1PTilePoint, flag = wx.GROW)
			self.sizerPoint.Add(self.text1PRegionPoint, flag = wx.GROW)
			self.sizerPoint.Add(self.text2PTilePoint, flag = wx.GROW)
			self.sizerPoint.Add(self.text2PRegionPoint, flag = wx.GROW)

			self.SetSizer(self.sizerPoint)

		def Update(self, Points:list):
			self.text1PTilePoint.SetLabelText("1P Tile Point : " + str(Points[0]))
			self.text1PRegionPoint.SetLabelText("1P Region Point : " + str(Points[1]))
			self.text2PTilePoint.SetLabelText("2P Tile Point : " + str(Points[2]))
			self.text2PRegionPoint.SetLabelText("2P Region Point : " + str(Points[3]))

	class ControllerPanel(wx.Panel):
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
				def __init__(self, Parent:wx.Panel, Color:str, SelectColor:str, ID:list):
					super().__init__(Parent, wx.ID_ANY)
					self.sizerButton = wx.GridSizer(rows=3, cols=3, gap=(0, 0))
					self.Intention = [0, 0]
					self.listButton = []
					self.Color = Color
					self.SelectColor = SelectColor

					#それぞれのボタンを作成
					ButtonCollection = ("左上", "上", "右上", "左", "留まる", "右", "左下", "下", "右下")
					for i in range(len(ButtonCollection)):
						ID.append(wx.NewId())
						self.listButton.append(wx.Button(self, ID[i], ButtonCollection[i], size=(50, 50)))
						self.listButton[i].SetBackgroundColour(Color)
						self.listButton[i].SetForegroundColour("#ffffff")
						self.sizerButton.Add(self.listButton[i], 0, wx.GROW)
						self.Bind(wx.EVT_BUTTON, self.OnButton, id=ID[i])

					self.SetSizer(self.sizerButton)
	
				def OnButton(self, e:wx.Event):
					ID = e.GetId()
					Button = e.GetEventObject()
					self.ResetIntention()
					for Player in ID_BUTTON:
						for iAction in range(len(Player)):
							if Player[iAction] == ID:
								self.Intention = [iAction % 3 - 1, iAction // 3 - 1]
					Button.SetBackgroundColour(self.SelectColor)

				def GetIntention(self)->list:
					return self.Intention.copy()

				def ResetIntention(self):
					self.listButton[self.Intention[0] + 1 + (self.Intention[1] + 1) * 3].SetBackgroundColour(self.Color)
					self.Intention = [0, 0]
					
			def __init__(self, Parent:wx.Panel, Label:str, Color:str, SelectColor:str, ButtonID:list):
				super().__init__(Parent, wx.ID_ANY)
				self.sizerPlayer = wx.BoxSizer(wx.VERTICAL)

				#コントローラのラベルを作成
				self.textPlayer = wx.StaticText(self, wx.ID_ANY, Label, style=wx.TE_CENTER)
				self.textPlayer.SetForegroundColour("#ffffff")
				self.sizerPlayer.Add(self.textPlayer, 0, wx.GROW|wx.BOTTOM, border=10)

				#ボタン・パネルを作成
				self.panelButton = self.ButtonPanel(self, Color, SelectColor, ButtonID)
				self.sizerPlayer.Add(self.panelButton)

				self.SetSizer(self.sizerPlayer)

			def GetIntention(self)->list:
				return self.panelButton.GetIntention()

			def ResetIntention(self):
				self.panelButton.ResetIntention()

		def __init__(self, Parent:wx.Panel):
			super().__init__(Parent, wx.ID_ANY)
			self.sizerController = wx.BoxSizer(wx.HORIZONTAL)

			#プレイヤー数分のコントローラ・パネルを作成
			self.listPanel = []
			for i in range(NumPlayers):
				ID_BUTTON.append([])
				self.listPanel.append(self.PlayerPanel(self, PlayerInfos[i].Label, PlayerInfos[i].Color, PlayerInfos[i].SelectColor, ID_BUTTON[i]))
				self.sizerController.Add(self.listPanel[i], 0, flag=wx.GROW|wx.ALL|wx.ALIGN_CENTER, border=20)

			self.SetSizer(self.sizerController)

		def GetIntentions(self)->list:
			return [self.listPanel[0].GetIntention(), self.listPanel[1].GetIntention(), self.listPanel[2].GetIntention(), self.listPanel[3].GetIntention()]

		def ResetIntentions(self):
			for p in self.listPanel:
				p.ResetIntention()

	def __init__(self):
		super().__init__(None, wx.ID_ANY, "Procon", pos=(100, 50))
		self.game = Game()
		gamePanels = self.game.getPanels()

		self.SetSize((780, len(gamePanels)*50 + 440))

		self.rootPanel = wx.Panel(self, wx.ID_ANY)
		self.rootPanel.SetBackgroundColour("#1f1f1f")

		self.rootLayout = wx.BoxSizer(wx.VERTICAL)

		#ステージ・パネルを作成
		self.panelStage = self.StagePanel(self.rootPanel, self.game.getPanels())
		self.rootLayout.Add(self.panelStage, 0, wx.ALIGN_CENTER|wx.ALL, border=15)

		#ポイント・パネルを作成
		self.panelPoint = self.PointPanel(self.rootPanel)
		self.rootLayout.Add(self.panelPoint, 0, wx.GROW|wx.LEFT, border=50)

		#コントローラ・パネルを作成
		self.panelController = self.ControllerPanel(self.rootPanel)
		self.rootLayout.Add(self.panelController, 0, wx.ALIGN_CENTER|wx.BOTTOM, border=15)
		
		#実行ボタンを作成
		ID_GO = wx.NewId()
		self.buttonAction = wx.Button(self.rootPanel, ID_GO, "実行", size=(80, 40))
		self.rootLayout.Add(self.buttonAction, 0, wx.ALIGN_CENTER|wx.BOTTOM, border=15)
		self.Bind(wx.EVT_BUTTON, self.OnButton, id=ID_GO)

		self.rootPanel.SetSizer(self.rootLayout)

		#self.SetSize((self.rootPanel.GetMaxWidth(), self.rootPanel.GetMaxHeight()))

		self.Update()

	def OnButton(self, e):
		Intentions = self.panelController.GetIntentions()
		self.game.action([Intentions[0], Intentions[1]], [Intentions[2], Intentions[3]])
		self.game.score()
		self.Update()
		self.panelController.ResetIntentions()

	def Update(self):
		self.panelStage.Update([self.game._1PAgents[0], self.game._1PAgents[1], self.game._2PAgents[0], self.game._2PAgents[1]], self.game.getPanels())
		self.panelPoint.Update(self.game.getPoints())
		self.Refresh()