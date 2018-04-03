import numpy as np
import random
import copy
from moveList import MoveList

class Board:

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
		if(self.points >= 3294.3275):
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
#  [  3,  19,   3, 199,  61, 163,  19],
#  [  3,   3,   3, 163, 199,   3,  43],
#  [163, 199,  61,  19, 199, 199,  19],
#  [ 19,  61,  61, 199,   3,  61, 163]]
# )
# 		self.board = np.array(
# [[ 61,  61, 61,  61, 163,  61, 199],
#  [ 61, 163,  43, 163,   3,  19,  43],
#  [ 61,  19, 199,   3,  43, 163,  19],
#  [ 61,  61, 163,  61,  61,   3,   3],
#  [163,   3, 199,  19, 163, 199,  43],
#  [  3, 163,  61,  43,   3,  61,  19],
#  [ 43,  43,   3,  19,  19,   3,   3]]
# )
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
		# possible_hell = self.get_sum_that_matter_hell_edition(board)
		# self.check_for_intersection_and_horizontal_and_vertical(possible_hell, givePoints, board)
		
		possible_vert_coll, possible_horizontal_coll = self.get_sum_that_matter(board)
		# print(board)
		# print("horizontal")
		# print(possible_horizontal_coll)
		# print("vertical")
		# print(possible_vert_coll)

		# #compare the two sets for intersections =
		self.find_intersection(possible_vert_coll, possible_horizontal_coll, givePoints, board)
		# #now we check for normal 3, normal 4, normal 5 in a row
		self.normal_vert_check(possible_vert_coll, givePoints, board)
		self.normal_horiz_check(possible_horizontal_coll, givePoints, board)
		
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
			
		#moves_made is a MoveList
		self.possible_moves_to_make = self.get_possible_moves(board)
		while (self.possible_moves_to_make.move_list == { }):
			# input("NO MOVES")
			# print("board before")
			# print(board)
			self.random_board(board)
			# print("board After")
			# print(board)
			# input("TRIED TO FIX")
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

	#vertical sums that represent 3 of same item back to back in col
	#return possible_vert_coll
	#horizontal sums that represent 3 of same item back to back in row
	#return possible_horizontal_coll
	def get_sum_that_matter_hell_edition(self, board):
		possible_hell = {}

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
								horizontal_sequ = set()
								horizontal_sequ.add((i,j))
								horizontal_sequ.add((i, j+1))
								horizontal_sequ.add((i, j+2))
								for x in range(j+3, self.cols):
									if board[i][x] == k:
										horizontal_sequ.add((i, x))
									else:
										break
								possible_hell[frozenset(horizontal_sequ)] = set()
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
								#check to see if (i, j) is in the keys for possible hell
								#if it is, then just add to the values
								#else, just do a frozenset key again
								vertical_seq = set()
								vertical_seq.add((i, j))
								vertical_seq.add((i+1,j))
								vertical_seq.add((i+2,j))
								recorded_intersection = False
								for x in range(i+3, self.rows):
									if board[x][j] == k:
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
								break
		
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
		droppingAmountMaxtrix = [[0 for x in range(self.cols)] for y in range(self.rows)] 
		#figure out which to drop and by how much 
		for x in range(self.rows-1)[::-1]:
			for y in range(self.cols)[::-1]:
				if board[x][y] == 0 and board[x+1][y] == 0:
					droppingAmountMaxtrix[x][y] = droppingAmountMaxtrix[x+1][y] + 1
				elif board[x][y] == 0 and board[x+1][y] != 0:
					droppingAmountMaxtrix[x][y] = droppingAmountMaxtrix[x+1][y]
				elif board[x][y] != 0 and board[x+1][y] == 0: 
					droppingAmountMaxtrix[x][y] = droppingAmountMaxtrix[x+1][y] + 1
				elif board[x][y] != 0 and board[x+1][y] != 0:
					droppingAmountMaxtrix[x][y] = droppingAmountMaxtrix[x+1][y]

		#update board to drop things
		for x in range(len(droppingAmountMaxtrix))[::-1]:
			for y in range(len(droppingAmountMaxtrix[x]))[::-1]:
				#only care about the non empty spots
				if board[x][y] != 0:
					#only care about the non empty spots that move
					if droppingAmountMaxtrix[x][y] != 0:
						dropping = droppingAmountMaxtrix[x][y]
						board[x+dropping][y] = board[x][y]
						board[x][y] = 0
	
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
		#random.seed(40)
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
				if (i <= 0):
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

		#check for match 3
		for x in range(self.rows):
			for y in range(self.cols):
				there_is_a_window = True
				#top row guys
				if x == 0 and y != 0 and y < (self.cols-1):
					window = [
								[0, 0, 0], 
								[board[x][y-1]  , board[x][y]  , board[x][y+1]   ],
								[board[x+1][y-1], board[x+1][y], board[x+1][y+1] ]
							 ]
					# window = np.insert((board)[x:x+2, y-1:y+2], 0, [0, 0, 0], axis=0)
				#left guy
				elif x != 0 and y == 0 and x < (self.rows-1):
					window = [
								[0, board[x-1][y], board[x-1][y+1] ],
								[0, board[x][y]  , board[x][y+1]   ],
								[0, board[x+1][y], board[x+1][y+1] ]
							 ]
					# window = np.insert((board)[x-1:x+2, y:y+2], 0, [0, 0, 0], axis=1)
				#last guy break
				elif (x == (self.rows-1) and y == (self.cols-1)) or (x == 0 and y == 0) or (x == 0 and y == self.cols-1) or (x == self.rows-1 and y == 0):
					#there_is_a_window = False
					continue
				#x-1->x+1, y-1-<y+1
				else:
					if y == (self.cols-1) or x == (self.rows-1):
						window = [
									[board[x-1][y-1], board[x-1][y], 0],
									[board[x][y-1]  , board[x][y]  , 0],
									[0, 0, 0]
								 ]
						# window = np.insert((board)[x-1:x+1, y-1:y+1], 2, [0, 0], axis=1)
						# window = np.insert(window, 2, [0, 0, 0], axis=0)
					else:
						window = (board)[x-1:x+2, y-1:y+2]

				# if (there_is_a_window):
				# 	center_of_window_value = board[x][y]
				# 	total = 0
				# 	exp = 8
				# 	for  i in range(len(window)):
				# 		for j in range(len(window[i])):
				# 			total += (1 if window[i][j] - center_of_window_value == 0 else 0) * (2**exp)
				# 			exp -= 1						
					
				center_of_window_value = board[x][y]
				result = [[1 if window[m][n] - center_of_window_value == 0 else 0 for n in range(len(window[m]))] for m in range(len(window))]
				self.check_window(result, x,y, list_of_moves_class)

				if (x < self.rows-3) and not (board[x+1][y] == board[x+2][y]):
					window_4_row = ([board[x][y], board[x+1][y], board[x+2][y], board[x+3][y]])
					start_row_val = board[x][y]
					result_swap = [1 if window_4_row[m] - start_row_val == 0 else 0 for m in range(len(window_4_row))]
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
					window_4_col = ([board[x][y], board[x][y+1], board[x][y+2], board[x][y+3]])
					start_col_value = board[x][y]
					result_swap = [1 if window_4_col[m] - start_col_value == 0 else 0 for m in range(len(window_4_col))]
					if(sum(result_swap) == 3):
						if(result_swap[1] == 0):
							swap_1 = (x,y)
							swap_2 = (x,y+1)

							list_of_moves_class.push(swap_1,swap_2)

							
						else:
							swap_1 = (x,y+2)
							swap_2 = (x,y+3)

							list_of_moves_class.push(swap_1,swap_2)
				
		return list_of_moves_class

	#check for match with window
	def check_window(self, window, center_of_window_x, center_of_window_y, list_of_moves_class):
		total = 0
		exp = 8
		for  i in range(len(window)):
			for j in range(len(window[i])):
				total += window[i][j] * (2**exp)
				exp -= 1

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
