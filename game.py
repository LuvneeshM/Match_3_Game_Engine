from board import Board
from randomAgent import RandomAgent
import random
import copy
import time
import csv
from mctsAgent import MCTSAgent
import uuid
import os, sys


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
	return is_move_a_match


#will make the player move
#swaps the positions (then that method will auto-update board and take care of points and stuff)
def matchMade(board, player_move):
	#will call the board swap_positions
	board.swap_positions(board.board, player_move)

def runGame(randomSeedNumber,trial):
	
	random.seed(randomSeedNumber)
	board = Board(7,7)
	
	game_id = uuid.uuid4()

	results = []

	#mcts
	board.init()
	print(board.board)
	mcts_ai = MCTSAgent()
	for i in range(20):
		results_list = []
		
		
		mct_move = mcts_ai.find_next_move(board)
		
		matchMade(board, mct_move)
		#which trial we on
		results_list.append(str(game_id))
		#which move
		results_list.append(str(i))
		#type of ai
		results_list.append("MCTS")
		#point after turn
		results_list.append(board.points)
		#time
		results_list.append(str(mcts_ai.end_time))
		#move ai makes
		results_list.append(str(mct_move))		
		#list of moves on the root
		results_list.append(str(mcts_ai.rootNode.get_state().list_of_possible_moves.move_list))
		
		results.append(results_list)
	random.seed(randomSeedNumber)

	#random
	board.init()
	random_ai = RandomAgent()
	for i in range(20):
		results_list = []

		#list of possible moves
		list_of_moves = board.possible_moves_to_make
		
		#ai_move is (tuple_1, tuple_2)
		#tuple_1 and tuple_2 are the positions of the numbers to swap
		ai_move = random_ai.pick_random_move(list_of_moves)
		matchMade(board, ai_move)
		#which trial we on
		results_list.append(str(game_id))
		#which move
		results_list.append(str(i))
		#type of ai
		results_list.append("Random")
		#point after turn
		results_list.append(board.points)
		#time
		results_list.append(str(0))
		#move ai makes
		results_list.append(str(ai_move))		
		#list of moves on the root
		results_list.append(str(list_of_moves.move_list))
		
		results.append(results_list)
	
	return results


def main():

	list_of_results = []

	seed = 40
	for trial in range(2):
		
		results = runGame(seed, trial)
		
		list_of_results.append(results)

	file_name = 'results.csv'
	file = None

	if not os.path.isfile(file_name):
		file = open(file_name, 'a')
		header = "Game_Id, Turn_#, Agent, Points, Time_Limit, Move_Made, List_Of_Moves\n"
		file.write(header)
	else:
		file = open(file_name, 'a')

	wr = csv.writer(file, delimiter=",")

	for each_trial in list_of_results:
		#print(each_trial)
		wr.writerows(each_trial)
	
	file.close()	


	'''	
	#player plays game
	#list_of_moves = board.possible_moves_to_make

	#player plays game
	
	#player makes move
	print("Hint valid moves are")
	list_of_moves.to_string()
	
	player_move = makeMove()
	print("player move is:", player_move)
	is_pMove_a_match = checkMove(list_of_moves, player_move)

	#if move made a match, update board
	if(is_pMove_a_match):
		print("BOARD\n",board.board)
		k = board.clone()
		#k = copy.deepcopy(board)
		matchMade(k,player_move)
		print("copy\n",k.board)
		print("BOARD\n",board.board)
	#not a match, repeat
	else:
		print("jokes")

	'''
	'''
	#Random Agent plays game
	results = []

	random_ai = RandomAgent()
	try:
		for j in range(1000):
			board = Board(7,7)
			board.init()
			for i in range(20):
				#list of possible moves
				list_of_moves = board.possible_moves_to_make
				
				#ai plays game
				#ai_move is (tuple_1, tuple_2)
				#tuple_1 and tuple_2 are the positions of the numbers to swap
				ai_move = random_ai.pick_random_move(list_of_moves)
				matchMade(board, ai_move)
			
			results.append(board.points)
			if (board.points == 0):
					raise
			print(j)
	except:
		print(board.board)
		raise
	print(float(sum(results)) / float(len(results)))
	print (max(results))
	print (min(results))
	'''
		
if __name__ == '__main__':
	main()

