from tree import *
from board import Board
import time

class IDSAgent:
	def __init__(self, level):
		self.level = level

	def find_next_move(self, board, startLevel, endLevel):
		tree = Tree()
		#get the root node
		self.rootNode = tree.get_root_node()
		#set the state of the board
		self.rootNode.get_state().set_board(board);
		self.level = endLevel
		
		self.ids(self.rootNode, startLevel)

		max_score = self.rootNode.get_child_with_max_score().get_state().get_score()

	 	winner_node = None
	 	for child in self.rootNode.childArray:
	 		if(child.get_state().get_score() == max_score):
	 			winner_node = child

	 	print("max score {0} reached level {1} with move {2}".format(max_score, endLevel, winner_node.get_state().move))
	 	return (winner_node.get_state().move, winner_node.get_state().get_score())
	
	def expand_node(self, promising_node):
		possible_states = promising_node.get_state().get_all_possible_states()
		
		for state in possible_states:
			new_node = Node()
			new_node.set_state(state)
			new_node.set_parent(promising_node)
			new_node.increment_move_count(promising_node.get_move_count())
			new_node.my_move = state.move
			promising_node.get_child_array().append(new_node)

	def ids(self,nodeToExplore, currLevel):
		if(currLevel >= self.level):
			parent = nodeToExplore
		
			while parent.parent != None:
				if parent.get_state().get_score() > parent.parent.get_state().get_score():
					parent.parent.get_state().set_score(parent.get_state().get_score())
				parent = parent.parent

		if(currLevel < self.level):
			self.expand_node(nodeToExplore)
			currLevel += 1
			for child in nodeToExplore.childArray:
				self.ids(child, currLevel)
			
random.seed(2)
#board
board = Board(7,7)
board.init()
list_of_moves = board.possible_moves_to_make.move_list

#ids stuff
level_counter = 1
ids_ai = IDSAgent(level_counter)
#time stuff
elapsed = 0
end_time = 60*5
start_time = time.time()
while(elapsed < end_time):
	move_and_score = ids_ai.find_next_move(board, 0, level_counter)
	level_counter += 1
	elapsed = time.time()-start_time
	print("Elasped time is: {0}".format(elapsed))

print("IDS move is {0} with final score {1}".format(move_and_score[0], move_and_score[1]))
