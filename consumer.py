from global_functions import *
import sys
import os
import time
import ast
import random
import game
from config import *

#from multiprocessing import Process
#import multiprocessing

input_file = "current_gen_info.txt"
output_file_prefix = "output_"
output_file_suffix = ".txt"

log_file = "log.txt"

# def init():
# 	created = multiprocessing.Process()
# 	current = multiprocessing.current_process()
# 	print ('running:', current.name, current._identity)
# 	print ('created:', created.name, created._identity)
	
def playGame(individual):
	seeds = random.sample(range(10000), number_of_games_per_worker)
	print("playing Game")
	score = game.main(seeds, individual, False)
	return score
	
def tempPlace(line_spot):
	return line_spot



def compute(line_spot):
	temp = 0 
	current_iteration = 0
	
	output_file = output_file_prefix + str(line_spot) + output_file_suffix
 
	while True:
		print("I AM ALIVE",line_spot)
		file_pointer = openFile(input_file)
		file_data = readFromFile(file_pointer)
		closeFile(file_pointer)
		
		temp = int(file_data[0])	

		if current_iteration >= number_of_generations:
			print("I AM DEAD ")
			break

		if temp > current_iteration:
			individual = ast.literal_eval(file_data[line_spot])
			result = playGame(individual)

			file_pointer = createFile(output_file)
			writeToFile(file_pointer, str(result))
			closeFile(file_pointer)
			
			addToFile(log_file, "DONE")
			current_iteration += 1
		else:
			print("Consumer " + str(id) + " is Sleeping")
			time.sleep(SLEEP_TIME_CONSUMER)

if __name__=='__main__':
	id = (int(sys.argv[1]) % LIMIT_OF_INDIVIDUALS)+1
	compute(id)