from board import Board
from randomAgent import RandomAgent
import copy
from mctsAgent import MCTSAgent

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

def main():

	file = open('results_5.txt', 'a')

	randWins = 0
	mctsWins = 0
	
	for trial in range(30):
		print("START",trial)

		toAppend = "======" + "TRIAL: " + str(trial) + "======\n"
		file.write(toAppend)
		board = Board(7,7)
		board.init()
		
		rand_agent_board = board.clone()
		mcts_agent_board = board.clone()
		
		#print ("=====BEFORE=====")
		#print ("=====NORMAL=====")
		#print(board.board)
		#print ("=====RANDOM=====")
		#print(rand_agent_board.board)
		#print ("======MCTS======")
		#print(mcts_agent_board.board)

		random_ai = RandomAgent()
		mcts_ai = MCTSAgent()

		toAppend = "======RANDOM ======\n"	
		file.write(toAppend)
		#run random for 20 turns	
		for i in range(20):
			#list of possible moves
			list_of_moves = rand_agent_board.possible_moves_to_make
			
			#ai_move is (tuple_1, tuple_2)
			#tuple_1 and tuple_2 are the positions of the numbers to swap
			ai_move = random_ai.pick_random_move(list_of_moves)
			matchMade(rand_agent_board, ai_move)
			if i != 19:
				toAppend = ("\t" + str(i) + " Random Single Move: " + "move: " + str(ai_move) + " score: " + str(rand_agent_board.points) + "\n")
			else:
				toAppend = (str(i) + " Random Result: " + "move: " + str(ai_move) + " score: " + str(rand_agent_board.points) + "\n")
			file.write(toAppend)
		#print("Random Points:", rand_agent_board.points)
		#toAppend = ("Random Results: " + str(rand_agent_board.points) + "\n")
		
		toAppend = "======MCTS======\n"	
		file.write(toAppend)
		for i in range(20):
			mct_move = mcts_ai.find_next_move(mcts_agent_board)
			matchMade(mcts_agent_board, mct_move)
			if i != 19:
				toAppend = ("\t"  + str(i) + " MCTS Single Move: " + "move: " + str(ai_move) + " score: " + str(mcts_agent_board.points) + "\n")
			else: 
				toAppend = (str(i) + " MCTS Results: " + "move: " + str(ai_move)	+ " score: " + str(mcts_agent_board.points) + "\n")
			file.write(toAppend)
		
		#print ("=====AFTER======")
		#print ("=====NORMAL=====")
		#print(board.board)
		#print ("=====RANDOM=====")
		#print(rand_agent_board.board)
		#print ("======MCTS======")
		#print(mcts_agent_board.board)
		
		print("random ai", rand_agent_board.points)
		print("mcts ai", mcts_agent_board.points)
		if(rand_agent_board.points > mcts_agent_board.points): 
			randWins = randWins + 1
			file.write("Winner Random")
			print("Winner Random")
		else:
			mctsWins = mctsWins + 1
			file.write("Winner MCTS")
			print("Winner MCTS")

		file.write("\n\n")

		print("END")
	file.write("Random won: " + str(randWins) + "\n")
	file.write("MCTS won: " + str(mctsWins))
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

