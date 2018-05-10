import pyximport; pyximport.install()
from cythoned import *

import random

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

def matchMade(board, player_move):
	#will call the board swap_positions
	board.swap_positions(player_move)

random.seed(56624)
board = Board(7,7)
board.init()
while True:
	print("Board in Main after sht happens")
	print(board.board)
	print(board.possible_moves_to_make.move_list)
	print(board.points)
	p = makeMove()
	matchMade(board, p)
	print("board after move")
	print(board.board)
	print(board.points)