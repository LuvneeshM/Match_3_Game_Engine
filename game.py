from board import Board
from randomAgent import RandomAgent
import random
import copy
import time
import csv
import numpy as np
from mctsAgent import MCTSAgent
import uuid
import os, sys
from functools import partial
import marshal
import multiprocessing as mp
import types

import operator, math

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

def runGame(randomSeedNumber, UCBFunctionToGet):
	
	game_id = uuid.uuid4()

	results = []

	number_of_moves_to_make = 20

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
	random_ai = RandomAgent()

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

	random.seed(randomSeedNumber)

	#random
	board = Board(7,7)
	board.init()
	for i in range(number_of_moves_to_make):
		results_list = []

		#list of possible moves
		list_of_moves = board.possible_moves_to_make
		
		#ai_move is (tuple_1, tuple_2)
		#tuple_1 and tuple_2 are the positions of the numbers to swap
		ai_move = random_ai.pick_random_move(list_of_moves)

		#which trial we on
		results_list.append(str(game_id))
		#which move
		results_list.append(str(i))
		#type of ai
		results_list.append("RAND")
		#time
		results_list.append(str(0))
		#move ai makes
		results_list.append(str(ai_move))		
		#list of moves on the root
		results_list.append(str(list_of_moves.move_list) + "\n")
		#board
		results_list.append(str(board.board))

		matchMade(board, ai_move)
		
		#point after turn
		results_list.append(board.points)
		
		results.append(results_list)
	
	return results

#Function for only running the mcts dude
#will return the score of each mcts
def runMCTSONLYGame(UCBFunctionToGet):
	game_id = uuid.uuid4()

	results = []

	number_of_moves_to_make = 20

	finalScoreForMCTS = 0

	# random.seed(randomSeedNumber)

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

	#seed = 40
	#try:
	num_games_to_play = val
	#pool = mp.Pool(mp.cpu_count())
	#list_of_results = pool.map(partial(runGame, UCBFunctionToGet=marshal.dumps(UCBFunctionToGet.__code__)), seeds)
	#mcts_points_result = map(partial(runMCTSONLYGame, UCBFunctionToGet=marshal.dumps(UCBFunctionToGet.__code__)), seeds)
	mcts_points_result = [0 for x in range(num_games_to_play)]
	for i in range(num_games_to_play):
		mcts_points_result[i] = runMCTSONLYGame(UCBFunctionToGet)
	#pool.terminate()

	#calc the avg of the mcts_points
	mcts_avg = calcMCTSAvg(np.array(mcts_points_result))

	#except:
	#	error_file = open("errors.csv", 'a')
	#	error_file.write("Error\n")
	#	error_file.close()
	#	pass

	#for trial in range(5):
	#	results = runGame(seed, trial)
	#	list_of_results.append(results)

	#print(((list_of_results[0])[0])[6])
	
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

#if __name__ == '__main__':
	#x = range(0, 10000)
	#for i in range(0, 0):
	#	print (x[(i*10):(i*10)+10])
	#	main(x[(i*10):(i*10)+10])
#	main([0, 0])

'''
print(gpTesting.UCBFunctionToGet)

board = Board(7,7)
board.init()
list_of_results = runGame(1)
file_name = 'gpMCTSTesting5.csv'
file = None

if not os.path.isfile(file_name):
	file = open(file_name, 'a')
	header = "Game_Id;Turn_#;Agent;Time_Limit;Move_Made;List_Of_Moves;Board;Points;Root_Visit_Count\n"
	file.write(header)
else:
	file = open(file_name, 'a')

wr = csv.writer(file, delimiter=";")
wr.writerows(list_of_results)

file.close()	
'''



#if __name__ == '__main__':
#	main()

