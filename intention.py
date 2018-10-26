class intention:
	def __init__(self):
		self.DeltaX = 0
		self.DeltaY = 0
	def __init(self,action_id:int):
		if(action_id >= 1 and action_id <= 3):
			self.DeltaY = -1
		elif(action_id >= 6 and action_id <= 8):
			self.DeltaY = 1
		else:
			self.DeltaY = 0

		if(action_id == 1 or action_id == 4 or action_id == 6):
			self.DeltaX = -1
		elif(action_id == 3 or action_id == 5 or action_id == 8):
			self.DeltaX = 1
		else:
			self.DeltaX = 0
