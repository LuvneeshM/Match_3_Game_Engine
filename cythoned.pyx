import random
import copy
import time
import csv
import numpy as np
import uuid
import os, sys
from functools import partial
import marshal
import multiprocessing as mp
import types
import gmpy2
from datetime import datetime
import time
import math
import operator

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
    
class Board:
	winning_score = 3294.3275
	#player move will make a match 3
	#make the swap and update board, give points, etc
	#player move --> ((#,#), (#,#))
	def swap_positions(self, player_move):
		#get the positions
		first_pos = player_move[0]
		second_pos = player_move[1]
		
		temp_val = self.board[first_pos[0]][first_pos[1]]
		self.board[first_pos[0]][first_pos[1]] = self.board[second_pos[0]][second_pos[1]]
		self.board[second_pos[0]][second_pos[1]] = temp_val
		#update board stuff now
		self.find_matches(1, True, self.board)
		###print("SCORE",self.points)

	def isWinner(self):
		if(self.points >= Board.winning_score):
			return True
		else: return False

	'''
	STUFF BELOW DOES THE BACKEND STUFF AUTOMATICALLY
	'''
	def __init__(self, rows=0, cols=0):
		self.divisors = [3, 19, 43, 61, 163, 199]
		self.rows = rows
		self.cols = cols
		self.board = []
		self.board_two = []
		self.points = 0;
		self.award_points = {}
		self.set_up_award_points_dict()
		self.possible_moves_to_make = MoveList()
		self.found_match_before_game_start = False

	def clone(self):
		deep_tmp = Board(7,7)
		deep_tmp.board = copy.deepcopy(self.board)
		deep_tmp.points = copy.deepcopy(self.points)
		deep_tmp.award_points = copy.deepcopy(self.award_points)
		deep_tmp.possible_moves_to_make = self.possible_moves_to_make.clone()
		deep_tmp.board_two = copy.deepcopy(self.board_two)
		return deep_tmp
	
	def init(self):
		
		self.create_board()
		
		#print(self.board)

	def set_up_award_points_dict(self):
		self.award_points[3] = 0
		self.award_points[4] = 0
		self.award_points[5] = 0
		self.award_points[6] = 0
		self.award_points[7] = 0
		self.award_points[8] = 0
		self.award_points[9] = 0
		self.award_points[10] = 0
		self.award_points[11] = 0
		self.award_points[12] = 0
		self.award_points[13] = 0
		self.award_points[14] = 0
		self.award_points[15] = 0
		self.award_points[16] = 0
		self.award_points[17] = 0
		self.award_points[18] = 0
		self.award_points[19] = 0
		self.award_points[20] = 0
		self.award_points[21] = 0
		self.award_points[22] = 0
		self.award_points[23] = 0
		self.award_points[24] = 0
		self.award_points[25] = 0
		
	def create_board(self):
		#self.board = [[random.choice(self.divisors) for x in range(self.cols)] for y in range(self.rows)]
		
		self.board = np.array([[0 for x in range(self.cols)] for y in range(self.rows)])
		self.fill_board(self.board)
		# 		self.board = np.array(
		# [[ 3, 3, 3, 3, 3, 3, 3],
		#  [ 3, 3, 3, 3, 3, 3, 3],
		#  [ 3, 3, 3, 3, 3, 3, 3],
		#  [ 3, 3, 3, 3, 3, 3, 3],
		#  [ 3, 3, 3, 3, 3, 3, 3],
		#  [ 3, 3, 3, 3, 3, 3, 3],
		#  [ 3, 3, 3, 3, 3, 3, 3]]
		# )

		# 		self.board = np.array(
		# [[ 61, 199,  43,   3,  19,  61,  61],
		#  [ 61,  61, 163,  61, 199,  43,  19],
		#  [  3,   3,   3,  43,  61,  19, 199],
		#  [  3,  19,   3, 199, 199, 199, 199],
		#  [  3,   3,   3, 163, 199,   3, 199],
		#  [  3, 199,  61,  19, 199, 199, 199],
		#  [ 19,  61,  61, 199,   3,  61, 163]]
		# )
		# 		self.board = np.array(
		# [[ 61, 163,  43, 163, 163,  61, 199],
		#  [ 61,  61,  61,  61,   3,  19,  43],
		#  [ 61,  19, 199,   3,  43, 163,  19],
		#  [ 61,  61, 163,  61,  61,   3,   3],
		#  [163,   3, 199,  19, 163, 199,  43],
		#  [  3, 163,  61,  43,   3,  61,  19],
		#  [ 43,  43,   3,  19,  19,   3,   3]]
		# )

		# 		self.board = np.array(
		# [[ 61, 199,  43,   3,  19,  61,  61],
		#  [ 61, 199,  61,   3, 199,  43,  19],
		#  [  3,  43, 199,  43,  61,  19, 199],
		#  [ 43,  19,   3,   3,  61, 163,  19],
		#  [  3,  61, 163, 163, 199,   3,  43],
		#  [163, 199,  61,  19, 199, 199,  19],
		#  [ 19,  61,  61, 199,   3,  61, 163]]
		#  )
		self.board_two =  np.array([[0 for x in range(self.cols)] for y in range(self.rows)])
		self.fill_board_two(self.board_two)

		#check board for any pre matches before game starts
		self.find_matches(1, False, self.board)
		#print("SCORE",self.points)

	'''
	REAL STUFF BELOW 
	WILL DO EVERYTHING FUN 
	SIMPLY CALL
	self.find_matches(1, <BOOL>, board)
	'''
	
	def find_matches(self, multiplier, givePoints, board):
		# so this way works too
		#returns a dictionary 
		#key is a frozenset, of either just the horizontal or just the vertical matches
		#value is a frozenset of the vertical intsections
		possible_hell = self.get_sum_that_matter_hell_edition(board)
		# print(possible_hell)
		#there are no matches, no need to check any futher
		 
		# possible_vert_coll, possible_horizontal_coll = self.get_sum_that_matter(board)
		# print(board)
		# print("horizontal")
		# print(possible_horizontal_coll)
		# print("vertical")
		# print(possible_vert_coll)

		# #compare the two sets for intersections =
		# self.find_intersection(possible_vert_coll, possible_horizontal_coll, givePoints, board)
		# #now we check for normal 3, normal 4, normal 5 in a row
		# self.normal_vert_check(possible_vert_coll, givePoints, board)
		# self.normal_horiz_check(possible_horizontal_coll, givePoints, board)
		
		#only clean board if there matches
		if (possible_hell != {} ):		
			#clean the board of all sequences/matches
			self.check_for_intersection_and_horizontal_and_vertical(possible_hell, givePoints, board)

			self.add_new_pieces(board)
			#gave points, refill board
			if(sum(self.award_points.values()) > 0):
				pointsToAdd = self.user_gets_points()
				###print("adding", pointsToAdd * multiplier, "points\n")
				self.points = self.points + (pointsToAdd * multiplier)
				#print("POINTS ADDED", self.points)
				multiplier += 1
				if(pointsToAdd != 0):
					self.find_matches(multiplier, True, board)
			#make sure when clearing, no ne board has
			elif ( givePoints == False and self.found_match_before_game_start == True):
				self.found_match_before_game_start = False
				self.find_matches(multiplier, False, board) 
		
		#find the moves a player can make for the board (there are no more matches in this board)				
		#moves_made is a MoveList
		self.possible_moves_to_make = self.get_possible_moves(board)
		while (self.possible_moves_to_make.move_list == { }):
			self.random_board(board)
			self.possible_moves_to_make = self.get_possible_moves(board)

	def random_board(self, board):
		for x in range(self.cols): 
			for y in range(self.rows):
				board[x][y] = 0
		#board = np.array([[0 for x in range(self.cols)] for y in range(self.rows)])
		#print("random calling fill_board")
		self.fill_board(board)
		#print ("after filled")
		#print(board)
		return board

	#vertical sums that represent 3 or more of same item back to back in col
	#return possible_vert_coll
	#horizontal sums that represent 3 or more of same item back to back in row
	#return possible_horizontal_coll
	def get_sum_that_matter_hell_edition(self, board):
		possible_hell = {}

		prev_vert_sum_list = [ -1 for location in range(self.cols) ]
		for i in range(self.rows):
			prev_horiz_sum = -1
			for j in range(self.cols):		
				#horizontal
				if (j < self.cols-2):
					if(board[i][j] == board[i][j+1] and board[i][j] == board[i][j+2]):
						sum_in_horiz = board[i][j]+board[i][j+1]+board[i][j+2]

						if(prev_horiz_sum != sum_in_horiz):
							prev_horiz_sum = sum_in_horiz

							horizontal_sequ = set()
							horizontal_sequ.add((i,j))
							horizontal_sequ.add((i, j+1))
							horizontal_sequ.add((i, j+2))
							for x in range(j+3, self.cols):
								if board[i][x] == board[i][j]:
									horizontal_sequ.add((i, x))
								else:
									break
							possible_hell[frozenset(horizontal_sequ)] = set()

							# for k in self.divisors:
							# 	if(sum_in_horiz%k == 0 and sum_in_horiz/k == 3):
							# 		horizontal_sequ = set()
							# 		horizontal_sequ.add((i,j))
							# 		horizontal_sequ.add((i, j+1))
							# 		horizontal_sequ.add((i, j+2))
							# 		for x in range(j+3, self.cols):
							# 			if board[i][x] == k:
							# 				horizontal_sequ.add((i, x))
							# 			else:
							# 				break
							# 		possible_hell[frozenset(horizontal_sequ)] = set()
							# 		break

				#vertical
				if (i < self.rows-2):
					if(board[i][j] == board[i+1][j] and board[i][j] == board[i+2][j]):
						sum_in_vert = board[i][j]+board[i+1][j]+board[i+2][j]
					#i did not count this before
						if(prev_vert_sum_list[j] != sum_in_vert):
							prev_vert_sum_list[j] = sum_in_vert
							#check to see if (i, j) is in the keys for possible_hell
							#if it is, then just add to the values, this means there is an intersection
							#else, just do a frozenset key again
							vertical_seq = set()
							vertical_seq.add((i, j))
							vertical_seq.add((i+1,j))
							vertical_seq.add((i+2,j))
							recorded_intersection = False
							#check to ensure the next adj is not the same (for a match of 4, 5, etc)
							for x in range(i+3, self.rows):
								if board[x][j] == board[i][j]:
									vertical_seq.add((x, j))
								else:
									break
							for key in possible_hell.keys():
								if ( (i,j) in key ):
									possible_hell[key].update(vertical_seq)
									recorded_intersection = True
									break
							if (recorded_intersection == False):
								possible_hell[frozenset(vertical_seq)] = set()
							
		
		return possible_hell

	def check_for_intersection_and_horizontal_and_vertical(self, possible_hell, givePoints, board):
		for key, value in possible_hell.items():
			#if len(value) == 0, then that is not an intersection
			#treat is like normal, accounts for both vertical and horizontal
			#else, this is an intersection, iterate through both key and value
			if(len(value) == 0):
				number_of_pieces_to_del = len(key)
				if givePoints == True:
					self.award_points[number_of_pieces_to_del] += 1
				else: 
					self.found_match_before_game_start = True
			else:
				number_of_pieces_to_del = len(key) + len(value) - 1 #intersection position counted twice so -1
				if givePoints == True:
					self.award_points[number_of_pieces_to_del] += 1
				else: 
					self.found_match_before_game_start = True
			#clean board
			for position in key:
				board[position[0]][position[1]] = 0
			for position in value:
				board[position[0]][position[1]] = 0
	
	def get_sum_that_matter(self, board):
		possible_vert_coll = {}
		possible_horizontal_coll = {}

		prev_vert_sum_list = [ -1 for location in range(self.cols) ]
		for i in range(self.rows):
			prev_horiz_sum = -1
			for j in range(self.cols):		
				#horizontal
				if (j < self.cols-2):
					sum_in_horiz = board[i][j]+board[i][j+1]+board[i][j+2]

					if(prev_horiz_sum != sum_in_horiz):
						prev_horiz_sum = sum_in_horiz
						for k in self.divisors:
							if(sum_in_horiz%k == 0 and sum_in_horiz/k == 3):
								possible_horizontal_coll[(i,j)] = set()
								possible_horizontal_coll[(i,j)].add((i,j))
								possible_horizontal_coll[(i,j)].add((i,j+1))
								possible_horizontal_coll[(i,j)].add((i,j+2))
								for x in range(j+3, self.cols):
									if board[i][x] == k:
										possible_horizontal_coll[(i, j)].add((i, x))
									else:
										break
								break

				#vertical
				if (i < self.rows-2):
					sum_in_vert = board[i][j]+board[i+1][j]+board[i+2][j]
					if(prev_vert_sum_list[j] == sum_in_vert):
						#i already counted this guy, skip plz
						continue
					else:
						prev_vert_sum_list[j] = sum_in_vert
						for k in self.divisors:
							if(sum_in_vert%k == 0 and sum_in_vert/k == 3):
								possible_vert_coll[(i,j)] = set()
								possible_vert_coll[(i,j)].add((i,j))
								possible_vert_coll[(i,j)].add((i+1,j))
								possible_vert_coll[(i,j)].add((i+2,j))
								for x in range(i+3, self.rows):
									if board[x][j] == k:
										possible_vert_coll[(i, j)].add((x, j))
									else:
										break
								break
		
		return possible_vert_coll, possible_horizontal_coll

	# #vertical sums that represent 3 of same item back to back in col
	# #return possible_vert_coll
	# def get_vertical_sum_that_matter(self, sum_matrix, board):
	# 	possible_vert_coll = {}
	# 	for j in range(self.cols):
	# 		i = 0
	# 		while i < (self.rows - 2):
	# 			for k in self.divisors:

	# 				sum_in_vert = board[i][j]+board[i+1][j]+board[i+2][j]

	# 				if(sum_matrix[i][j]%k == 0 and sum_matrix[i][j]/k == 3):
	# 					possible_vert_coll[(i,j)] = set()
	# 					possible_vert_coll[(i,j)].add((i,j))
	# 					possible_vert_coll[(i,j)].add((i+1,j))
	# 					possible_vert_coll[(i,j)].add((i+2,j))
	# 					for x in range(i+3, self.rows):
	# 						if board[x][j] == k:
	# 							possible_vert_coll[(i, j)].add((x, j))
	# 							if x == self.rows - 1:
	# 								i = x
	# 						else:
	# 							i = x
	# 							break
	# 					break
	# 			i += 1

	# 	return possible_vert_coll

	# #horizontal sums that represent 3 of same item back to back in row
	# #return possible_horizontal_coll
	# def get_horizontal_sum_that_matter(self, sum_matrix, board):
	# 	possible_horizontal_coll = {}
	# 	for i in range(self.rows):
	# 		j = 0
	# 		while j < (self.cols - 2):
	# 			for k in self.divisors:
	# 				##print ("i: " + str(i))
	# 				##print ("j: " + str(j))

	# 				sum_in_horiz = board[i][j]+board[i][j+1]+board[i][j+2]

	# 				if(sum_matrix[i][j]%k == 0 and sum_matrix[i][j]/k == 3):
	# 					possible_horizontal_coll[(i,j)] = set()
	# 					possible_horizontal_coll[(i,j)].add((i,j))
	# 					possible_horizontal_coll[(i,j)].add((i,j+1))
	# 					possible_horizontal_coll[(i,j)].add((i,j+2))
	# 					for x in range(j+1, self.cols):
	# 						if board[i][x] == k:
	# 							possible_horizontal_coll[(i, j)].add((i, x))
	# 							if x == self.cols - 1:
	# 								j = x
	# 						else:
	# 							j = x
	# 							break
	# 					break
	# 			j += 1

	# 	return possible_horizontal_coll

	#looks for intersection between horizontal and vertical 
	#will be for 5 pieces
	def find_intersection(self, possible_vert_coll, possible_horizontal_coll, givePoints, board):
		#check for intersection between possible permutations and possible_vert_coll
		#if there is a coll, check to see if intersection in possible_hor_coll
		#if in both then you found intersection in game board
		delete_v_k_set = set()
		delete_h_k_set = set()
		for v_k in list(possible_vert_coll.keys()):
			for h_k in list(possible_horizontal_coll.keys()):
				intersection = possible_vert_coll[v_k].intersection(possible_horizontal_coll[h_k])
				if(intersection):
					number_of_pieces_to_del = 1
					lists_of_pairs_to_delete = possible_vert_coll[v_k].symmetric_difference(possible_horizontal_coll[h_k])
					for pairs_to_del in lists_of_pairs_to_delete:
						row = pairs_to_del[0]
						col = pairs_to_del[1]
						board[row][col] = 0
						number_of_pieces_to_del += 1
					board[list(intersection)[0][0]][list(intersection)[0][1]] = 0
					#get rid of the interesection place from the two sum matrices too
					delete_h_k_set.add(h_k)
					delete_v_k_set.add(v_k)
					# possible_horizontal_coll.pop(h_k)
					
					#player got points of the intersection --> 5
					#5, base value 40 * 5
					if givePoints == True:
						self.award_points[number_of_pieces_to_del] += 1
					else: 
						self.found_match_before_game_start = True
			
		for key in delete_v_k_set: 
			possible_vert_coll.pop(key)
		for key in delete_h_k_set:
			possible_horizontal_coll.pop(key)


	#normal check for vertical matches of 3,4,5,6...
	def normal_vert_check(self, possible_vert_coll, givePoints, board):
		consec_pieces = 2
		vertical_pos_to_del = set()
		for key_vert in possible_vert_coll:
			if givePoints == True:
				self.award_points[len(possible_vert_coll[key_vert])] += 1
			else: 
				self.found_match_before_game_start = True
			for val_vert in possible_vert_coll[key_vert]:
				vertical_pos_to_del.add(val_vert)
		#list of positions on game board to set to 0							
		for board_pos_to_del in vertical_pos_to_del:
			board[board_pos_to_del[0]][board_pos_to_del[1]] = 0
		
	#normal check for horizontal matches of 3,4,5,6...
	#possible_horizontal_coll is a dict
	def normal_horiz_check(self, possible_horizontal_coll, givePoints, board):
		consec_pieces = 2
		horizontal_pos_to_del = set()
		for key_hor in possible_horizontal_coll:
			if givePoints == True:
				self.award_points[len(possible_horizontal_coll[key_hor])] += 1
			else: 
				self.found_match_before_game_start = True
			for val_hor in possible_horizontal_coll[key_hor]:
				horizontal_pos_to_del.add(val_hor)
		#list of positions on game board to set to 0							
		for board_pos_to_del in horizontal_pos_to_del:
			board[board_pos_to_del[0]][board_pos_to_del[1]] = 0

	#board is updated
	#add new pieces
	def add_new_pieces(self, board):
		#first move pieces down
		self.drop_pieces(board)
		#now add pieces
		self.add_pieces(board)
		#refill board two
		self.fill_board_two(self.board_two)

	#in board drop board_one items down
	def drop_pieces(self, board):
		for col in range(self.cols):
			n = 6
			i = n-1
			#I am 0, find + give me guy above
			while(n >= 0):
				# print("INSIDE FIRST WHILE", n, i)
				if board[n][col] == 0:
					while(i >= 0):
						# print("SECOND WHILE", n, i)
						#found guy, "swap"
						if(board[i][col] > 0):
							# print("SWAP EM")
							board[n][col] = board[i][col]
							board[i][col] = 0
							n -= 1
						i -= 1
				else:
					# print("N NOT A ZERO")
					n -= 1
					if(n <= i):
						i = n-1
				if (i < 0):
					break
		# droppingAmountMaxtrix = [[0 for x in range(self.cols)] for y in range(self.rows)] 
		# #figure out which to drop and by how much 
		# for x in range(self.rows-1)[::-1]:
		# 	for y in range(self.cols)[::-1]:
		# 		if board[x][y] == 0 and board[x+1][y] == 0:
		# 			droppingAmountMaxtrix[x][y] = droppingAmountMaxtrix[x+1][y] + 1
		# 		elif board[x][y] == 0 and board[x+1][y] != 0:
		# 			droppingAmountMaxtrix[x][y] = droppingAmountMaxtrix[x+1][y]
		# 		elif board[x][y] != 0 and board[x+1][y] == 0: 
		# 			droppingAmountMaxtrix[x][y] = droppingAmountMaxtrix[x+1][y] + 1
		# 		elif board[x][y] != 0 and board[x+1][y] != 0:
		# 			droppingAmountMaxtrix[x][y] = droppingAmountMaxtrix[x+1][y]

		# #update board to drop things
		# for x in range(len(droppingAmountMaxtrix))[::-1]:
		# 	for y in range(len(droppingAmountMaxtrix[x]))[::-1]:
		# 		#only care about the non empty spots
		# 		if board[x][y] != 0:
		# 			#only care about the non empty spots that move
		# 			if droppingAmountMaxtrix[x][y] != 0:
		# 				dropping = droppingAmountMaxtrix[x][y]
		# 				board[x+dropping][y] = board[x][y]
		# 				board[x][y] = 0
	
	#add news numbers to the empty stuff on the top parts of the board	
	def add_pieces(self, board):
		#add new numbers to board
		#add to these spots
		num_pieces_per_col = [0 for x in range(self.cols)]
		for x in range(self.rows):
			for y in range(self.cols):
				if board[x][y] == 0:
					num_pieces_per_col[y] += 1 
		#actually add the pieces from second board
		for x in range(self.cols):
			y = num_pieces_per_col[x]-1
			board_two_row = self.rows-1
			while y >= 0:
				board[y][x] = self.board_two[board_two_row][x]
				self.board_two[board_two_row][x] = 0
				board_two_row -= 1
				y -= 1

	#refills the top of board two
	#IF starting fresh game, used to fill board_one for the first time
	def fill_board(self, board):
		#add to these spots
		num_pieces_per_col = [0 for x in range(self.cols)]
		#count number of 0 in each col
		for x in range(self.rows):
			for y in range(self.cols):
				if board[x][y] == 0:
					num_pieces_per_col[y] += 1 
		#fill exmpty spots in 2nd board
		for x in range(self.cols):
			y = num_pieces_per_col[x]-1
			while y >= 0:
				board[y][x] = random.choice(self.divisors)
				y -= 1
		#rig board so that no groups of 3 in 2nd board
		for x in range(0, self.rows):
			for y in range(0, self.cols):
				if y < (num_pieces_per_col[x]):
					#vertical groups
					if x < self.rows-1:# and x > 0:
						while board[x][y] == board[x-1][y] and board[x][y] == board[x+1][y]:
							board[x+1][y] = random.choice(self.divisors)
					#horizontal
					if(y < self.cols-1):
						while board[x][y-1] == board[x][y] and board[x][y] == board[x][y+1]:
							board[x][y+1] = random.choice(self.divisors)
		#print("fill board")
		#print(board)
	#after taking from board_Two
	#we update the board down and fill in the stuff on the top
	def fill_board_two(self, board):
		for col in range(self.cols):
			n = 6
			i = n-1
			#I am 0, find + give me guy above
			while(n >= 0):
				if board[n][col] == 0:
					while(i >= 0):
						#found guy, "swap"
						if(board[i][col] > 0):
							board[n][col] = board[i][col]
							board[i][col] = 0
							n -= 1
						i -= 1
				else:
					n -= 1
					if(n <= i):
						i = n-1
				if (i < 0):
					break

		# droppingAmountMaxtrix = [[0 for x in range(self.cols)] for y in range(self.rows)] 
		# #find how much to drop 
		# for x in range(self.rows-1)[::-1]: #5,4,3,2,1,0
		# 	for y in range(self.cols)[::-1]:
		# 		if board[x][y] == 0 and board[x+1][y] == 0:
		# 			droppingAmountMaxtrix[x][y] = droppingAmountMaxtrix[x+1][y] + 1
		# 		elif board[x][y] == 0 and board[x+1][y] != 0:
		# 			droppingAmountMaxtrix[x][y] = droppingAmountMaxtrix[x+1][y]
		# 		elif board[x][y] != 0 and board[x+1][y] == 0: 
		# 			droppingAmountMaxtrix[x][y] = droppingAmountMaxtrix[x+1][y] + 1
		# 		elif board[x][y] != 0 and board[x+1][y] != 0:
		# 			droppingAmountMaxtrix[x][y] = droppingAmountMaxtrix[x+1][y]
		# #drop em
		# for x in range(len(droppingAmountMaxtrix))[::-1]:
		# 	for y in range(len(droppingAmountMaxtrix[x]))[::-1]:
		# 		#only care about the non empty spots
		# 		if board[x][y] != 0:
		# 			#only care about the non empty spots that move
		# 			if droppingAmountMaxtrix[x][y] != 0:
		# 				dropping = droppingAmountMaxtrix[x][y]
		# 				board[x+dropping][y] = board[x][y]
		# 				board[x][y] = 0
		self.fill_board(board)

	#user gets their points 
	#also will reset that award_points[i] back to 0
	def user_gets_points(self):
		total_points_earned = 0
		base_value = 20
		for i in (self.award_points):
			#print(i,self.award_points[i])
			total_points_earned += i * base_value * self.award_points[i]
			self.award_points[i] = 0
			base_value += 10
		return total_points_earned

	#returns all moves that makes a match
	#returns a MoveList()
	def get_possible_moves(self, board):
		###print((board))

		list_of_moves_class = MoveList()

		#check for possible match 3 moves
		for x in range(self.rows):
			for y in range(self.cols):

				if (x < self.rows-3) and not (board[x+1][y] == board[x+2][y]):
					# window_4_row = ([board[x][y], board[x+1][y], board[x+2][y], board[x+3][y]])
					start_row_val = board[x][y]
					# result_swap = [1 if window_4_row[m] - start_row_val == 0 else 0 for m in range(len(window_4_row))]
					result_swap = ([1, 1 if board[x+1][y] - start_row_val == 0 else 0, 1 if board[x+2][y] - start_row_val == 0 else 0, 1 if board[x+3][y] - start_row_val == 0 else 0 ])
					if(sum(result_swap) == 3):
						if(result_swap[1] == 0):
							swap_1 = (x,y)
							swap_2 = (x+1,y)
							list_of_moves_class.push(swap_1,swap_2)

						else:
							swap_1 = (x+2,y)
							swap_2 = (x+3,y)			
							list_of_moves_class.push(swap_1,swap_2)
				if (y < self.cols-3) and not (board[x][y+1] == board[x][y+2]):
					# window_4_col = ([board[x][y], board[x][y+1], board[x][y+2], board[x][y+3]])
					start_col_value = board[x][y]
					# result_swap = [1 if window_4_col[m] - start_col_value == 0 else 0 for m in range(len(window_4_col))]
					result_swap = ([1, 1 if board[x][y+1] - start_col_value == 0 else 0, 1 if board[x][y+2] - start_col_value == 0 else 0, 1 if board[x][y+3] - start_col_value == 0 else 0 ])
					if(sum(result_swap) == 3):
						if(result_swap[1] == 0):
							swap_1 = (x,y)
							swap_2 = (x,y+1)
							list_of_moves_class.push(swap_1,swap_2)
							
						else:
							swap_1 = (x,y+2)
							swap_2 = (x,y+3)
							list_of_moves_class.push(swap_1,swap_2)
				

				center_of_window_value = board[x][y]
				total = 0
				#top row guys
				if x == 0 and y != 0 and y < (self.cols-1):
					# total += (1 if board[x-1][y-1] - center_of_window_value == 0 else 0) * (2**8) 0 
					# total += (1 if board[x-1][y  ] - center_of_window_value == 0 else 0) * (2**7) 0 
					# total += (1 if board[x-1][y+1] - center_of_window_value == 0 else 0) * (2**6) 0
					total += (1 if board[x  ][y-1] - center_of_window_value == 0 else 0) * (2**5)
					total += (1) * (2**4)
					total += (1 if board[x  ][y+1] - center_of_window_value == 0 else 0) * (2**3)
					total += (1 if board[x+1][y-1] - center_of_window_value == 0 else 0) * (2**2)
					total += (1 if board[x+1][y  ] - center_of_window_value == 0 else 0) * (2**1)
					total += (1 if board[x+1][y+1] - center_of_window_value == 0 else 0) * (2**0)
					# window = [
					# 			[0, 0, 0], 
					# 			[1 if board[x  ][y-1] - center_of_window_value == 0 else 0, 1                                                      , 1 if board[x  ][y+1] - center_of_window_value == 0 else 0 ],
					# 			[1 if board[x+1][y-1] - center_of_window_value == 0 else 0, 1 if board[x+1][y] - center_of_window_value == 0 else 0, 1 if board[x+1][y+1] - center_of_window_value == 0 else 0 ]
					# 		 ]
					
					# window = np.insert((board)[x:x+2, y-1:y+2], 0, [0, 0, 0], axis=0)
				#left guy
				elif x != 0 and y == 0 and x < (self.rows-1):
					# total += (1 if board[x-1][y-1] - center_of_window_value == 0 else 0) * (2**8) 0
					total += (1 if board[x-1][y  ] - center_of_window_value == 0 else 0) * (2**7)
					total += (1 if board[x-1][y+1] - center_of_window_value == 0 else 0) * (2**6)
					# total += (1 if board[x  ][y-1] - center_of_window_value == 0 else 0) * (2**5) 0
					total += (1) * (2**4)
					total += (1 if board[x  ][y+1] - center_of_window_value == 0 else 0) * (2**3)
					# total += (1 if board[x+1][y-1] - center_of_window_value == 0 else 0) * (2**2) 0
					total += (1 if board[x+1][y  ] - center_of_window_value == 0 else 0) * (2**1)
					total += (1 if board[x+1][y+1] - center_of_window_value == 0 else 0) * (2**0)
					# window = [
					# 			[0                                                       , 1 if board[x-1][y] - center_of_window_value == 0 else 0, 1 if board[x-1][y+1] - center_of_window_value == 0 else 0 ],
					# 			[0                                                       , 1                                                      , 1 if board[x  ][y+1] - center_of_window_value == 0 else 0 ],
					# 			[0                                                       , 1 if board[x+1][y] - center_of_window_value == 0 else 0, 1 if board[x+1][y+1] - center_of_window_value == 0 else 0 ]
					# 		 ]
					
					# window = np.insert((board)[x-1:x+2, y:y+2], 0, [0, 0, 0], axis=1)
				#last guy break
				elif (x == (self.rows-1) and y == (self.cols-1)) or (x == 0 and y == 0) or (x == 0 and y == self.cols-1) or (x == self.rows-1 and y == 0):
					#there_is_a_window = False
					continue
				#x-1->x+1, y-1-<y+1
				else:
					if y == (self.cols-1) and x != (self.rows-1):
						total += (1 if board[x-1][y-1] - center_of_window_value == 0 else 0) * (2**8)
						total += (1 if board[x-1][y  ] - center_of_window_value == 0 else 0) * (2**7)
						# total += (1 if board[x-1][y+1] - center_of_window_value == 0 else 0) * (2**6) 0
						total += (1 if board[x  ][y-1] - center_of_window_value == 0 else 0) * (2**5)
						total += (1) * (2**4)
						# total += (1 if board[x  ][y+1] - center_of_window_value == 0 else 0) * (2**3) 0
						total += (1 if board[x+1][y-1] - center_of_window_value == 0 else 0) * (2**2) 
						total += (1 if board[x+1][y  ] - center_of_window_value == 0 else 0) * (2**1) 
						# total += (1 if board[x+1][y+1] - center_of_window_value == 0 else 0) * (2**0) 0
						# window = [
						# 			[1 if board[x-1][y-1] - center_of_window_value == 0 else 0, 1 if board[x-1][y] - center_of_window_value == 0 else 0, 0],
						# 			[1 if board[x  ][y-1] - center_of_window_value == 0 else 0, 1                                                      , 0],
						# 			[1 if board[x+1][y-1] - center_of_window_value == 0 else 0, 1 if board[x+1][y] - center_of_window_value == 0 else 0, 0]
						# 		 ]
					elif y != (self.cols-1) and x == (self.rows-1):
						total += (1 if board[x-1][y-1] - center_of_window_value == 0 else 0) * (2**8)
						total += (1 if board[x-1][y  ] - center_of_window_value == 0 else 0) * (2**7)
						total += (1 if board[x-1][y+1] - center_of_window_value == 0 else 0) * (2**6) 
						total += (1 if board[x  ][y-1] - center_of_window_value == 0 else 0) * (2**5)
						total += (1) * (2**4)
						total += (1 if board[x  ][y+1] - center_of_window_value == 0 else 0) * (2**3) 
						# total += (1 if board[x+1][y-1] - center_of_window_value == 0 else 0) * (2**2) 0
						# total += (1 if board[x+1][y  ] - center_of_window_value == 0 else 0) * (2**1) 0
						# total += (1 if board[x+1][y+1] - center_of_window_value == 0 else 0) * (2**0) 0
						# window = [
						# 			[1 if board[x-1][y-1] - center_of_window_value == 0 else 0, 1 if board[x-1][y] - center_of_window_value == 0 else 0, 1 if board[x-1][y+1] - center_of_window_value == 0 else 0],
						# 			[1 if board[x  ][y-1] - center_of_window_value == 0 else 0, 1                                                      , 1 if board[x  ][y+1] - center_of_window_value == 0 else 0],
						# 			[0, 0, 0]
						# 		 ]
					elif y == (self.cols-1) and x == (self.rows-1):
						total += (1 if board[x-1][y-1] - center_of_window_value == 0 else 0) * (2**8)
						total += (1 if board[x-1][y  ] - center_of_window_value == 0 else 0) * (2**7)
						# total += (1 if board[x-1][y+1] - center_of_window_value == 0 else 0) * (2**6) 0
						total += (1 if board[x  ][y-1] - center_of_window_value == 0 else 0) * (2**5)
						total += (1) * (2**4)
						# total += (1 if board[x  ][y+1] - center_of_window_value == 0 else 0) * (2**3) 0
						# total += (1 if board[x+1][y-1] - center_of_window_value == 0 else 0) * (2**2) 0
						# total += (1 if board[x+1][y  ] - center_of_window_value == 0 else 0) * (2**1) 0
						# total += (1 if board[x+1][y+1] - center_of_window_value == 0 else 0) * (2**0) 0
						# window = [
						# 			[1 if board[x-1][y-1] - center_of_window_value == 0 else 0, 1 if board[x-1][y] - center_of_window_value == 0 else 0, 0],
						# 			[1 if board[x  ][y-1] - center_of_window_value == 0 else 0, 1                                                      , 0],
						# 			[0, 0, 0]
						# 		 ]

						# window = np.insert((board)[x-1:x+1, y-1:y+1], 2, [0, 0], axis=1)
						# window = np.insert(window, 2, [0, 0, 0], axis=0)
					else:
						total += (1 if board[x-1][y-1] - center_of_window_value == 0 else 0) * (2**8)
						total += (1 if board[x-1][y  ] - center_of_window_value == 0 else 0) * (2**7)
						total += (1 if board[x-1][y+1] - center_of_window_value == 0 else 0) * (2**6)
						total += (1 if board[x  ][y-1] - center_of_window_value == 0 else 0) * (2**5)
						total += (1) * (2**4)
						total += (1 if board[x  ][y+1] - center_of_window_value == 0 else 0) * (2**3)
						total += (1 if board[x+1][y-1] - center_of_window_value == 0 else 0) * (2**2)
						total += (1 if board[x+1][y  ] - center_of_window_value == 0 else 0) * (2**1)
						total += (1 if board[x+1][y+1] - center_of_window_value == 0 else 0) * (2**0)
						# window = [
						# 			[1 if board[x-1][y-1] - center_of_window_value == 0 else 0, 1 if board[x-1][y] - center_of_window_value == 0 else 0, 1 if board[x-1][y+1] - center_of_window_value == 0 else 0],
						# 			[1 if board[x  ][y-1] - center_of_window_value == 0 else 0, 1                                                      , 1 if board[x  ][y+1] - center_of_window_value == 0 else 0],
						# 			[1 if board[x+1][y-1] - center_of_window_value == 0 else 0, 1 if board[x+1][y] - center_of_window_value == 0 else 0, 1 if board[x+1][y+1] - center_of_window_value == 0 else 0 ]
						# 		 ]
						
						# window = (board)[x-1:x+2, y-1:y+2]

				# center_of_window_value = board[x][y]
				# result = [[1 if window[m][n] - center_of_window_value == 0 else 0 for n in range(len(window[m]))] for m in range(len(window))]
				# self.check_window(result, x,y, list_of_moves_class)
				if gmpy2.popcount(total) >= 3:
					self.check_window(total, x,y, list_of_moves_class)


		return list_of_moves_class

	#check for match with window
	def check_window(self, total, center_of_window_x, center_of_window_y, list_of_moves_class):
		# total = 0
		# exp = 8
		# for  i in range(len(window)):
		# 	for j in range(len(window[i])):
		# 		total += window[i][j] * (2**exp)
		# 		exp -= 1

		total_shift_left_1 = total << 1
		total_shift_left_2 = total << 2
		total_shift_left_3 = total << 3
		total_shift_left_4 = total << 4
		total_shift_right_1 = total >> 1
		total_shift_right_2 = total >> 2
		total_shift_right_3 = total >> 3
		total_shift_right_4 = total >> 4

		#x = row; y = col

		'''
		1 0 1
		0 1 0
		0 0 0
		'''
		if(total & total_shift_right_2 & total_shift_right_4 & 16):
			swap_1 = (center_of_window_x-1, center_of_window_y)
			swap_2 = (center_of_window_x, center_of_window_y)

			list_of_moves_class.push(swap_1,swap_2)

		'''
		1 0 0
		0 1 1
		0 0 0
		'''
		if(total & total_shift_right_4 & total_shift_left_1 & 16):
			swap_1 = (center_of_window_x-1, center_of_window_y-1)
			swap_2 = (center_of_window_x, center_of_window_y-1)

			list_of_moves_class.push(swap_1,swap_2)

			
			#APPEND MOVE (X, Y) -> left | (x, y) -> right | (x, y) -> up | (x, y) -> down
		'''
		1 0 0
		0 1 0
		1 0 0
		'''
		if(total & total_shift_right_4 & total_shift_left_2 & 16):
			swap_1 = (center_of_window_x, center_of_window_y-1)
			swap_2 = (center_of_window_x, center_of_window_y)

			list_of_moves_class.push(swap_1,swap_2)

			
		'''
		1 0 0
		0 1 0
		0 1 0
		'''
		if(total & total_shift_right_4 & total_shift_left_3 & 16):
			swap_1 = (center_of_window_x-1, center_of_window_y)
			swap_2 = (center_of_window_x-1, center_of_window_y-1)

			list_of_moves_class.push(swap_1,swap_2)

			
		'''
		0 1 0
		0 1 0
		1 0 0
		'''
		if(total & total_shift_right_3 & total_shift_left_2 & 16):
			swap_1 = (center_of_window_x+1, center_of_window_y)
			swap_2 = (center_of_window_x+1, center_of_window_y-1)

			list_of_moves_class.push(swap_1,swap_2)

			
		'''
		0 1 0
		0 1 0
		0 0 1
		'''
		if(total & total_shift_right_3 & total_shift_left_4 & 16):
			swap_1 = (center_of_window_x+1, center_of_window_y)
			swap_2 = (center_of_window_x+1, center_of_window_y+1)

			list_of_moves_class.push(swap_1,swap_2)
		
		'''
		0 0 1
		1 1 0
		0 0 0
		'''
		######
		if(total & total_shift_right_2 & total_shift_right_1 & 16):
			swap_1 = (center_of_window_x-1, center_of_window_y+1)
			swap_2 = (center_of_window_x, center_of_window_y+1)

			list_of_moves_class.push(swap_1,swap_2)

		'''
		0 0 1
		0 1 0
		0 1 0
		'''
		if(total & total_shift_right_2 & total_shift_left_3 & 16):
			swap_1 = (center_of_window_x-1, center_of_window_y)
			swap_2 = (center_of_window_x-1, center_of_window_y+1)

			list_of_moves_class.push(swap_1,swap_2)

		'''
		0 0 1
		0 1 0
		0 0 1
		'''
		if(total & total_shift_right_2 & total_shift_left_4 & 16):
			swap_1 = (center_of_window_x, center_of_window_y)
			swap_2 = (center_of_window_x, center_of_window_y+1)

			list_of_moves_class.push(swap_1,swap_2)

		'''
		0 0 0
		1 1 0
		0 0 1
		'''
		if(total & total_shift_right_1 & total_shift_left_4 & 16):
			swap_1 = (center_of_window_x, center_of_window_y+1)
			swap_2 = (center_of_window_x+1, center_of_window_y+1)

			list_of_moves_class.push(swap_1,swap_2)

		'''
		0 0 0
		0 1 1
		1 0 0
		'''
		if(total & total_shift_left_1 & total_shift_left_2 & 16):
			swap_1 = (center_of_window_x, center_of_window_y-1)
			swap_2 = (center_of_window_x+1, center_of_window_y-1)

			list_of_moves_class.push(swap_1,swap_2)

		'''
		0 0 0
		0 1 0
		1 0 1
		'''
		if(total & total_shift_left_2 & total_shift_left_4 & 16):
			swap_1 = (center_of_window_x, center_of_window_y)
			swap_2 = (center_of_window_x+1, center_of_window_y)

			list_of_moves_class.push(swap_1,swap_2)

		###print(total & total_shift_right_2 & total_shift_right_4 & 16)
		###print(total & total_shift_right_4 & total_shift_left_2 & 16)
		###print(total & total_shift_right_4 & total_shift_left_3 & 16)
		###print(total & total_shift_right_3 & total_shift_left_2 & 16)
		###print(total & total_shift_right_3 & total_shift_left_4 & 16)
		###print(total & total_shift_right_2 & total_shift_right_1 & 16)
		###print(total & total_shift_right_2 & total_shift_left_3 & 16)
		###print(total & total_shift_right_2 & total_shift_left_4 & 16)
		###print(total & total_shift_right_1 & total_shift_left_4 & 16)
		###print(total & total_shift_left_1 & total_shift_left_2 & 16)
		###print(total & total_shift_left_2 & total_shift_left_4 & 16)
		

	#future state of board
	def sim_next_state(self,move_made):
		self.swap_positions(move_made)

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
				# print("Board in Main after sht happens")
				#print(temp_board.board)
				# print(self.list_of_possible_moves.move_list)
				# print(move_to_make)
				temp_board.swap_positions(move_to_make)
				temp_state = State()
				temp_state.set_score(temp_board.points)
				temp_state.board = temp_board
				temp_state.set_list_of_possible_moves()
				temp_state.move = move_to_make
				list_of_states.append(temp_state)

		return list_of_states

	def randomPlay(self):
		tuple_1 = random.choice(list(self.list_of_possible_moves.move_list))
		tuple_2 = random.choice(list(self.list_of_possible_moves.move_list[tuple_1]))

		move = (tuple_1,tuple_2)
		self.board.swap_positions(move)
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
			if child.get_win_score > max_score: 
				max_score = child.get_win_score
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

