from tree import *
from board import Board
from datetime import datetime
import time

import copy
import math

class MCTSAgent():
	level = 0

	def __init__(self, ubcReplacementFunc):
		self.func = ubcReplacementFunc

	def getRootNode_VisitCount(self):
		return self.rootNode.get_visit_count()

	#board is current game board
	#will return the
	def find_next_move(self, board, current_move):
		tree = Tree(current_move)
		#get the root node
		self.rootNode = tree.get_root_node()
		#set the state of the board
		self.rootNode.get_state().set_board(board);

		#need way to find terminating condition
		self.end_time = 30
		start_time = time.time()
		elapsed = 0
		#while(elapsed < self.end_time):
		while (self.rootNode.get_visit_count() < 250):
			#pick the promising node
			
			promising_node = self.select_promising_node(self.rootNode)
			
			#expand that node
			#since game endless just check the level, if >= 20 dont expand
			#create the childs for that node
			self.expand_node(promising_node)
			
			#explore that node
			nodeToExplore = promising_node.get_random_child_node()
			
			#simulate 
			simulationResult = self.simulate_random_play(nodeToExplore)
			
			#propogate up
			self.back_propogation(nodeToExplore,simulationResult)
			
			nowTime = time.time()
			elapsed += (nowTime - start_time)
			start_time = nowTime
			#print("elapsed time", elapsed)
			

		#winner is root node with child with big score
		#winner_node = rootNode.get_child_with_max_score()
		winner_node = None
		max_ucb = float('-inf')
		for child in self.rootNode.childArray:
			# UCB1 = self.selectionFuntion(child.get_win_score(), child.get_visit_count(), self.rootNode.get_visit_count())
			UCB1 = self.selectionFuntion(child.get_win_score(), child.get_visit_count(), self.rootNode.get_visit_count(), len(self.child.state.board.possible_moves_to_make.move_list))
			
			#print("child_win_score",child.get_win_score())
			#print("child_visit_count", child.get_visit_count())
			#print("rootMan_visit_count", rootNode.get_visit_count())
			#print("move for current node",child.get_state().move)
			#print("UCB1", UCB1)
			#input("HIT ENTER")
			if UCB1 > max_ucb:
				max_ucb = UCB1
				winner_node = child
		#tree.set_root_node
		#tree.set_root(winner_node)
		#return the winning Board
		#print("move is",winner_node.get_state().move)
		#print("Root visit count: ", rootNode.get_visit_count())
		return winner_node.get_state().move

	def selectionFuntion(self,child_win_score, child_visit_count, current_visit_count):
		try:
			return self.func(child_win_score, child_visit_count, current_visit_count)
		except ZeroDivisionError:
			#python 3 doesnt have max int value....
			return float('inf')
		except ValueError:
			return float('inf')
		

	def UCB(self,child_win_score, child_visit_count, current_visit_count):
		if(child_visit_count == 0):
			#python 3 doesnt have max int value....
			return float('inf')
		UCB1 = (float(child_win_score)/float(child_visit_count)) + 1.414 * math.sqrt(2.0*math.log(current_visit_count)/float(child_visit_count))
		return UCB1

	def select_promising_node(self, rootNode):
		parentVisit = rootNode.get_visit_count()

		#check for children
		if(rootNode.get_child_array() == []):
			return rootNode

		currentNode = rootNode

		while currentNode.get_child_array() != []:
			best = 0
			best_node = None
			for child in currentNode.get_child_array():
				UCB1 = self.selectionFuntion(child.get_win_score(), child.get_visit_count(), currentNode.get_visit_count())
				#UCB1 = (child.get_win_score() / child.get_visit_count()) + 1.414 * math.sqrt(2.0 * math.log(currentNode.get_visit_count())/child.get_visit_count())
				if UCB1 > best or best_node == None:
					best = UCB1
					best_node = child
			currentNode = best_node


		return best_node

	def expand_node(self, promising_node):

		#IN TREE HELP WITH GETTING ALL POSSIBLE STATES 
		#get the node
		#get the state from that node
		#say these are all the possible states I can go to?
		possible_states = promising_node.get_state().get_all_possible_states()
		
		for state in possible_states:
			new_node = Node()
			new_node.set_state(state)
			new_node.set_parent(promising_node)
			new_node.increment_move_count(promising_node.get_move_count())
			new_node.my_move = state.move
			promising_node.get_child_array().append(new_node)


		pass

	def simulate_random_play(self, nodeToExplore):

		temp_copy = nodeToExplore.clone() #copy.deepcopy(nodeToExplore)

		#print("start score",temp_copy.get_state().get_board().points)

		while (temp_copy.get_move_count() < 20):
			temp_copy.get_state().randomPlay()
			temp_copy.increment_move_count(temp_copy.get_move_count())

		nodeToExplore.visit_count += 1
		if temp_copy.get_state().get_board().isWinner():
			nodeToExplore.win_score = nodeToExplore.win_score + 1

		#print("end score",temp_copy.get_state().get_board().points)

		return 1 if temp_copy.get_state().get_board().isWinner() else 0

	def back_propogation(self, nodeToExplore, win):
		parent = nodeToExplore
		
		while parent.parent != None:
			parent = parent.parent

			parent.visit_count += 1
			parent.win_score += win
