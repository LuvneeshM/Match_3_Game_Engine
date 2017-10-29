'''
TODO:
MAKE GAME LOOP
ALLOW USER TO SOMEHOW INTERACT AND PICK PIECES TO MOVE 
MAYBE graphics?
'''

#player input for making a move
#x1
#y1
#x2
#y2
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
	print("is it:",is_move_a_match)
	return is_move_a_match

#will make the player move
#swaps the positions (then that method will auto-update board and take care of points and stuff)
def matchMade(board, player_move):
	board.swap_positions(player_move)

import numpy as np
import random

def main():
	board = Board(7,7)
	board.init()
	while True:
		#player makes move
		print("Hint valid moves are")
		list_of_moves = board.getPossibleMoves(board.board)
		print("list of moves")
	#	for i in list_of_moves:
	#		print(i)
		list_of_moves.to_string()
		
		player_move = makeMove()
		print("player move is:", player_move)
		is_pMove_a_match = checkMove(list_of_moves, player_move)

		#if move made a match, update board
		if(is_pMove_a_match):
			matchMade(board, player_move)
		#not a match, repeat
		else:
			print("jokes")

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

	def to_string(self):
		for m in self.move_list.keys():
			for k in self.move_list[m]:
				print ("1: " + str(m) + " 2: " + str(k))

	def push(self, arg_1, arg_2):
		if(arg_1 in self.move_list):
			if(arg_2 not in self.move_list[arg_1]):
				self.move_list[arg_1].append(arg_2)
		else:
			self.move_list[arg_1] = [arg_2]
		#self.move_list[arg_2] = arg_1

	def does_move_exist(self, move_made):
		if move_made[0] in self.move_list:
			if move_made[1] in self.move_list[move_made[0]]:
				return True
		return False

