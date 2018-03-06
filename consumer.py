from global_functions import *
import sys
import os
import time
import ast
import random
import game
from config import *
from lockfile import LockFile

#from multiprocessing import Process
#import multiprocessing

input_file = "current_gen_info.txt"
consumer_gen_file = "consumer_current_gen_info.txt"

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

def compute(line_spot):
	temp = 0 
	current_iteration = 0
	 
	lock_input = LockFile("data/"+input_file)
	lock_output = LockFile("data/"+consumer_gen_file)

	while True:
		print("I AM ALIVE",line_spot)

#		print ("Acquiring input_file")
		if (not lock_input.is_locked()):

			lock_input.acquire()
			file_pointer = open("data/" + input_file, "r+")
			file_data = readFromFile(file_pointer)
			file_pointer.seek(0)
			file_pointer.truncate()
			individual = None
			if (len(file_data) > 2):
				individual = file_data[1]
			temp = int(file_data[0])
			if len(file_data) > 2:
				file_data = [file_data[0]] + [l for l in file_data[2:]]
			else:
				file_data = [file_data[0]]
			for line in file_data:
				writeToFile(file_pointer, str(line))	
			closeFile(file_pointer)

			time.sleep(0.1)
			lock_input.release()
#			print ("Released input_file")

			current_iteration = int(file_data[0])

			if current_iteration >= number_of_generations+1:
				print("I AM DEAD ")
				break

			if individual != None:
				individual = ast.literal_eval(individual)
				result = playGame(individual)

#				print ("Acquiring gen_file")
				lock_output.acquire()
#				print ("Got the gen lock")
				
				addToFile(consumer_gen_file, str(individual) + ";" + str(result))
				time.sleep(0.1)
				lock_output.release()
#				print ("Released gen_file")

				individual = None

			else:
				print("Consumer " + str(id) + " is Sleeping")
				time.sleep(SLEEP_TIME_CONSUMER)
		else:
			print("Sleep cause no lock")
			time.sleep(SLEEP_TIME_CONSUMER)

if __name__=='__main__':
	id = (int(sys.argv[1]) % LIMIT_OF_INDIVIDUALS)
	compute(id)
	print ("all done")
	