import wx
from Game import Game
from Panel import Panel

		
ID_BUTTON = []
ID_GO:int
ColorPanelBkgnd = "#5f5f5f"
ColorPanel1PRegion = "#af5f5f"
ColorPanel2PRegion = "#5f8faf"
ColorPanel1P2PRegion = "#a349a4"
ColorPanel1PTile = "#8e2f2f"
ColorPanel2PTile = "#2f5f8e"
NumPlayers = 4

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