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
		for i in range(len(Panels)):
			for j in range(len(Panels[0])):
				label = tk.Label(self.frame, text = str(Panels[i][j].getScore()), fg = color[Panels[i][j].getState()], relief = tk.RIDGE, bd = 2)
				label.grid(row = i, column = j)

		#意思表示入力ボックス
		self.frame2 = tk.LabelFrame(self, bd = 2, relief = "ridge", text="1P-1,1P-2,2P-1,2P-2")
		self.frame2.pack(fill = "x")
		self.entry1 = tk.Entry(self.frame2, font = ("",12), justify = "left", width = 20)
		self.entry1.pack()
		self.entry2 = tk.Entry(self.frame2, font = ("",12), justify = "left", width = 20)
		self.entry2.pack()
		self.entry3 = tk.Entry(self.frame2, font = ("",12), justify = "left", width = 20)
		self.entry3.pack()
		self.entry4 = tk.Entry(self.frame2, font = ("",12), justify = "left", width = 20)
		self.entry4.pack()
		self.button = tk.Button(self.frame2, text = "決定", font = ("", 12), width = 5, bg = "gray", command = self.push)
		self.button.pack()

	def push(self): #ボタンが押された際，エージェントの意思をGameに渡す
		print(self.entry1.get())
		print(self.entry2.get())
		print(self.entry3.get())
		print(self.entry4.get())
        #self._Game.action(self.entry1.get(), self.entry2.get(), self.entry3.get(), self.entry4.get())
		#self._Game.score()
		#GUIの更新
		self.entry1.delete(0, tk.END)
		self.entry2.delete(0, tk.END)
		self.entry3.delete(0, tk.END)
		self.entry4.delete(0, tk.END)