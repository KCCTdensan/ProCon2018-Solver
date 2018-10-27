import wx
import sys
from .Game import Game
from .Panel import Panel
from .GUI.ControllerWindow import ControllerFrame
from .Engine.KA_31 import KA_31
from .Engine.kerasDQN_ai import kerasDQNPlayer

class PlayerInfo:
	def __init__(self, Label:str, Color:str, SelectColor:str):
		self.Label = Label
		self.Color = Color
		self.SelectColor = SelectColor
		
#ID_BUTTON = []
#ID_GO:int
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

	def __init__(self):
		super().__init__(None, wx.ID_ANY, "Procon", pos=(100, 50))
		#ステージのインスタンス生成
		self.__Game = Game()
		gamePanels = self.__Game.getPanels()

		#コントローラのインスタンス生成
		#self.__Human1 = ControllerFrame(PlayerInfo("1P-1", "#ed1c24", "#f78e94"), PlayerInfo("1P-2", "#ff7f27", "#ffbe93"),None)
		#self.__Human2 = ControllerFrame(PlayerInfo("2P-1", "#22b14c", "#82e8a0"), PlayerInfo("2P-2", "#00a2e8", "#75d6ff"),None)
		self.__Human1 = ControllerFrame(PlayerInfo("1P-1", "#ed1c24", "#f78e94"), PlayerInfo("1P-2", "#ff7f27", "#ffbe93"), KA_31())
		self.__Human2 = ControllerFrame(PlayerInfo("2P-1", "#22b14c", "#82e8a0"), PlayerInfo("2P-2", "#00a2e8", "#75d6ff"), kerasDQNPlayer(2))

		self.__RootPanel = wx.Panel(self, wx.ID_ANY)
		self.__RootPanel.SetBackgroundColour("#1f1f1f")
		self.__Sizer = wx.BoxSizer(wx.VERTICAL)

		#ステージ・パネルを作成
		self.__StagePanel = self.StagePanel(self.__RootPanel, self.__Game.getPanels())
		self.__Sizer.Add(self.__StagePanel, 0, wx.ALIGN_CENTER|wx.ALL, border=15)

		#ポイント・パネルを作成
		self.__PointPanel = self.PointPanel(self.__RootPanel)
		self.__Sizer.Add(self.__PointPanel, 0, wx.GROW|wx.LEFT, border=50)
		
		#実行ボタンを作成
		ID_GO = wx.NewId()
		self.__ActionButton = wx.Button(self.__RootPanel, ID_GO, "実行", size=(80, 40))
		self.__Sizer.Add(self.__ActionButton, 0, wx.ALIGN_CENTER|wx.BOTTOM, border=15)
		self.Bind(wx.EVT_BUTTON, self.OnButton, id=ID_GO)

		# 一手戻すボタンを作成
		ID_REV = wx.NewId()
		self.__Revert1Button = wx.Button(self.__RootPanel, ID_REV, "一手戻す", size = (80, 40))
		self.__Sizer.Add(self.__Revert1Button, 0, wx.ALIGN_CENTER|wx.BOTTOM, border = 15)
		self.Bind(wx.EVT_BUTTON, self.Rev1Act, id = ID_REV)

		self.__RootPanel.SetSizer(self.__Sizer)
		self.__RootPanel.Fit()
		self.Update()
		self.Fit()
				
		self.__Human1.Show()
		self.__Human2.Show()

		self.__Human1.UpdateAIEvaluation(self.__Game)
		self.__Human2.UpdateAIEvaluation(self.__Game)

		#TEST
	def Rev1Act(self, e):
		self.__Game = self.__Game.rewindOneTurn()
		self.Update()

	def OnButton(self, e):
		Intentions1 = self.__Human1.GetIntentions()
		Intentions2 = self.__Human2.GetIntentions()
		self.__Game.action([Intentions1[0], Intentions1[1], Intentions2[0], Intentions2[1]])
		self.__Game.score()
		if self.__Game.endGame():
			Scores = self.__Game.getPoints()
			print("1PTileScore : "+str(Scores[0]))
			print("1PRegionScore : "+str(Scores[1]))
			print("2PTileScore : "+str(Scores[2]))
			print("2PRegionScore : "+str(Scores[3]))
			print("Winner : "+str(self.__Game.getWinner()))
			sys.exit()
		self.Update()

		self.__Human1.UpdateAIEvaluation(self.__Game)
		self.__Human2.UpdateAIEvaluation(self.__Game)

		self.__Human1.ResetIntentions()
		self.__Human2.ResetIntentions()

	def Update(self):
		self.__StagePanel.Update([self.__Game._1PAgents[0], self.__Game._1PAgents[1], self.__Game._2PAgents[0], self.__Game._2PAgents[1]], self.__Game.getPanels())
		self.__PointPanel.Update(self.__Game.getPoints())
		self.Refresh()