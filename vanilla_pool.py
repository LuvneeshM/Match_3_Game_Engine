import pyximport; pyximport.install()
from cythoned import *

import random
import time
import os
import sys

import multiprocessing as mp
import numpy as np

from global_functions import *
from config import *

pop_size = number_of_individuals

ngen=number_of_generations

eachGenResults_file = 'data/vanilla_output.csv.txt'
eachGenRandom_file = 'data/random_output.csv.txt'

def evalFunc(seed):
    #pass UCBFunctionToGet
    #play game n times with n seeds, return avg score overall
    score = main(number_of_games_per_worker, False, seed) 
    return score,

def eachGenResultsToWrite(toWriteHeader, file_name, g=None, num_sims=None, pop_size=None, pop_highscore=None, current_time=None):
	if(toWriteHeader):
		sys.stdout = open(file_name, 'w')
		print('GEN;num-sims;pop-size;avg-fitness;ellapsed-time;')
	else:
		sys.stdout = open(file_name, 'a')
		print(str(g) + ';' + str(num_sims) + ";" + str(pop_size) + ";" + str(pop_highscore) + ';' + str(current_time) + ';')
	sys.stdout = sys.__stdout__

def readSeedsFromFile(fp):
	result = []
	
	for line in fp:
		value_str = line.split('\n')[0]
		result.append(float(line.split('\n')[0]))
	
	return result

if __name__ == "__main__":
	seed = 10321
	res = evalFunc(seed)
	print("score for mct, random", res)
	input()
	eachGenResultsToWrite(True, eachGenResults_file)
	eachGenResultsToWrite(True, eachGenRandom_file)
	pool = mp.Pool(mp.cpu_count())

	number_of_seeds = 50

	vanilla_file_name = "vanilla_game_results.txt"

	start_from_previous_gen = False

	vanilla_mcts_score_file_name = "vanilla_mcts_scores.txt"
	random_score_file_name = "random_scores.txt"
	for g in range(1, ngen):
		

		if start_from_previous_gen:
			current_directory = "generation-" + str(g) + "/"
			if os.path.exists("data/" + current_directory + vanilla_mcts_score_file_name):
				print("gen", str(g), "finished before")
				continue
		
		start = time.time()
		#current generation directory
		current_directory = "generation-" + str(g) + "/"
		if not os.path.exists("data/" + current_directory):
			continue
		#grab the seeds for that generation from the folder
		file_name = "my_seeds.txt"
		fp_my_seeds = openFile(current_directory + file_name)
		seeds_list = readSeedsFromFile(fp_my_seeds)

		#will be a list of scores for those 50 seeds for that generation
		print("playing games for gen", str(g))
		scores = pool.map(evalFunc, seeds_list)
		mcts_scores = []
		rand_scores = []
		for i in scores:
			#i = ((1,2),)
			#r[0] -> (1,2)
			#r[0][0] -> 1
			mcts_scores.append(i[0][0])
			rand_scores.append(i[0][1])
			print("score for mct", i)

		print("done playing games for gen", str(g))
		#lets save that value in  a txt for each gen
		temp_file = createFile(current_directory + vanilla_mcts_score_file_name)
		
		score_buffer_mcts = ""
		for i in range(0, len(mcts_scores)):
			score_buffer_mcts += str(mcts_scores[i])
			if i < len(scores) - 1:
				score_buffer_mcts += "\n"
		writeToFile(temp_file, score_buffer_mcts)
		closeFile(temp_file)
		
		temp_file = createFile(current_directory + random_score_file_name)
		score_buffer_ran = ""
		for i in range(0, len(rand_scores)):
			score_buffer_ran += str(rand_scores[i])
			if i < len(scores) - 1:
				score_buffer_ran += "\n"
		writeToFile(temp_file, score_buffer_ran)
		closeFile(temp_file)

		#write the max to a file too
		eachGenResultsToWrite(False,eachGenResults_file, g=g, num_sims=number_of_games_per_worker, pop_size=pop_size, pop_highscore=np.mean(mcts_scores), current_time=str(time.time() - start))
		eachGenResultsToWrite(False,eachGenRandom_file, g=g, num_sims=number_of_games_per_worker, pop_size=pop_size, pop_highscore=np.mean(rand_scores), current_time=str(time.time() - start))

	pool.terminate()

	print('done')
	


