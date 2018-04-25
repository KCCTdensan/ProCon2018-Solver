import tkinter as tk
import tkinter.ttk as ttk

from Game import *

class Window(ttk.Frame):
	def __init__(self, master = None, Game = None): #GUI生成
		super().__init__(master)
		master.title("ProCon2018-Solver")
		master.geometry("1260x720")
		self._Game = Game
		self.pack()
		self.create_widgets()

	def create_widgets(self):
		#盤面

		#意思表示入力ボックス

		#quitボタン
		self.quit = tk.Button(self, text="QUIT", fg = "red", command = self.destroy)
		self.quit.pack(side="bottom")

	def input(): #エージェントの意思をGameに渡す
		self._Game.action()
		self._Game.score()

	def update(): #盤面を更新する
		pass
