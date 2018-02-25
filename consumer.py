from global_functions import *
import sys
import os
import time
import ast
import random
from config import *

from multiprocessing import Process
import multiprocessing

current_iteration = 0

input_file = "test.txt"
output_file_prefix = "output_"
output_file_suffix = ".txt"

log_file = "log.txt"

def init():
	created = multiprocessing.Process()
	current = multiprocessing.current_process()
	print ('running:', current.name, current._identity)
	print ('created:', created.name, created._identity)
	print()
	

def playGame(individual):
	return gpTesting.evalFunc(individual, number_of_games_per_worker)

def tempPlace(line_spot):
	return line_spot



def compute(line_spot, q):
	global current_iteration
	
	output_file = output_file_prefix + str(line_spot) + output_file_suffix
 
	print("my lines spot is ", line_spot)
	
	#while True:
	file_pointer = openFile(input_file)
	file_data = readFromFile(file_pointer)
	closeFile(file_pointer)
	temp = int(file_data[0])

	if temp > current_iteration:
		individual = ast.literal_eval(file_data[line_spot])

		result = tempPlace(individual)

		file_pointer = createFile(output_file)
		writeToFile(file_pointer, str(result))
		closeFile(file_pointer)
		#time.sleep(random.randint(10,15))
		addToFile(log_file, "DONE")
		q.put("DONE")
		current_iteration += 1
	else:
		time.sleep(SLEEP_TIME_CONSUMER)

	# if current_iteration >= number_of_generations+1:
	# 	break