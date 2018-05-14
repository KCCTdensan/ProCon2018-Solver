import tkinter as tk
import tkinter.ttk as ttk

from Game import *

class Window(ttk.Frame):
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
		#self._Game.action([self.entry[0][0].get(), self.entry[0][1].get()], [self.entry[1][0].get(), self.entry[1][1].get()], [self.entry[2][0].get(), self.entry[2][1].get()], [self.entry[3][0].get(), self.entry[3][1].get()])
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