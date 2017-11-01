'''
TODO:
MAKE GAME LOOP
ALLOW USER TO SOMEHOW INTERACT AND PICK PIECES TO MOVE 
MAYBE graphics?
'''

from board import Board
from randomAgent import RandomAgent
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
	#will call the board swap_positions
	board.swap_positions(player_move)


def main():
	results = []

	random_ai = RandomAgent()
	try:
		for j in range(1000):
			board = Board(7,7)
			board.init()
			for i in range(20):
				#list of possible moves
				list_of_moves = board.possible_moves_to_make

				#player plays game
				'''
				#player makes move
				print("Hint valid moves are")
				
				#print("list of moves")
				#list_of_moves.to_string()
				
				player_move = makeMove()
				print("player move is:", player_move)
				is_pMove_a_match = checkMove(list_of_moves, player_move)

				#if move made a match, update board
				if(is_pMove_a_match):
					matchMade(board, player_move)
				#not a match, repeat
				else:
					print("jokes")
				'''

				#print("list of moves")
				#list_of_moves.to_string()

				#ai plays game
				#ai_move is (tuple_1, tuple_2)
				#tuple_1 and tuple_2 are the positions of the numbers to swap
				ai_move = random_ai.pick_random_move(list_of_moves)
				matchMade(board, ai_move)
			
			results.append(board.points)
			print(j)
	except:
		print(board.board)
		raise
	print(float(sum(results)) / float(len(results)))
	print max(results)
	print min(results)
		
if __name__ == '__main__':
	main()

