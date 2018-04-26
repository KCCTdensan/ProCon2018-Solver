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
		
		color = {0:"white", 1:"red", 2:"blue"}
		for i in range(12):
			for j in range(12):
				#Panel = self._Game.getPanels[i][j]
				#label = tk.Label(frame, text = Panel.getScore(), bg = color[Panel.getState()] relief = tk.RIDGE, bd = 2)
				label = tk.Label(self.frame,	text ="1", bg = color[0], relief = tk.RIDGE, bd = 2)
				label.grid(row = i, column = j)

		#意思表示入力ボックス
		self.entry = tk.Entry(self, font = ("",12), justify = "center", width = 20)
		self.entry.pack()
		self.button = tk.Button(self, text = "決定", font = ("", 12), width = 5, bg = "gray", command = self.push)
		self.button.pack()

	def push(self): #ボタンが押された際，エージェントの意思をGameに渡す
		print(self.entry.get())
		#self._Game.action(self.entry.get())
		#self._Game.score()
		#GUIの更新