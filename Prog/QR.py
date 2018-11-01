import os
from .Panel import *
from .Agent import *
from pyzbar.pyzbar import decode
from PIL import Image

class QR:
	def __init__(self):
		self.existQR = False
		image = 'QRCode.jpg' #QRコードの画像
		try:
			data = decode(Image.open(image))	#QRコードのデータ全体
		except FileNotFoundError:
			print("QRCode.jpgがないです")
			return
		self.existQR = True
		QRtext = str(data).split('\'')[1]	#QRコードのテキスト部分
		self._yLen = int(QRtext.split(':')[0].split(' ')[0])	#ステージの縦*横(_yLen*_xLen)
		self._xLen = int(QRtext.split(':')[0].split(' ')[1])
		Agentx = int(QRtext.split(':')[self._yLen+1].split(' ')[1])-1	#1Pの1人目のエージェントのx,y座標
		Agenty = int(QRtext.split(':')[self._yLen+1].split(' ')[0])-1
		self._1PAgents = [Agent([Agenty, Agentx],1),Agent([self._yLen - 1 - Agenty, self._xLen - 1 - Agentx],1)] #ステージに存在する1Pのエージェントのリスト
		self._2PAgents = [Agent([self._yLen - 1 - Agenty, Agentx],2),Agent([Agenty, self._xLen - 1 - Agentx],2)] #ステージに存在する2Pのエージェントのリスト
		self.Agents4 = [self._1PAgents[0], self._1PAgents[1], self._2PAgents[0], self._2PAgents[1]]
		self._Panels = [[Panel(0) for i in range(self._xLen)]for j in range(self._yLen)] #パネルの配列の作成
		#パネルのスコア設定
		for y in range(self._yLen):
			PanelsScores = QRtext.split(':')[y+1]
			for x in range(self._xLen):
				PanelScore = int(PanelsScores.split(' ')[x])
				self._Panels[y][x] = Panel(PanelScore)