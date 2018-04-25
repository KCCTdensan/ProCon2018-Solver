import tkinter as tk

from Game import *
from Window import *

def main():
	g = Game()
	root = tk.Tk()
	Window(master = root, Game = g)

	root.mainloop()

if __name__ == '__main__':
	main()