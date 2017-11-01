import random

class RandomAgent:
	#def __init__(self):
		#uuhhh
	def pick_random_move(self, list_of_possible_moves):
		tuple_1 = random.choice(list(list_of_possible_moves.move_list))
		tuple_2 = random.choice(list_of_possible_moves.move_list[tuple_1])

		move = (tuple_1,tuple_2)
		#print("MY MOVE IS", move)
		return move