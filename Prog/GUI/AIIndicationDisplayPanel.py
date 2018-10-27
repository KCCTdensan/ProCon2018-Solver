import wx
from enum import Enum

class IndicationPosition(Enum):
	TOPRIGHT		= 1
	TOP			= 2
	TOPLEFT 		= 3
	RIGHT			= 4
	STOP			= 5
	LEFT			= 6
	BOTTOMRIGHT	= 7
	BOTTOM			= 8
	BOTTOMLEFT		= 9

class IndicationAction(Enum):
	MOVE		= 0
	TURN		= 1

def GetIndication(Intention: list) -> (IndicationPosition, IndicationAction):
	if (Intention[0] == 0) and (Intention[1] == 0): # 停留
		return (IndicationPosition.STOP, IndicationAction.MOVE)
	pos = IndicationPosition.STOP # 適当
	if Intention[0] == -1: # 左側
		if Intention[1] == -1: # 上
			pos = IndicationPosition.TOPLEFT
		elif Intention[1] == 1: # 下
			pos = IndicationPosition.BOTTOMLEFT
		else: # 左
			pos = IndicationPosition.LEFT
	elif Intention[0] == 1: # 右側
		if Intention[1] == -1: # 上
			pos = IndicationPosition.TOPRIGHT
		elif Intention[1] == 1: # 下
			pos = IndicationPosition.BOTTOMRIGHT
		else: # 右
			pos = IndicationPosition.RIGHT
	else: # 中心
		if Intention[1] == -1: # 上
			pos = IndicationPosition.TOP
		elif Intention[1] == 1: # 下
			pos = IndicationPosition.BOTTOM

	act = IndicationAction.MOVE
	if Intention[2] != 0:
		act = IndicationAction.TURN
	return (pos, act)

def GetIndicationJPStr(pos, act)  -> str:
	s = ""
	if act == IndicationAction.MOVE:
		s = "[動] "
	elif act == IndicationAction.TURN:
		s = "[返] "
	else:	
		s = "[?] "
	if pos == IndicationPosition.TOPRIGHT:
		return s + "右上"
	elif pos == IndicationPosition.TOP:
		return s + "上"
	elif pos == IndicationPosition.TOPLEFT:
		return s + "左上"
	elif pos == IndicationPosition.RIGHT:
		return s + "右"
	elif pos == IndicationPosition.STOP:
		return s + "留"
	elif pos == IndicationPosition.LEFT:
		return s + "左"
	elif pos == IndicationPosition.BOTTOMRIGHT:
		return s + "右下"
	elif pos == IndicationPosition.BOTTOM:
		return s + "下"
	elif pos == IndicationPosition.BOTTOMLEFT:
		return s + "左下"
	else:
		return s + "?"

def GetIndicationPlayingCardsInfoStr(pos, agtnum) -> str:
	s = ""
	if agtnum == 1:
		s = "黒"
	elif agtnum == 2:
		s = "赤"
	else:
		s = "?"
	# 壇(ステージ)側は上
	if pos == IndicationPosition.TOPRIGHT:
		return s + "9"
	elif pos == IndicationPosition.TOP:
		return s + "8"
	elif pos == IndicationPosition.TOPLEFT:
		return s + "7"
	elif pos == IndicationPosition.RIGHT:
		return s + "6"
	elif pos == IndicationPosition.STOP:
		return s + "5"
	elif pos == IndicationPosition.LEFT:
		return s + "4"
	elif pos == IndicationPosition.BOTTOMRIGHT:
		return s + "3"
	elif pos == IndicationPosition.BOTTOM:
		return s + "2"
	elif pos == IndicationPosition.BOTTOMLEFT:
		return s + "1"
	else:
		return s + "?"

class AIIndicationDisplayPanel(wx.Panel):
	def __init__(self, Parent: wx.Panel, AI):
		super().__init__(Parent, wx.ID_ANY)
		self.__Sizer = wx.BoxSizer(wx.VERTICAL)
		self.__IntentionText = wx.StaticText(self, wx.ID_ANY)
		self.__IntentionText.SetForegroundColour("#000000")
		self.__Sizer.Add(self.__IntentionText, 0, wx.GROW|wx.CENTER|wx.ALL, border = 20)
		self.SetBackgroundColour("#ffffff")
		self.SetSizer(self.__Sizer)
		self.Fit()
		self.__AI = AI

	def UpdateEvaluation(self, Game):
		Intentions = self.__AI.intention(Game)
		print(Intentions)
		(pos1, act1) = GetIndication(Intentions[0])
		(pos2, act2) = GetIndication(Intentions[1])
		agent1 = "1P: " + GetIndicationJPStr(pos1, act1) + "(" + GetIndicationPlayingCardsInfoStr(pos1, 1) + ")"
		agent2 = "2P: " + GetIndicationJPStr(pos2, act2) + "(" + GetIndicationPlayingCardsInfoStr(pos2, 2) + ")"
		self.__IntentionText.SetLabelText(agent1 + "    |    " + agent2)
