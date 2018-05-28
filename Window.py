import wx
from Game import *
import Panel

class PlayerInfo:
	def __init__(self, Label:str, Color:str):
		self.Label = Label
		self.Color = Color
		
ID_BUTTON = []
ID_GO:int
ColorPanelBkgnd = "#5f5f5f"
Color1PRegion = "#8e2f2f"
Color2PRegion = "#2f5f8e"
PlayerInfos = (PlayerInfo("1P-1", "#ed1c24"), PlayerInfo("1P-2", "#ff7f27"), PlayerInfo("2P-1", "#22b14c"), PlayerInfo("2P-2", "#00a2e8"))

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
			def __init__(self, Parent:wx.Panel, StagePanel:Panel.Panel):
				super().__init__(Parent, wx.ID_ANY, size=(40, 40))
				self.sizerPanel = wx.BoxSizer(wx.VERTICAL)

				#パネルに点数を表示
				font = wx.Font(30, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
				self.text = wx.StaticText(self, wx.ID_ANY, str(StagePanel.getScore()))
				self.text.SetFont(font)
				self.text.Center()
				self.sizerPanel.Add(self.text, flag=wx.GROW)

				self.SetSizer(self.sizerPanel)

		def __init__(self, Parent:wx.Panel, Stage:Game):
			super().__init__(Parent, wx.ID_ANY)
			self.Stage = Stage
			self.sizerStage = wx.GridSizer(rows=len(self.Stage._Panels), cols=len(self.Stage._Panels[0]), gap=(0, 0))

			#それぞれのプレイヤーの現在位置を示す枠パネルを作成
			self.listPanelPosition = []
			for ip in range(len(PlayerInfos)):
				self.listPanelPosition.append(wx.Panel(self, wx.ID_ANY, size=(50, 50)))
				self.listPanelPosition[ip].SetBackgroundColour(PlayerInfos[ip].Color)
				
			#パネル・パネルを作成
			self.listPanelPanel = []
			for iy in range(len(self.Stage._Panels)):
				self.listPanelPanel.append([])
				for ix in range(len(self.Stage._Panels[0])):
					self.listPanelPanel[iy].append(self.PanelPanel(self, self.Stage._Panels[iy][ix]))
					self.listPanelPanel[iy][ix].text.SetForegroundColour("#ffffff")
					self.sizerStage.Add(self.listPanelPanel[iy][ix], 0, wx.ALL, border=5)
					
			#枠パネルを現在位置のところに移動
			Agents = [self.Stage._1PAgents[0], self.Stage._1PAgents[1], self.Stage._2PAgents[0], self.Stage._2PAgents[1]]
			for ip in range(len(PlayerInfos)):
				Point = Agents[ip]._point
				self.listPanelPosition[ip].SetPosition(self.PanelPosition(Point[1], Point[0]))

			self.SetSizer(self.sizerStage)
			self.Fit()

		def PanelPosition(self, x, y)->tuple:
			PanelPos = list(self.listPanelPanel[y][x].GetPosition())
			return (PanelPos[0] - 5, PanelPos[1] - 5)

		def Update(self):
			Agents = [self.Stage._1PAgents[0], self.Stage._1PAgents[1], self.Stage._2PAgents[0], self.Stage._2PAgents[1]]
			#現在位置を示す枠パネルの更新
			for ip in range(len(PlayerInfos)):
				Point = Agents[ip]._point
				self.listPanelPosition[ip].SetPosition(self.PanelPosition(Point[1], Point[0]))

			#ステージのパネルの更新
			for iy in range(len(self.Stage._Panels)):
				for ix in range(len(self.Stage._Panels[0])):
					State = self.Stage._Panels[iy][ix].getState()
					if State == 0:
						self.listPanelPanel[iy][ix].SetBackgroundColour(ColorPanelBkgnd)
					elif State == 1:						
						self.listPanelPanel[iy][ix].SetBackgroundColour(Color1PRegion)
					elif State == 2:						
						self.listPanelPanel[iy][ix].SetBackgroundColour(Color2PRegion)

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
				def __init__(self, Parent:wx.Panel, SelectColor:str, ID:list):
					super().__init__(Parent, wx.ID_ANY)
					self.sizerButton = wx.GridSizer(rows=3, cols=3, gap=(0, 0))
					self.Intention = [0, 0]
					self.listButton = []
					self.SelectColor = SelectColor

					#それぞれのボタンを作成
					ButtonCollection = ("左上", "上", "右上", "左", "留まる", "右", "左下", "下", "右下")
					for i in range(len(ButtonCollection)):
						ID.append(wx.NewId())
						self.listButton.append(wx.Button(self, ID[i], ButtonCollection[i], size=(50, 50)))
						self.listButton[i].SetBackgroundColour(SelectColor)
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
					Button.SetForegroundColour(self.SelectColor)

				def GetIntention(self)->list:
					return self.Intention

				def ResetIntention(self):				
					self.Intention = [0, 0]
					for b in self.listButton:
						b.SetForegroundColour("#ffffff")
					
			def __init__(self, Parent:wx.Panel, Label:str, SelectColor:str, ButtonID:list):
				super().__init__(Parent, wx.ID_ANY)
				self.sizerPlayer = wx.BoxSizer(wx.VERTICAL)

				#コントローラのラベルを作成
				self.textPlayer = wx.StaticText(self, wx.ID_ANY, Label, style=wx.TE_CENTER)
				self.textPlayer.SetForegroundColour("#ffffff")
				self.sizerPlayer.Add(self.textPlayer, 0, wx.GROW|wx.BOTTOM, border=10)

				#ボタン・パネルを作成
				self.panelButton = self.ButtonPanel(self, SelectColor, ButtonID)
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
			for i in range(len(PlayerInfos)):
				ID_BUTTON.append([])
				self.listPanel.append(self.PlayerPanel(self, PlayerInfos[i].Label, PlayerInfos[i].Color, ID_BUTTON[i]))
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

		self.SetSize((780, len(gamePanels)*50 + 380))

		self.rootPanel = wx.Panel(self, wx.ID_ANY)
		self.rootPanel.SetBackgroundColour("#1f1f1f")

		self.rootLayout = wx.BoxSizer(wx.VERTICAL)

		#ステージ・パネルを作成
		self.panelStage = self.StagePanel(self.rootPanel, self.game)
		self.rootLayout.Add(self.panelStage, 0, wx.ALIGN_CENTER|wx.TOP, border=50)

		#コントローラ・パネルを作成
		self.panelController = self.ControllerPanel(self.rootPanel)
		self.rootLayout.Add(self.panelController, 0, wx.ALIGN_CENTER)
		
		#実行ボタンを作成
		ID_GO = wx.NewId()
		self.buttonAction = wx.Button(self.rootPanel, ID_GO, "実行", size=(80, 40))
		self.rootLayout.Add(self.buttonAction, 0, wx.ALIGN_CENTER|wx.BOTTOM, border=30)
		self.Bind(wx.EVT_BUTTON, self.OnButton, id=ID_GO)

		self.rootPanel.SetSizer(self.rootLayout)

		self.Update()

	def OnButton(self, e):
		Intentions = self.panelController.GetIntentions()
		self.game.action([Intentions[0], Intentions[1]], [Intentions[2], Intentions[3]])
		self.game.score()
		self.Update()
		self.panelController.ResetIntentions()

	def Update(self):
		self.panelStage.Update()
		self.Refresh()