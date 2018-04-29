import time
import random
# time.sleep(random.uniform(1,10))

import pyximport; pyximport.install()
from cythoned import *

from global_functions import *
from config import *
import sys

import ast


from mpi4py import MPI

def playGame(individual):
	score = main(number_of_games_per_worker, individual, False) #main function from game in the cythoned.pyx file
	return score

id = rank - 1
current_iteration = 1

current_directory = "data/generation-" + str(current_iteration) + "/"

input_file = "test.txt"
output_file_prefix = "ind-"
output_file_sufix = ".txt"

#value depends on the number of games we want each player playing
number_of_total_games_I_play = 20 #100/5 = 20, every 20th I play

def consumerFunc():
	while True:
		comm.send(None, dest=0, tag=tags.READY)
		#task is a tuple: seed and current generation number
		task = comm.recv(source=0, tag=MPI.ANY_TAG, status=status)
		tag = status.Get_tag()

		
		if tag == tags.START:
			
			seed = task[0]
			current_iteration = task[1]
			current_directory = "data/generation-" + str(current_iteration) + "/"
			try:
				file_pointer = openFile(current_directory + input_file)
				file_data = readFromFile(file_pointer)
				closeFile(file_pointer)
			except:
				print ("Failed to open ", current_directory + input_file)
				time.sleep(0.1)
				continue

			population = [ast.literal_eval(file_data[i]) for i in range(1, len(file_data))]
		
			evaluated_pop = [ast.literal_eval(file_data[i+1]) for i in range(0, len(file_data)-1) if (i % number_of_total_games_I_play) == (id % number_of_total_games_I_play)]

			print(id, "is playing Games")
			print("num gmaes playing", len(evaluated_pop))
			# result = random.sample(range(1000,4000), len(evaluated_pop))
			result = list(map(playGame, evaluated_pop))
			print(id, "finished playing Games")

			comm.send(result, dest=0, tag=tags.DONE)

			# i = (id % number_of_total_games_I_play)
			# index = 0
			# while i < (len(result) * number_of_total_games_I_play):
			# 	addToFile(current_directory + output_file_prefix + str(i) + output_file_sufix, str(result[index]) + ";")
			# 	i += number_of_total_games_I_play
			# 	index += 1
			# 	#addToFile(log_file, "DONE")
			
			time.sleep(5)

		elif tag == tags.SLEEP:
			print("sleep", id)
			time.sleep(SLEEP_TIME_CONSUMER)

		elif tag == tags.EXIT:
			print("exit", id)
			break

	comm.send(None, dest=0, tag=tags.EXIT)

