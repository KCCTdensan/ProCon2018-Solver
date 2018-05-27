import wx
from Game import *
import Panel

class PlayerInfo:
	def __init__(self, Label:str, Color:str):
		self.Label = Label
		self.Color = Color
		
ID_BUTTON = []
ID_GO = 0
Players = (PlayerInfo("1P-1", "#00a2e8"), PlayerInfo("1P-2", "#3f48cc"), PlayerInfo("2P-1", "#ed1c24"), PlayerInfo("2P-2", "#b10e16"))

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
				self.SetBackgroundColour("#ffffff")
				font = wx.Font(30, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
				text = wx.StaticText(self, wx.ID_ANY, str(StagePanel.getScore()), style=wx.TE_CENTER)
				text.SetFont(font)
				self.sizerPanel.Add(text, flag=wx.GROW)
				self.SetSizer(self.sizerPanel)

		def __init__(self, Parent:wx.Panel, NumX:int, NumY:int, Panels:list):
			super().__init__(Parent, wx.ID_ANY)
			self.Panels = Panels
			self.listPanelPanel = []
			self.sizerStage = wx.GridSizer(rows=NumY, cols=NumX, gap=(0, 0))
			for iy in range(len(Panels)):
				self.listPanelPanel.append([])
				for ix in range(len(Panels[0])):
					self.listPanelPanel[iy].append(self.PanelPanel(self, Panels[iy][ix]))
					self.sizerStage.Add(self.listPanelPanel[iy][ix], 0, wx.GROW|wx.ALL, border=5)
			self.SetSizer(self.sizerStage)

		def Update(self, Positions:list):
			for iy in range(len(self.Panels)):
				for ix in range(len(self.Panels[0])):
					State = self.Panels[iy][ix].getState()
					if State == 0:
						self.listPanelPanel[iy][ix].SetBackgroundColour("#ffffff")
					elif State == 1:						
						self.listPanelPanel[iy][ix].SetBackgroundColour("#99d9ea")
					elif State == 2:						
						self.listPanelPanel[iy][ix].SetBackgroundColour("#ffaec9")
					for ip in range(len(Players)):
						Point = Positions[ip]._point
						if (Point[0] == ix)and(Point[1] == iy):
							pass

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
					ButtonCollection = ("左上", "上", "右上", "左", "留まる", "右", "左下", "下", "右下")
					self.Intention = [0, 0]
					self.listButton = []
					self.SelectColor = SelectColor
					self.sizerButton = wx.GridSizer(rows=3, cols=3, gap=(0, 0))
					for i in range(len(ButtonCollection)):
						ID.append(wx.NewId())
						self.listButton.append(wx.Button(self, ID[i], ButtonCollection[i], size=(50, 50)))
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
						b.SetForegroundColour("#000000")
					
			def __init__(self, Parent:wx.Panel, Label:str, SelectColor:str, ButtonID:list):
				super().__init__(Parent, wx.ID_ANY)
				self.textPlayer = wx.StaticText(self, wx.ID_ANY, Label, style=wx.TE_CENTER)
				self.panelButton = self.ButtonPanel(self, SelectColor, ButtonID)

				self.sizerPlayer = wx.BoxSizer(wx.VERTICAL)
				self.sizerPlayer.Add(self.textPlayer, 0, wx.GROW|wx.BOTTOM, border=10)
				self.sizerPlayer.Add(self.panelButton)
				self.SetSizer(self.sizerPlayer)

			def GetIntention(self)->list:
				return self.panelButton.GetIntention()

			def ResetIntention(self):
				self.panelButton.ResetIntention()

		def __init__(self, Parent:wx.Panel):
			super().__init__(Parent, wx.ID_ANY)
			self.listPanel = []

			self.sizerController = wx.BoxSizer(wx.HORIZONTAL)
			for i in range(len(Players)):
				ID_BUTTON.append([])
				self.listPanel.append(self.PlayerPanel(self, Players[i].Label, Players[i].Color, ID_BUTTON[i]))
				self.sizerController.Add(self.listPanel[i], 0, flag=wx.GROW|wx.ALL|wx.ALIGN_CENTER, border=20)
			self.SetSizer(self.sizerController)

		def GetIntentions(self)->list:
			return [self.listPanel[0].GetIntention(), self.listPanel[1].GetIntention(), self.listPanel[2].GetIntention(), self.listPanel[3].GetIntention()]

		def ResetIntentions(self):
			for p in self.listPanel:
				p.ResetIntention()

	def __init__(self):
		super().__init__(None, wx.ID_ANY, "Procon")
		self.game = Game()
		gamePanels = self.game.getPanels()
		ID_GO = wx.NewId()

		self.Center()
		self.SetBackgroundColour("#2f2f2f")
		self.SetSize((760, len(gamePanels)*50 + 300))

		self.rootPanel = wx.Panel(self, wx.ID_ANY)
		self.rootPanel.SetBackgroundColour("#afafaf")
		self.panelStage = self.StagePanel(self.rootPanel, len(gamePanels[0]), len(gamePanels), gamePanels)
		self.panelController = self.ControllerPanel(self.rootPanel)
		self.buttonAction = wx.Button(self.rootPanel, ID_GO, "実行", size=(80, 40))

		self.rootLayout = wx.BoxSizer(wx.VERTICAL)
		self.rootLayout.Add(self.panelStage, 0, wx.GROW)
		self.rootLayout.Add(self.panelController, 0, wx.GROW)
		self.rootLayout.Add(self.buttonAction, 0, wx.ALIGN_CENTER)
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
		self.panelStage.Update([self.game._1PAgents[0], self.game._1PAgents[1], self.game._2PAgents[0], self.game._2PAgents[1]])

"""class Window(ttk.Frame):
	def __init__(self, master = None, Game = None): #GUI生成
		super().__init__(master)
		master.title("ProCon2018-Solver")
		master.geometry("1260x720")
		self._Game = Game
		self.create_widgets()
		self.pack()

	def create_widgets(self):
		#盤面
		self.frame = tk.LabelFrame(self, bd = 2, relief = "ridge", text = "stage")
		self.frame.pack(fill = "x")
		color = {0:"black", 1:"red", 2:"blue"}
		Panels = self._Game.getPanels()
		self.label = [[0 for j in range(len(Panels[0]))] for i in range(len(Panels))]#self.label[i][j]
		for i in range(len(Panels)):
			for j in range(len(Panels[0])):
				self.label[i][j] = tk.Label(self.frame, relief = tk.RIDGE, bd = 2)
				self.label[i][j].grid(row = i, column = j)
		self.update()

		#意思表示入力ボックス
		self.frame2 = tk.LabelFrame(self, bd = 2, relief = "ridge", text="1P-1,1P-2,2P-1,2P-2")
		self.frame2.pack(fill = "x")
		self.entry = [[0 for j in range(2)]for i in range(4)]#self.entry[4][2]
		for i in range(4):
			for j in range(2):
				self.entry[i][j] = tk.Entry(self.frame2, font = ("",12), justify = "left", width = 20)
				self.entry[i][j].grid(row = i, column = j)

		self.button = tk.Button(self, text = "決定", font = ("", 12), width = 5, bg = "gray", command = self.push)
		self.button.pack()

	def push(self): #ボタンが押された際，エージェントの意思をGameに渡す
		print(self.entry[0][0].get())
		self._Game.action([[self.entry[0][0].get(), self.entry[0][1].get()], [self.entry[1][0].get(), self.entry[1][1].get()]], [[self.entry[2][0].get(), self.entry[2][1].get()], [self.entry[3][0].get(), self.entry[3][1].get()]])
		#self._Game.score()
		self.update()
		for i in range(4):
			for j in range(2):
				self.entry[i][j].delete(0, tk.END)
		
	def update(self): #GUIの更新
		color = {0:"black", 1:"red", 2:"blue"}
		Panels = self._Game.getPanels()
		for i in range(len(Panels)):
			for j in range(len(Panels[0])):
				self.label[i][j]["text"] = str(Panels[i][j].getScore())
				self.label[i][j]["fg"] = color[Panels[i][j].getState()]
		self._Game.score()
		print(self._Game._1Pscore)
		print(self._Game._2Pscore)
		print("/////////////")
"""