class Board:

	#player move will make a match 3
	#make the swap and update board, give points, etc
	def swap_positions(self, player_move):
		#get the positions
		first_pos = player_move[0]
		second_pos = player_move[1]
		#make the swap
		temp_val = self.board[first_pos[0]][first_pos[1]]
		self.board[first_pos[0]][first_pos[1]] = self.board[second_pos[0]][second_pos[1]]
		self.board[second_pos[0]][second_pos[1]] = temp_val
		#update board stuff now
		self.find_matches(1)
		print("SCORE",self.points)

	'''
	STUFF BELOW DOES THE BACKEND STUFF AUTOMATICALLY
	'''
	def __init__(self, rows, cols):
		self.divisors = [3, 19, 43, 61, 163, 199]
		self.rows = rows
		self.cols = cols
		self.board = []
		self.points = 0;
		self.award_points = {}
		self.set_up_award_points_dict()

		#tester = [
		#		[1, 1, 0],
		#		[0, 1, 1],
		#		[1, 0, 1],
		#		]
		#list_of_moves = self.getPossibleMoves(tester)
		#self.check_window(tester)
		pass

	def init(self):
		self.create_board()

	def set_up_award_points_dict(self):
		self.award_points[3] = 0
		self.award_points[4] = 0
		self.award_points[5] = 0
		self.award_points[6] = 0
		self.award_points[7] = 0
		
	def create_board(self):
		'''
		self.board = [
				[3, 19, 43, 61, 163],
				[3, 3, 163, 61, 19],
				[3, 163, 61, 61, 61],
				[43, 43, 61, 19, 19],
				[163, 3, 3, 3, 19],
				]
		'''
		'''
		self.board = [
				[163, 199, 163, 199, 61, 3, 61],
				[3, 163, 199, 43, 19, 3, 61],
				[199, 199, 163, 163, 19, 19, 43],
				[163, 19, 3, 61, 3, 43, 3],
				[3, 19, 61, 199, 61, 3, 61],
				[3, 163, 3, 3, 163, 19, 19],
				[199, 61, 43, 61, 61, 43, 3]
				]
		'''

		#self.board = [[random.choice(self.divisors) for x in range(self.cols)] for y in range(self.rows)]
		self.board =  [[0 for x in range(self.cols)] for y in range(self.rows)] 
		self.fill_board(self.board)
		self.board_two =  [[0 for x in range(self.cols)] for y in range(self.rows)] 
		self.fill_board_two(self.board_two)
		'''
		self.board = [[  3 , 43 , 43, 199 ,  3 , 19,   3],
					 [ 19,   3,   3 , 19, 163 ,163,  43],
					 [ 43 ,163, 163 , 19 ,  3, 199 ,199],
					 [199 ,  3 , 43 ,199 , 61 , 61 , 61],
					 [ 61 ,199  ,43, 199 ,  3 , 19 ,  3],
					 [ 19 ,  3 ,  3, 163 , 19, 199 ,163],
					 [  3 , 19, 163 , 61, 163 , 19 , 61]]
		'''

		#check board for any pre matches before game starts
		self.find_matches(1)

	'''
	REAL STUFF BELOW 
	WILL DO EVERYTHING FUN 
	SIMPLY CALL
	self.find_matches(1)
	'''
	def find_matches(self, multiplier):
		print("GAMEBOARD")
		print(np.matrix(self.board))

		vertical_sum_matrix = self.sum_vertical(self.board)
		#print(np.matrix(vertical_sum_matrix))
		possible_vert_coll = self.get_vertical_sum_that_matter(vertical_sum_matrix)
		
		#print()

		horizontal_sum_matrix = self.sum_horizontal(self.board)
		#print(np.matrix(horizontal_sum_matrix))
		possible_horizontal_coll = self.get_horizontal_sum_that_matter(horizontal_sum_matrix)

		#print()

		#compare the two sets for intersections =
		self.find_intersection(possible_vert_coll, possible_horizontal_coll, vertical_sum_matrix, horizontal_sum_matrix, True)
		#print()

		#now we check for normal 3, normal 4, normal 5 in a row
		#print("Checked Vertical for Consecutives:")
		self.normal_vert_check(vertical_sum_matrix, possible_vert_coll, True)
		#print(np.matrix(vertical_sum_matrix))

		print()

		#print("Checked Horizontal for Consecutives:")
		#print(np.matrix(horizontal_sum_matrix))
		self.normal_horiz_check(horizontal_sum_matrix, possible_horizontal_coll, True)
		
		
		#print()

		#print("Board now clean of consecs, points to deliver")
		#print(self.award_points)
		#print()
		#print("matches are removed, board updated")
		#print(np.matrix(self.board))
		print("add new pieces to updated GAMEBOARD")
		self.add_new_pieces()
		print(np.matrix(self.board))
		print ("award points, multiplier:", multiplier)
		pointsToAdd = self.user_gets_points()
		print("adding", pointsToAdd * multiplier, "points\n")
		self.points = self.points + (pointsToAdd * multiplier)
		multiplier += 1
		if(pointsToAdd != 0):
			self.find_matches(multiplier)

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
	def get_vertical_sum_that_matter(self, sum_matrix):
		possible_vert_coll = {}
		for i in range(len(sum_matrix)):
			for j in range(len(sum_matrix[i])):
				for k in self.divisors:
					if(sum_matrix[i][j]%k == 0 and sum_matrix[i][j]/k == 3):
						possible_vert_coll[(i,j)] = set()
						possible_vert_coll[(i,j)].add((i,j))
						possible_vert_coll[(i,j)].add((i+1,j))
						possible_vert_coll[(i,j)].add((i+2,j))

		#				print("row",i,"col",j,"divisor",k,"sum", sum_matrix[i][j])

		#for pos in possible_vert_coll:
		#	print("match 3 vert",pos, possible_vert_coll[pos])
		return possible_vert_coll

	#horizontal sums that represent 3 of same item back to back in row
	#return possible_horizontal_coll
	def get_horizontal_sum_that_matter(self, sum_matrix):
		possible_horizontal_coll = {}
		for i in range(len(sum_matrix)):
			for j in range(len(sum_matrix[i])):
				for k in self.divisors:
					if(sum_matrix[i][j]%k == 0 and sum_matrix[i][j]/k == 3):
						possible_horizontal_coll[(i,j)] = set()
						possible_horizontal_coll[(i,j)].add((i,j))
						possible_horizontal_coll[(i,j)].add((i,j+1))
						possible_horizontal_coll[(i,j)].add((i,j+2))

		return possible_horizontal_coll

	#looks for intersection between horizontal and vertical 
	#will be for 5 pieces
	def find_intersection(self, possible_vert_coll, possible_horizontal_coll,vertical_sum_matrix, horizontal_sum_matrix, givePoints):
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

		#get all possible permutations
		for i in x_var:
			for j in y_var:
				possible_pairs_set.add((i,j))

		#print("possible pairs for intersection: ", possible_pairs_set)

		#check for intersection between possible permutations and possible_vert_coll
		#if there is a coll, check to see if intersection in possible_hor_coll
		#if in both then you found intersection in game board
		intersection_pos_to_del = set()
		for vert_key in list(possible_vert_coll.keys()):
			match_found = possible_pairs_set.intersection(possible_vert_coll[vert_key])
			#if found a match
			#CHECK THE HORIZONTAL 
			if(match_found):
				#print("matched in vert: match, vert_key:", match_found,vert_key)
				for horiz_key in list(possible_horizontal_coll.keys()):
					second_match_found = possible_pairs_set.intersection(possible_horizontal_coll[horiz_key])
					#the pair works is in both vertical and horizontal
					if(second_match_found and second_match_found==match_found):
						for pairs_to_del in possible_vert_coll[vert_key].symmetric_difference(possible_horizontal_coll[horiz_key]):
							intersection_pos_to_del.add(pairs_to_del)
							row = pairs_to_del[0]
							col = pairs_to_del[1]
							self.board[row][col] = 0

						intersection_pos_to_del.add(next(iter(match_found)))
						vert_horiz_inter_x = next(iter(match_found))[0]
						vert_horiz_inter_y = next(iter(match_found))[1]
						#update board for values taken care of
						self.board[vert_horiz_inter_x][vert_horiz_inter_y] = 0
						
						#get rid of the interesection place from the two sum matrices too
						possible_vert_coll.pop(vert_key)
						possible_horizontal_coll.pop(horiz_key)
						
						#update vertical sum matrix to not include intersection
						vertical_sum_matrix[vert_key[0]][vert_key[1]] = 0
						#update horizontal sum matrix to not include intersection 
						horizontal_sum_matrix[horiz_key[0]][horiz_key[1]] = 0

						#for pos in possible_vert_coll:
			#			print("match 3 vert after", possible_vert_coll)
			#			print("match 3 horiz after", possible_horizontal_coll)
			#			print ("deleted at: " ,intersection_pos_to_del)
						#player got points of the intersection --> 5
						#5, base value 40 * 5
						if givePoints == True:
							self.award_points[5] += 1
					#else: 
					#	print("Match failed")

	#normal check for vertical matches of 3,4,5,6...
	def normal_vert_check(self, vertical_sum_matrix, possible_vert_coll, givePoints):
		consec_pieces = 2
		vertical_pos_to_del = set()
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
		#list of positions on game board to set to 0							
		for board_pos_to_del in vertical_pos_to_del:
			self.board[board_pos_to_del[0]][board_pos_to_del[1]] = 0
		
	#normal check for horizontal matches of 3,4,5,6...
	#possible_horizontal_coll is a dict
	def normal_horiz_check(self, horizontal_sum_matrix, possible_horizontal_coll, givePoints):
		consec_pieces = 2
		horizontal_pos_to_del = set()

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
			
		#list of positions on game board to set to 0							
		for board_pos_to_del in horizontal_pos_to_del:
			self.board[board_pos_to_del[0]][board_pos_to_del[1]] = 0

	#board is updated
	#add new pieces
	def add_new_pieces(self):
		#first move pieces down
		self.drop_pieces()
		#now add pieces
		self.add_pieces()
		#refill board two
		self.fill_board_two(self.board_two)

	#in board drop board_one items down
	def drop_pieces(self):
		droppingAmountMaxtrix = [[0 for x in range(self.cols)] for y in range(self.rows)] 
		#figure out which to drop and by how much 
		for x in range(self.rows-1)[::-1]:
			for y in range(self.cols)[::-1]:
				if self.board[x][y] == 0 and self.board[x+1][y] == 0:
					droppingAmountMaxtrix[x][y] = droppingAmountMaxtrix[x+1][y] + 1
				elif self.board[x][y] == 0 and self.board[x+1][y] != 0:
					droppingAmountMaxtrix[x][y] = droppingAmountMaxtrix[x+1][y]
				elif self.board[x][y] != 0 and self.board[x+1][y] == 0: 
					droppingAmountMaxtrix[x][y] = droppingAmountMaxtrix[x+1][y] + 1
				elif self.board[x][y] != 0 and self.board[x+1][y] != 0:
					droppingAmountMaxtrix[x][y] = droppingAmountMaxtrix[x+1][y]

		#update board to drop things
		for x in range(len(droppingAmountMaxtrix))[::-1]:
			for y in range(len(droppingAmountMaxtrix[x]))[::-1]:
				#only care about the non empty spots
				if self.board[x][y] != 0:
					#only care about the non empty spots that move
					if droppingAmountMaxtrix[x][y] != 0:
						dropping = droppingAmountMaxtrix[x][y]
						self.board[x+dropping][y] = self.board[x][y]
						self.board[x][y] = 0
	
	#add news numbers to the empty stuff on the top parts of the board	
	def add_pieces(self):
		#add new numbers to board
		#add to these spots
		num_pieces_per_col = [0 for x in range(self.cols)]
		for x in range(self.rows):
			for y in range(self.cols):
				if self.board[x][y] == 0:
					num_pieces_per_col[y] += 1 
		#actually add the pieces from second board
		for x in range(len(num_pieces_per_col)):
			y = num_pieces_per_col[x]-1
			board_two_row = self.rows-1
			while y >= 0:
				self.board[y][x] = self.board_two[board_two_row][x]
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
		'''
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
		for x in range(1, len(board)-1):
			for y in range(1, len(board)-1):
				if y < (num_pieces_per_col[x]):
				#horizontal groups
					while board[x][y] == board[x-1][y] and board[x][y] == board[x+1][y]:
						board[x+1][y] = random.choice(self.divisors)
					#vertical groups
					while board[x][y-1] == board[x][y] and board[x][y] == board[x][y+1]:
						board[x][y+1] = random.choice(self.divisors)
		'''
	
	#user gets their points 
	#also will reset that award_points[i] back to 0
	def user_gets_points(self):
		total_points_earned = 0
		base_value = 20
		for i in (self.award_points):
			print(i,self.award_points[i])
			total_points_earned += i * base_value * self.award_points[i]
			self.award_points[i] = 0
			base_value += 10

		return total_points_earned

	#returns all moves that makes a match
	def getPossibleMoves(self, board):
		print(np.matrix(board))

		list_of_moves_class = MoveList()

		list_of_moves = []
		window_zero = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
		temp_window = None
		#check for match 3
		for x in range(len(board)):
			for y in range(len(board[x])):
				#top row guys
				if x == 0 and y != 0 and y < (len(board[x])-1):
					#print ("x: " + str(x) + " | y: " + str(y))
					window = np.array(board)[x:x+2, y-1:y+2]
					temp_window = np.copy(window_zero)
					for i in range(0, len(window)):
						for j in range(0, len(window[i])):
							temp_window[i+1][j] = window[i][j]
					window = np.copy(temp_window)
				#left guy
				elif x != 0 and y == 0 and x < (len(board)-1):
					#print ("x: " + str(x) + " | y: " + str(y))
					window = np.array(board)[x-1:x+2, y:y+2]
					temp_window = np.copy(window_zero)
					for i in range(0, len(window)):
						for j in range(0, len(window[i])):
							temp_window[i][j+1] = window[i][j]
					window = np.copy(temp_window)
				#last guy break
				elif (x == (len(board)-1) and y == (len(board[x])-1)) or (x == 0 and y == 0) or (x == 0 and y == len(board[x])-1) or (x == len(board)-1 and y == 0):
					#print ("KILL " + str(x) + "," + str(y))
					continue
				#x-1->x+1, y-1-<y+1
				else:
					#print ("x: " + str(x) + " | y: " + str(y))
					window = np.array(board)[x-1:x+2, y-1:y+2]
					if y == (len(board[x])-1) or x == (len(board)-1):
						temp_window = np.copy(window_zero)
						for i in range(0, len(window)):
							for j in range(0, len(window[i])):
								temp_window[i][j] = window[i][j]
						window = np.copy(temp_window)

				#print(window,"\n")				
				center_of_window_value = board[x][y]
				result = [[1 if window[m][n] - center_of_window_value == 0 else 0 for n in range(len(window[m]))] for m in range(len(window))]
				self.check_window(result, list_of_moves, x,y, list_of_moves_class)

		#[_,_,_,_]
		#possible of having 4 in row or 4 in col
		for x in range(len(board)-3):
			for y in range(len(board[x])):
				if not (board[x+1][y] == board[x+2][y]):
					window_4_row = np.array([board[x][y], board[x+1][y], board[x+2][y], board[x+3][y]])
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

							
		for x in range(len(board)):
			for y in range(len(board[x])-3):
				if not (board[x][y+1] == board[x][y+2]):
					window_4_col = [board[x][y], board[x][y+1], board[x][y+2], board[x][y+3]]
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

	def check_window(self, window, list_of_moves, center_of_window_x, center_of_window_y, list_of_moves_class):
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

		#print(total & total_shift_right_2 & total_shift_right_4 & 16)
		#print(total & total_shift_right_4 & total_shift_left_2 & 16)
		#print(total & total_shift_right_4 & total_shift_left_3 & 16)
		#print(total & total_shift_right_3 & total_shift_left_2 & 16)
		#print(total & total_shift_right_3 & total_shift_left_4 & 16)
		#print(total & total_shift_right_2 & total_shift_right_1 & 16)
		#print(total & total_shift_right_2 & total_shift_left_3 & 16)
		#print(total & total_shift_right_2 & total_shift_left_4 & 16)
		#print(total & total_shift_right_1 & total_shift_left_4 & 16)
		#print(total & total_shift_left_1 & total_shift_left_2 & 16)
		#print(total & total_shift_left_2 & total_shift_left_4 & 16)
		
		
if __name__ == '__main__':
	main()

