class Player():#人，AIの継承用クラス
	self._intention : [int, int] #2つのエージェントの動かし方

	def intention(self):#盤面の情報を渡して最適なAgentの動かし方を返す
		return self._Intention

	def getResult(self):#結果を渡す(学習に使う?)
		return