class MCTSAgent():
	level = 0

	def __init__(self, ubcReplacementFunc):
		self.func = ubcReplacementFunc

	def getRootNode_VisitCount(self):
		return self.rootNode.get_visit_count()

	#board is current game board
	#will return the
	def find_next_move(self, board):
		tree = Tree()
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
			UCB1 = self.selectionFuntion(child.get_win_score(), child.get_visit_count(), self.rootNode.get_visit_count())
			# UCB1 = self.selectionFuntion(child.get_win_score(), child.get_visit_count(), self.rootNode.get_visit_count(), len(self.child.state.board.possible_moves_to_make.move_list))
			
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
			#return self.func(child_win_score, child_visit_count, current_visit_count)
			return self.UCB(child_win_score, child_visit_count, current_visit_count)
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

def makeMove():
	valid_move_made = False
	input_valid_move = False
	while input_valid_move == False:
		print("Make a move")
		x1 = int(input("input x1"))
		if x1 < 0 or x1 > 7:
			print("invalid x1, be in range [0,6]")
			continue
		y1 = int(input("input y1"))
		if y1 < 0 or y1 > 7:
			print("invalid y1, be in range [0,6]")
			continue
		x2 = int(input("input x2"))
		if x2 < 0 or x2 > 7:
			print("invalid x2, be in range [0,6]")
			continue
		y2 = int(input("input y2"))
		if y2 < 0 or y2 > 7:
			print("invalid y2, be in range [0,6]")
			continue
		if abs(x1-x2) == 1 and y1-y2 == 0:
			input_valid_move = True
		elif x1-x2 == 0 and abs(y1-y2) == 1:
			input_valid_move = True
		else:
			print("Error invalid move")
			continue

		#check user move to see if it make a match
		tuple_1 = (x1, y1)
		tuple_2 = (x2, y2)
		player_move = (tuple_1,tuple_2)
		return (player_move)

