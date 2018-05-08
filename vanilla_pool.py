import pyximport; pyximport.install()
from cythoned import *

import operator
import math
import numbers
import marshal
import random
import time
import uuid
import itertools
import os
import sys
from deap import base
from deap import creator
from deap import gp
from deap import tools
from deap import algorithms
import multiprocessing as mp
import numpy as np
from prettyPrintTree import prettyPrint

from global_functions import *
from config import *

import sympy
from sympy import Symbol, sqrt
from sympy.parsing.sympy_parser import parse_expr

pop_size = number_of_individuals

ngen=number_of_generations

eachGenResults_file = 'data/vanilla_output.csv.txt'

def evalFunc(seed):
    #pass UCBFunctionToGet
    #play game n times with n seeds, return avg score overall
    score = main(number_of_games_per_worker, False, seed) 
    return score,

def eachGenResultsToWrite(toWriteHeader, g=None, num_sims=None, pop_size=None, pop_highscore=None, current_time=None):
	if(toWriteHeader):
		sys.stdout = open(eachGenResults_file, 'w')
		print('GEN;num-sims;pop-size;max-fitness;ellapsed-time;')
	else:
		sys.stdout = open(eachGenResults_file, 'a')
		print(str(g) + ';' + str(num_sims) + ";" + str(pop_size) + ";" + str(pop_highscore) + ';' + str(current_time) + ';')
	sys.stdout = sys.__stdout__

def readSeedsFromFile(fp):
	result = []
	
	for line in file_pointer:
		value_str = line.split('\n')[0]
		result.append(float(line.split('\n')[0]))
	
	return result

if __name__ == "__main__":
	
	eachGenResultsToWrite(True)

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
		seeds_list = readFromFile(fp_my_seeds)

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
		for i in range(0, len(scores)):
			score_buffer_ran += str(rand_scores[i])
			if i < len(scores) - 1:
				score_buffer_ran += "\n"
		writeToFile(temp_file, score_buffer_ran)
		closeFile(temp_file)

		#write the max to a file too
		eachGenResultsToWrite(False, g=g, num_sims=number_of_games_per_worker, pop_size=pop_size, pop_highscore=np.max(mcts_scores), current_time=str(time.time() - start))


	pool.terminate()

	print('done')
	
















'''
import operator
import math
import game
from deap import base
from deap import creator
from deap import gp
from deap import tools
from deap import algorithms

from prettyPrintTree import prettyPrint

from contextlib import redirect_stdout

import multiprocessing as mp

#toolbox.evaluate 
def evalFunc(individual):
	print (prettyPrint(individual))
	print (individual)
	UCBFunctionToGet = toolbox.compile(individual)
	#pass UCBFunctionToGet
	#play game n times with n seeds, return avg score overall
	n = 1
	score =	game.main([0,n], UCBFunctionToGet, False)

	return (score,)

def originalMCTSFunc():
	new_individual = gp.PrimitiveTree.from_string("add(truediv(child_win_score, child_visit_count), (mul(1.414,sqrt(mul(2.0,truediv(log(current_visit_count),child_visit_count))))) )", pset)

	#UCBFunctionToGet = toolbox.compile(new_individual)
	#print(UCBFunctionToGet(2,3,4),)

	return new_individual

pool = mp.Pool()
pset = gp.PrimitiveSetTyped('MAIN', [float, float, float], float)
pset.renameArguments(ARG0='child_win_score', ARG1='child_visit_count', ARG2='current_visit_count')
pset.addPrimitive(operator.add, [float, float], float)
pset.addPrimitive(operator.mul, [float, float], float)
pset.addPrimitive(operator.truediv, [float, float], float)
pset.addPrimitive(math.sqrt, [float], float)
pset.addPrimitive(math.log, [float],float)
pset.addTerminal(1.414, float)
pset.addTerminal(0.5, float)
pset.addTerminal(2.0, float)
pset.addTerminal(3.0, float)
pset.addTerminal(4.0, float)
pset.addTerminal(5.0, float)

creator.create('FitnessMax', base.Fitness, weights=(1.0,))
creator.create('Individual', gp.PrimitiveTree, fitness=creator.FitnessMax,
              pset=pset)

toolbox = base.Toolbox()
toolbox.register('compile', gp.compile, pset=pset)
toolbox.register('expr', gp.genFull, pset=pset, min_=5, max_=5)
toolbox.register('individual', tools.initIterate, creator.Individual,
                toolbox.expr)

toolbox.register('evaluate', evalFunc)

toolbox.register('population', tools.initRepeat, list, toolbox.individual)
toolbox.register('select', tools.selBest)
toolbox.register('mate', gp.cxOnePoint)
toolbox.register('mutate', gp.mutUniform, expr=toolbox.expr, pset=pset)

toolbox.register('map', pool.map)

#for the single uct individual
toolbox.register('create_initial_uct', originalMCTSFunc)
toolbox.register('initial_uct', tools.initIterate, creator.Individual, toolbox.create_initial_uct)

initial_uct_indiv = toolbox.initial_uct()
#s =toolbox.evaluate(initial_uct_indiv)
#print(s)

#then test generations
#population of 5 so computer doesnt cry
pop = toolbox.population (4)
pop.append(initial_uct_indiv)

if __name__ == '__main__':
	#setup for the gp/deap
	#gpStuff()

	#the original uct guy
	
	#initial_uct_indiv = toolbox.initial_uct()
	#s =toolbox.evaluate(initial_uct_indiv)
	#print(s)

	#then test generations
	#population of 5 so computer doesnt cry
	#pop = toolbox.population (4)
	#pop.append(initial_uct_indiv)
	
	#for p in pop:
	#	print(prettyPrint(p))
	
	with open('output.txt', 'w') as outfile:
		with redirect_stdout(outfile):
			final_pop = algorithms.eaSimple (pop, toolbox, cxpb=0.5, mutpb=0.2, ngen=2)
			
			for fp in toolbox.select(final_pop[0], k = 3):
				print(prettyPrint(fp))
				print(fp.fitness)

	pool.terminate()
'''