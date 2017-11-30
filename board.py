import numpy as np
import random
import copy
from moveList import MoveList

class Board:

	#player move will make a match 3
	#make the swap and update board, give points, etc
	#player move --> ((#,#), (#,#))
	def swap_positions(self, board, player_move):
		#get the positions
		first_pos = player_move[0]
		second_pos = player_move[1]
		#make the swap
		if(first_pos[0] >= self.rows or first_pos[1] >= self.rows):
			print("ARG")
			print(self.possible_moves_to_make.move_list)
			input()

		temp_val = board[first_pos[0]][first_pos[1]]
		board[first_pos[0]][first_pos[1]] = board[second_pos[0]][second_pos[1]]
		board[second_pos[0]][second_pos[1]] = temp_val
		#update board stuff now
		self.find_matches(1, True, board)
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


		#tester = [
		#		[1, 1, 0],
		#		[0, 1, 1],
		#		[1, 0, 1],
		#		]
		#list_of_moves = self.get_possible_moves(tester)
		#self.check_window(tester)
		pass

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
		#print("GAMEBOARD")
		#print((self.board))

		vertical_sum_matrix = self.sum_vertical(board)
		###print((vertical_sum_matrix))
		possible_vert_coll = self.get_vertical_sum_that_matter(vertical_sum_matrix, board)
		###print()

		horizontal_sum_matrix = self.sum_horizontal(board)
		###print((horizontal_sum_matrix))
		possible_horizontal_coll = self.get_horizontal_sum_that_matter(horizontal_sum_matrix, board)
		###print()

		#compare the two sets for intersections =
		self.find_intersection(possible_vert_coll, possible_horizontal_coll, vertical_sum_matrix, horizontal_sum_matrix, givePoints, board)
		###print()

		#now we check for normal 3, normal 4, normal 5 in a row
		###print("Checked Vertical for Consecutives:")
		self.normal_vert_check(vertical_sum_matrix, possible_vert_coll, givePoints, board)
		###print((vertical_sum_matrix))

		##print()

		###print("Checked Horizontal for Consecutives:")
		###print((horizontal_sum_matrix))
		self.normal_horiz_check(horizontal_sum_matrix, possible_horizontal_coll, givePoints, board)
		
		
		###print()

		###print("Board now clean of consecs, points to deliver")
		###print(self.award_points)
		###print()
		#print("matches are removed, board updated")
		#print((self.board))
		#gave points, refill board
		if(sum(self.award_points.values()) > 0):
			self.add_new_pieces(board)
			pointsToAdd = self.user_gets_points()
			###print("adding", pointsToAdd * multiplier, "points\n")
			self.points = self.points + (pointsToAdd * multiplier)
			#print("POINTS ADDED", self.points)
			multiplier += 1
			if(pointsToAdd != 0):
				self.find_matches(multiplier, True, board)
			
		else: 
			###print("no matches, next")
			pass
		#moves_made is a MoveList
		self.possible_moves_to_make = self.get_possible_moves(board)
		if(self.possible_moves_to_make.move_list == { }):
			board = self.random_board(board)
			self.possible_moves_to_make = self.get_possible_moves(board)

	def random_board(self, board):
		board = np.array([[0 for x in range(self.cols)] for y in range(self.rows)])
		self.fill_board(board)
		return board

	def sum_vertical(self, board):
		return [ [ board[i][j]+board[i+1][j]+board[i+2][j]
		 	for j in range(len(board[i]))] for i in range(len(board)-2) ]
		'''
		vert_sun = []
		for i in range(len(board)-2):
			vert_sum.append([])
			for j in range(len(board[i])):
				vert_sum[i].append(board[i][j]+board[i+1][j]+board[i+2][j])
		return vert_sum
		'''

	def sum_horizontal(self, board):
		return [ [ board[i][j]+board[i][j+1]+board[i][j
			+2] for j in range(len(board[i])-2)] for i in range(len(board))]
		'''
		horizontal_sum = []
		for i in range(len(board)):
			horizontal_sum.append([])
			for j in range(len(board[i])-2):
				horizontal_sum[i].append(board[i][j]+board[i][j+1]+board[i][j+2])

		return horizontal_sum
		'''

	#vertical sums that represent 3 of same item back to back in col
	#return possible_vert_coll
	def get_vertical_sum_that_matter(self, sum_matrix, board):
		possible_vert_coll = {}
		for j in range(self.cols):
			i = 0
			while i < (self.rows - 2):
				for k in self.divisors:
					##print ("i: " + str(i))
					##print ("j: " + str(j))
					if(sum_matrix[i][j]%k == 0 and sum_matrix[i][j]/k == 3):
						possible_vert_coll[(i,j)] = set()
						possible_vert_coll[(i,j)].add((i,j))
						possible_vert_coll[(i,j)].add((i+1,j))
						possible_vert_coll[(i,j)].add((i+2,j))
						for x in range(i+1, self.rows):
							if board[x][j] == k:
								possible_vert_coll[(i, j)].add((x, j))
								if x == self.rows - 1:
									i = x
							else:
								i = x
								break
						break
				i += 1

		#				##print("row",i,"col",j,"divisor",k,"sum", sum_matrix[i][j])

		#for pos in possible_vert_coll:
		#	##print("match 3 vert",pos, possible_vert_coll[pos])
		##print("PVC: " + str(possible_vert_coll))
		return possible_vert_coll

	#horizontal sums that represent 3 of same item back to back in row
	#return possible_horizontal_coll
	def get_horizontal_sum_that_matter(self, sum_matrix, board):
		possible_horizontal_coll = {}
		for i in range(self.rows):
			j = 0
			while j < (self.cols - 2):
				for k in self.divisors:
					##print ("i: " + str(i))
					##print ("j: " + str(j))
					if(sum_matrix[i][j]%k == 0 and sum_matrix[i][j]/k == 3):
						possible_horizontal_coll[(i,j)] = set()
						possible_horizontal_coll[(i,j)].add((i,j))
						possible_horizontal_coll[(i,j)].add((i,j+1))
						possible_horizontal_coll[(i,j)].add((i,j+2))
						for x in range(j+1, self.cols):
							if board[i][x] == k:
								possible_horizontal_coll[(i, j)].add((i, x))
								if x == self.cols - 1:
									j = x
							else:
								j = x
								break
						break
				j += 1

		##print("PHC: " + str(possible_horizontal_coll))
		return possible_horizontal_coll

	#looks for intersection between horizontal and vertical 
	#will be for 5 pieces
	def find_intersection(self, possible_vert_coll, possible_horizontal_coll,vertical_sum_matrix, horizontal_sum_matrix, givePoints, board):
		x_var = set()
		y_var = set()

		possible_pairs_set = set()

		#get 2nd, which comes form the vertical --> y
		for stuff in possible_vert_coll:
			y_var.add(stuff[1])
		#get 1st, whcih comes from the horizontal --> x
		for stuff in possible_horizontal_coll:
			x_var.add(stuff[0])


		#INSTEAD OF STORING THE POS as KEY, Store the SUM AS the key

		#get all possible permutations in terms of (i,j)
		for i in x_var:
			for j in y_var:
				possible_pairs_set.add((i,j))

		#print("possible pairs for intersection: ", possible_pairs_set)
		#print("possible_vert_coll.keys()",possible_vert_coll.keys())
		#print("possible_horizontal_coll.keys()",possible_horizontal_coll.keys())
		#check for intersection between possible permutations and possible_vert_coll
		#if there is a coll, check to see if intersection in possible_hor_coll
		#if in both then you found intersection in game board
		intersection_pos_to_del = set()
		for vert_key in list(possible_vert_coll.keys()):
			match_found = possible_pairs_set.intersection(possible_vert_coll[vert_key])
			#print("\nmatch",match_found)
			#if found a match
			#CHECK THE HORIZONTAL 
			if(match_found):
				#print("matched in vert: match, vert_key:", match_found,vert_key)
				for horiz_key in list(possible_horizontal_coll.keys()):
					#print("possible_horizontal_coll[horiz_key]",possible_horizontal_coll[horiz_key],"horiz_key",horiz_key)
					second_match_found = match_found.intersection(possible_horizontal_coll[horiz_key])
					#print("second_match_found",second_match_found)
					#the pair works is in both vertical and horizontal
					if(second_match_found and second_match_found.intersection(match_found)):
						#print ("vk: " + str(vert_key))
						#print ("pvc: " + str(possible_vert_coll))
						#print ("hk: " + str(horiz_key))
						#print ("phc: " + str(possible_horizontal_coll))
						number_of_pieces_to_del = 1
						for pairs_to_del in possible_vert_coll[vert_key].symmetric_difference(possible_horizontal_coll[horiz_key]):
							intersection_pos_to_del.add(pairs_to_del)
							row = pairs_to_del[0]
							col = pairs_to_del[1]
							board[row][col] = 0
							number_of_pieces_to_del += 1

						tmp = next(iter(second_match_found))
						intersection_pos_to_del.add(tmp)
						vert_horiz_inter_x = tmp[0]
						vert_horiz_inter_y = tmp[1]
						#update board for values taken care of
						board[vert_horiz_inter_x][vert_horiz_inter_y] = 0
						
						#get rid of the interesection place from the two sum matrices too
						possible_horizontal_coll.pop(horiz_key)
						
						#update vertical sum matrix to not include intersection
						vertical_sum_matrix[vert_key[0]][vert_key[1]] = 0
						#update horizontal sum matrix to not include intersection 
						horizontal_sum_matrix[horiz_key[0]][horiz_key[1]] = 0

						#player got points of the intersection --> 5
						#5, base value 40 * 5
						if givePoints == True:
							#print("PIECES =",number_of_pieces_to_del)
							self.award_points[number_of_pieces_to_del] += 1
					#else: 
					#	##print("Match failed")
					#print(board)
				possible_vert_coll.pop(vert_key)

	#normal check for vertical matches of 3,4,5,6...
	def normal_vert_check(self, vertical_sum_matrix, possible_vert_coll, givePoints, board):
		consec_pieces = 2
		vertical_pos_to_del = set()
		for key_vert in possible_vert_coll:
			if givePoints == True:
				self.award_points[len(possible_vert_coll[key_vert])] += 1
			for val_vert in possible_vert_coll[key_vert]:
				vertical_pos_to_del.add(val_vert)
		'''
		for i in range(len(vertical_sum_matrix)):
			consec_pieces = 2
			for j in range(len(vertical_sum_matrix[i])):
				for k in self.divisors:
					if(vertical_sum_matrix[i][j]%k == 0 and vertical_sum_matrix[i][j]/k == 3):
						consec_pieces += 1
						look_down = True
						next_row = i+1
						while(look_down and next_row < len(vertical_sum_matrix)):
							if vertical_sum_matrix[i][j] == vertical_sum_matrix[next_row][j]:
								for pairs_to_del in possible_vert_coll[(next_row,j)]:
									vertical_pos_to_del.add(pairs_to_del)

								vertical_sum_matrix[next_row][j] = 0
								consec_pieces += 1
								next_row +=1
								
							else:
								vertical_sum_matrix[i][j] = 0
								look_down = False;
						for pairs_to_del in possible_vert_coll[(i,j)]:
							vertical_pos_to_del.add(pairs_to_del)
						#track points for that single 3+ consecutive pieces
						if givePoints == True:
							self.award_points[consec_pieces] += 1
						break
		'''
		#list of positions on game board to set to 0							
		for board_pos_to_del in vertical_pos_to_del:
			board[board_pos_to_del[0]][board_pos_to_del[1]] = 0
		
	#normal check for horizontal matches of 3,4,5,6...
	#possible_horizontal_coll is a dict
	def normal_horiz_check(self, horizontal_sum_matrix, possible_horizontal_coll, givePoints, board):
		consec_pieces = 2
		horizontal_pos_to_del = set()
		for key_hor in possible_horizontal_coll:
			if givePoints == True:
				self.award_points[len(possible_horizontal_coll[key_hor])] += 1
			for val_hor in possible_horizontal_coll[key_hor]:
				horizontal_pos_to_del.add(val_hor)
				#horizontal_sum_matrix[val_hor[0]][val_hor[1]] = 0
			#horizontal_pos_to_del.add()
		'''
		#row
		for i in range(len(horizontal_sum_matrix)):
			consec_pieces = 2
			#col
			j = 0
			while j < len(horizontal_sum_matrix[i]):
				for k in self.divisors:
					if(horizontal_sum_matrix[i][j]%k == 0 and horizontal_sum_matrix[i][j]/k == 3):
						consec_pieces += 1
						look_right = True
						next_col = j+1
						while(look_right and next_col < len(horizontal_sum_matrix[i])):
							if horizontal_sum_matrix[i][j] == horizontal_sum_matrix[i][next_col]:
								for pairs_to_del in possible_horizontal_coll[(i,next_col)]:
									horizontal_pos_to_del.add(pairs_to_del)

								horizontal_sum_matrix[next_col][j] = 0
								consec_pieces += 1
								next_col +=1
								
							else:
								horizontal_sum_matrix[i][j] = 0
								look_right = False;
						for pairs_to_del in possible_horizontal_coll[(i,j)]:
							horizontal_pos_to_del.add(pairs_to_del)
						#track points for that single 3+ consecutive pieces
						if givePoints == True:
							self.award_points[consec_pieces] += 1
						j = next_col
						if j >=len(horizontal_sum_matrix[i]):
							break 
				j += 1
		'''	
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
		for x in range(len(num_pieces_per_col)):
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
		for x in range(len(num_pieces_per_col)):
			y = num_pieces_per_col[x]-1
			while y >= 0:
				board[y][x] = random.choice(self.divisors)
				y -= 1
		#rig board so that no groups of 3 in 2nd board
		for x in range(0, len(board)):
			for y in range(0, len(board)):
				if y < (num_pieces_per_col[x]):
					#vertical groups
					if x < len(board)-1:# and x > 0:
						while board[x][y] == board[x-1][y] and board[x][y] == board[x+1][y]:
							board[x+1][y] = random.choice(self.divisors)
					#horizontal
					if(y < len(board)-1):
						while board[x][y-1] == board[x][y] and board[x][y] == board[x][y+1]:
							board[x][y+1] = random.choice(self.divisors)
		pass

	#after taking from board_Two
	#we update the board down and fill in the stuff on the top
	def fill_board_two(self, board):
		droppingAmountMaxtrix = [[0 for x in range(self.cols)] for y in range(self.rows)] 
		#find how much to drop 
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
		#drop em
		for x in range(len(droppingAmountMaxtrix))[::-1]:
			for y in range(len(droppingAmountMaxtrix[x]))[::-1]:
				#only care about the non empty spots
				if board[x][y] != 0:
					#only care about the non empty spots that move
					if droppingAmountMaxtrix[x][y] != 0:
						dropping = droppingAmountMaxtrix[x][y]
						board[x+dropping][y] = board[x][y]
						board[x][y] = 0
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

		window_zero = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
		temp_window = None
		#check for match 3
		for x in range(len(board)):
			for y in range(len(board[x])):
				#top row guys
				if x == 0 and y != 0 and y < (len(board[x])-1):
					###print ("x: " + str(x) + " | y: " + str(y))
					window = (board)[x:x+2, y-1:y+2]
					temp_window = np.copy(window_zero)
					for i in range(0, len(window)):
						for j in range(0, len(window[i])):
							temp_window[i+1][j] = window[i][j]
					window = np.copy(temp_window)
				#left guy
				elif x != 0 and y == 0 and x < (len(board)-1):
					###print ("x: " + str(x) + " | y: " + str(y))
					window = (board)[x-1:x+2, y:y+2]
					temp_window = np.copy(window_zero)
					for i in range(0, len(window)):
						for j in range(0, len(window[i])):
							temp_window[i][j+1] = window[i][j]
					window = np.copy(temp_window)
				#last guy break
				elif (x == (len(board)-1) and y == (len(board[x])-1)) or (x == 0 and y == 0) or (x == 0 and y == len(board[x])-1) or (x == len(board)-1 and y == 0):
					###print ("KILL " + str(x) + "," + str(y))
					continue
				#x-1->x+1, y-1-<y+1
				else:
					###print ("x: " + str(x) + " | y: " + str(y))
					window = (board)[x-1:x+2, y-1:y+2]
					if y == (len(board[x])-1) or x == (len(board)-1):
						temp_window = np.copy(window_zero)
						for i in range(0, len(window)):
							for j in range(0, len(window[i])):
								temp_window[i][j] = window[i][j]
						window = np.copy(temp_window)

				###print(window,"\n")				
				center_of_window_value = board[x][y]
				result = [[1 if window[m][n] - center_of_window_value == 0 else 0 for n in range(len(window[m]))] for m in range(len(window))]
				self.check_window(result, x,y, list_of_moves_class)

		#[_,_,_,_]
		#possible of having 4 in row or 4 in col
		#row 4+
		for x in range(len(board)-3):
			for y in range(len(board[x])):
				if not (board[x+1][y] == board[x+2][y]):
					window_4_row = ([board[x][y], board[x+1][y], board[x+2][y], board[x+3][y]])
					start_row_val = board[x][y]
					result = [1 if window_4_row[m] - start_row_val == 0 else 0 for m in range(len(window_4_row))]
					if(sum(result) == 3):
						if(result[1] == 0):
							swap_1 = (x,y)
							swap_2 = (x+1,y)

							list_of_moves_class.push(swap_1,swap_2)

						else:
							swap_1 = (x+2,y)
							swap_2 = (x+3,y)
							
							list_of_moves_class.push(swap_1,swap_2)
		#col 4+			
		for x in range(len(board)):
			for y in range(len(board[x])-3):
				if not (board[x][y+1] == board[x][y+2]):
					window_4_col = ([board[x][y], board[x][y+1], board[x][y+2], board[x][y+3]])
					start_col_value = board[x][y]
					result = [1 if window_4_col[m] - start_col_value == 0 else 0 for m in range(len(window_4_col))]
					if(sum(result) == 3):
						if(result[1] == 0):
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
		self.swap_positions(self.board,move_made)