#check the player move
#to see if move makes a match
def checkMove(list_of_moves, player_move):
	is_move_a_match = list_of_moves.does_move_exist(player_move)
	return is_move_a_match


#will make the player move
#swaps the positions (then that method will auto-update board and take care of points and stuff)
def matchMade(board, player_move):
	#will call the board swap_positions
	board.swap_positions(player_move)

#Function for only running the mcts dude
#will return the score of each mcts
def runMCTSONLYGame(randomSeedNumber, UCBFunctionToGet):
	game_id = uuid.uuid4()

	results = []

	number_of_moves_to_make = 20

	finalScoreForMCTS = 0

	random.seed(randomSeedNumber)

	func_globals = globals()
	func_globals['add'] = operator.add
	func_globals['mul'] = operator.mul
	func_globals['truediv'] = operator.truediv
	func_globals['sqrt'] = math.sqrt
	func_globals['log'] = math.log
	UCBFunc_code = marshal.loads(UCBFunctionToGet)
	UCBFunc = types.FunctionType(UCBFunc_code, func_globals)
	mcts_ai = MCTSAgent(UCBFunc)

	#mcts
	board = Board(7,7)
	board.init()
	for i in range(number_of_moves_to_make):
		results_list = []
		
		mct_move = mcts_ai.find_next_move(board)
		
		#which trial we on
		results_list.append(str(game_id))
		#which move
		results_list.append(str(i))
		#type of ai
		results_list.append("MCTS")
		#time
		results_list.append(str(mcts_ai.end_time))
		#move ai makes
		results_list.append(str(mct_move))		
		#list of moves on the root
		results_list.append(str(mcts_ai.rootNode.get_state().list_of_possible_moves.move_list)+ "\n")
		#board
		#print(board.board)
		results_list.append(str(board.board))
		
		matchMade(board, mct_move)
		#point after turn
		results_list.append(board.points)

		results_list.append(str(mcts_ai.getRootNode_VisitCount()))

		#print(results_list)
		results.append(results_list)
		
		#grab the final score
		if(i == 19):
			finalScoreForMCTS += board.points

	#print("score: " + str(finalScoreForMCTS))

	return finalScoreForMCTS

#gets the list of results for the mcts 
	#list optimally be np.array, makes life easy when getting mean
#and returns the average score
def calcMCTSAvg(mcts_points_list):
	return np.mean(mcts_points_list)

def main(val, UCBFunctionToGet, logData):

	list_of_results = []

	seeds = val
	mcts_points_result = [0 for x in range(len(seeds))]
	for i in range(len(seeds)):
		mcts_points_result[i] = runMCTSONLYGame(seeds[i], UCBFunctionToGet=UCBFunctionToGet)

	#calc the avg of the mcts_points
	mcts_avg = calcMCTSAvg(np.array(mcts_points_result))

	if (logData):
		file_name = 'testing2.csv'
		file = None

		if not os.path.isfile(file_name):
			file = open(file_name, 'a')
			header = "Game_Id;Turn_#;Agent;Time_Limit;Move_Made;List_Of_Moves;Board;Points;\n"
			file.write(header)
		else:
			file = open(file_name, 'a')

		wr = csv.writer(file, delimiter=";")

		for each_trial in list_of_results:
			wr.writerows(each_trial)
		
		file.close()	

	return mcts_avg

