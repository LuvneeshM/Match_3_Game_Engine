from global_functions import *
from config import *
import sys
import time
import ast
import random
import game

def playGame(individual):
	seeds = random.sample(range(10000), number_of_games_per_worker)
	score = game.main(seeds, individual, False)
	return score


id = int(sys.argv[1])
current_iteration = 1

current_directory = "data/generation-" + str(current_iteration) + "/"

input_file = "test.txt"
output_file_prefix = "ind-"
output_file_sufix = ".txt"


#def compute():
temp = 0 
current_iteration = 0

while True:
	try:
		file_pointer = openFile(current_directory + input_file)
		file_data = readFromFile(file_pointer)
		closeFile(file_pointer)
		temp = int(file_data[0])
	except:
		print ("Failed to open ", current_directory + input_file)
		time.sleep(0.1)
		continue

	length_of_data = 0
	try:
		offset = (id % 2) - 2
		test_pointer = openFile(current_directory + "ind-" + str(number_of_individuals + offset) + ".txt")
		test_data = readLineFromFile(test_pointer)
		length_of_data = len(test_data)
	except:
		pass

	print ("Data len: ", length_of_data)
	if length_of_data < number_of_simulations:
		population = [ast.literal_eval(file_data[i]) for i in range(1, len(file_data))]
		
		evaluated_pop = [ast.literal_eval(file_data[i+1]) for i in range(0, len(file_data)-1) if (i % 10) == (id % 10)]

		print(id, "is playing Games")
		print(len(evaluated_pop))
		result = list(map(playGame, evaluated_pop))
		print(id, "finished playing Games")

		i = id % 10
		index = 0
		while i < (len(result) * 10):
			addToFile(current_directory + output_file_prefix + str(i) + output_file_sufix, str(result[index]) + ";")
			i += 10
			index += 1
			#addToFile(log_file, "DONE")
		
		time.sleep(5)
		#current_iteration += 1
	else:
		current_iteration += 1
		print ("Start gen ", current_iteration)
		current_directory = "data/generation-" + str(current_iteration) + "/"
		time.sleep(SLEEP_TIME_CONSUMER)
	
	if current_iteration >= number_of_generations+1:
		break	