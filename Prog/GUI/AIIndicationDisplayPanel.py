import wx
from enum import Enum

class IndicationPosition(Enum):
	TopRight		= 1
	Top			= 2
	TopLeft 		= 3
	Right		= 4
	Stop		= 5
	Left			= 6
	BottomRight	= 7
	Bottom		= 8
	BottomLeft	= 9


class IndicationAction(Enum):
	Move		= 0
	Turn		= 1


def GetIndication(Intention: list) -> (IndicationPosition, IndicationAction):
	if (Intention[0] == 0) and (Intention[1] == 0):
		return (IndicationPosition.Stop, IndicationAction.Stop)

	pos = IndicationPosition.Stop
	if Intention[0] == -1: # 左側
		if Intention[1] == -1: # 上
			pos = IndicationPosition.TopLeft
		elif Intention[1] == 1: # 下
			pos = IndicationPosition.BottomLeft
		else: # 左
			pos = IndicationPosition.Left
	elif Intention[0] == 1: # 右側
		if Intention[1] == -1: # 上
			pos = IndicationPosition.TopRight
		elif Intention[1] == 1: # 下
			pos = IndicationPosition.BottomRight
		else: # 右
			pos = IndicationPosition.Right

	act = IndicationAction.Move
	if Intention[2] != 0:
		act = IndicationAction.Turn

	return (pos, act)


def GetIndicationJPStr(pos, act)  -> str:
	s = ""
	if act == IndicationAction.Move:
		s = "[動] "
	elif act == IndicationAction.Turn:
		s = "[返] "
	else:	
		s = "[?] "

	if pos == IndicationPosition.TopRight:
		return s + "右上"
	elif pos == IndicationPosition.Top:
		return s + "上"
	elif pos == IndicationPosition.TopLeft:
		return s + "左上"
	elif pos == IndicationPosition.Right:
		return s + "右"
	elif pos == IndicationPosition.Stop:
		return s + "留"
	elif pos == IndicationPosition.Left:
		return s + "左"
	elif pos == IndicationPosition.BottomRight:
		return s + "右下"
	elif pos == IndicationPosition.Bottom:
		return s + "下"
	elif pos == IndicationPosition.BottomLeft:
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
	if pos == IndicationPosition.TopRight:
		return s + "9"
	elif pos == IndicationPosition.Top:
		return s + "8"
	elif pos == IndicationPosition.TopLeft:
		return s + "7"
	elif pos == IndicationPosition.Right:
		return s + "6"
	elif pos == IndicationPosition.Stop:
		return s + "5"
	elif pos == IndicationPosition.Left:
		return s + "4"
	elif pos == IndicationPosition.BottomRight:
		return s + "3"
	elif pos == IndicationPosition.Bottom:
		return s + "2"
	elif pos == IndicationPosition.BottomLeft:
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
		(pos1, act1) = GetIndication(Intentions[0])
		(pos2, act2) = GetIndication(Intentions[1])

		agent1 = "1P: " + GetIndicationJPStr(pos1, act1) + GetIndicationPlayingCardsInfoStr(pos1, 1)
		agent2 = "2P: " + GetIndicationJPStr(pos2, act2) + GetIndicationPlayingCardsInfoStr(pos2, 2)

		self.__IntentionText.SetLabelText(agent1 + "    |    " + agent2)
