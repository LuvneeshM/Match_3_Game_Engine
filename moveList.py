import copy

class MoveList(object):
	def __init__(self):
		self.move_list = { }
		self._iter_index = 0

	def __iter__(self):
		for m in self.move_list.keys():
			yield (m, self.move_list[m])

	def __str__(self):
		for m in self.move_list.keys():
			yield (m, self.move_list[m])

	def clone(self):
		deep_tmp = MoveList()
		deep_tmp.move_list = copy.deepcopy(self.move_list)
		return deep_tmp

	def to_string(self):
		for m in self.move_list.keys():
			for k in self.move_list[m]:
				print ("1: " + str(m) + " 2: " + str(k))

	def push(self, arg_1, arg_2):
		if(arg_1 not in self.move_list):
			if(arg_2 in self.move_list):
				if(arg_1 in self.move_list[arg_2]):
					return
				else:
					self.move_list[arg_1] = set()
			else:
				self.move_list[arg_1] = set()
		self.move_list[arg_1].add(arg_2)
		
	def does_move_exist(self, move_made):
		if move_made[0] in self.move_list:
			if move_made[1] in self.move_list[move_made[0]]:
				return True
		return False
