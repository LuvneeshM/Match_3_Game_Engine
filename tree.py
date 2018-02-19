#For tree search part

from board import Board
import random
import copy

#each node has a particular state of the problem 
class State:
	def __init__(self):
		self.board = Board()
		self.score = 0
		#MoveList class object
		self.list_of_possible_moves = self.board.possible_moves_to_make
		self.move = None

	def clone(self):
		temp_deep = State()
		temp_deep.board = self.board.clone()
		temp_deep.score = self.score
		temp_deep.list_of_possible_moves = self.list_of_possible_moves.clone()
		temp_deep.move = copy.deepcopy(self.move)
		return temp_deep

	def get_all_possible_states(self):
		#list of all possible states from current state
		list_of_states = []
		#list_of_possible_moves.move_list is a dictionary
		#for every move, make a new state
		for tuple_1 in (self.list_of_possible_moves.move_list).keys():
			for tuple_2 in self.list_of_possible_moves.move_list[tuple_1]:
				temp_board = self.board.clone()
				#temp_board = copy.deepcopy(self.board)
				move_to_make = (tuple_1,tuple_2)
				temp_board.swap_positions(temp_board.board, move_to_make)
				temp_state = State()
				temp_state.set_score(temp_board.points)
				temp_state.board = temp_board
				temp_state.set_list_of_possible_moves()
				temp_state.move = move_to_make
				list_of_states.append(temp_state)

		return list_of_states

	def randomPlay(self):
		tuple_1 = random.choice(list(self.list_of_possible_moves.move_list))
		tuple_2 = random.choice(self.list_of_possible_moves.move_list[tuple_1])

		move = (tuple_1,tuple_2)
		self.board.swap_positions(self.board.board, move)
		self.list_of_possible_moves = self.board.possible_moves_to_make


	def get_board(self):
		return self.board

	def get_score(self):
		return self.score	

	def set_board(self, new_board):
		self.board = new_board
		self.set_list_of_possible_moves()

	def set_score(self, new_score):
		self.score = new_score

	def set_list_of_possible_moves(self):
		self.list_of_possible_moves = self.board.possible_moves_to_make


class Node:
	def __init__(self):
		#List<Node> childArray
		self.childArray = []
		self.state = State()
		#empty tuple
		#will hold (<tuple1>,<tuple2>)
		self.my_move = None
		#number of moves made
		#initally 0, take parents + 1
		self.win_score = 0
		self.visit_count = 0
		self.parent = None
		self.move_count = 0				

	def clone(self):
		temp_deep = Node()
		temp_deep.childArray = copy.deepcopy(self.childArray)
		temp_deep.state = self.state.clone()
		temp_deep.my_move = copy.deepcopy(self.my_move)
		temp_deep.win_score = copy.deepcopy(self.win_score)
		temp_deep.visit_count = copy.deepcopy(self.visit_count)
		temp_deep.parent = self.parent
		temp_deep.move_count = copy.deepcopy(self.move_count)
		return temp_deep

	def get_state(self):
		return self.state

	def get_child_array(self):
		return self.childArray
	

	def get_win_score(self):
		return self.win_score

	def get_random_child_node(self):
		if(len(self.childArray) == 0):
			print("child array 0")
			input("broken we are in tree get_random_child_node()")
		random_index = random.randint(0, len(self.childArray)-1)
		return self.childArray[random_index]

	def get_child_with_max_score(self):
		#returns the child with the largest State.score
		child_to_return = None
		max_score = 0
		for child in self.childArray:
			if child.state.score > max_score: 
				max_score = child.state.score
				child_to_return = child
				
		return child_to_return
		pass

	def get_visit_count(self):
		return self.visit_count

	def get_win_score(self):
		return self.win_score

	def get_move_count(self):
		return self.move_count	

	def set_parent(self, new_parent):
		self.parent = new_parent

	def set_state(self, new_state):
		self.state = new_state

	def set_visit_count(self, new_vc):
		self.visit_count = new_vc

	def increment_move_count(self, parent_move_count):
		self.move_count = parent_move_count + 1

	def set_move_count(self, parent_move_count):
		self.move_count = parent_move_count		

class Tree:
	def __init__(self):
		#Node root;
		self.root = Node()

	def get_root_node(self):
		return self.root

	def set_root(self, newRoot):
		self.root = newRoot
