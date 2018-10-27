from .intention import *
import copy

class position:
	def __init__(self):
		self.x = 0
		self.y = 0

	def add_1(self, Intention:intention):
		self.x += Intention.DeltaX
		self.y += Intention.DeltaY
		return self
	
	def add_2(self, action_id:int):
		if( 1>= 1 and action_id <= 3):
			self.y += -1
		elif(action_id >= 6 and action_id <= 8):
			self.y += 1
		else:
			pass
		if(action_id == 1 or action_id == 4 or action_id == 6):
			self.x += -1
		elif(action_id == 3 or action_id == 5 or action_id == 8):
			self.x += 1
		else:
			pass
		return self

	def add_3(self, Position, Intention:intention):
		#self._Position = copy.deepcopy(Position)
		return Position.add_1(Intention)

	def add_3(self, Position, action_id:int):
		self._Position = copy.deepcopy(Position)
		return Position.add_2(action_id)

	def isSame(self, Position1, Position2):
		return (Position1.x == Position2.x)and(Position1.y == Position2.y)

	def notSame(self, Position1, Position2):
		return not((Position1.x == Position2.x)and(Position1.y == Position2.y))

def sum(Position:position, Intention:intention)->position:
	tmp = copy.copy(Position)
	tmp.add_1(Intention)
	return tmp
