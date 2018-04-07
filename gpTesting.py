# import pyximport; pyximport.install()
# from cythoned import *

import pyximport; pyximport.install()
from cythoned import *

import operator
import math
# import game
import marshal
import random
import time
import uuid
import itertools
import os
from deap import base
from deap import creator
from deap import gp
from deap import tools
from deap import algorithms
import multiprocessing as mp
from prettyPrintTree import prettyPrint
import sys

from global_functions import *
from config import *

#global variables
pool = None
pset = None
toolbox = None

pop_size = number_of_individuals

cxpb=0.5
mutpb=0.2
ngen=number_of_generations

eachGenResults_file = 'data/output.csv.txt'
originalEq_file = 'data/original_population_eqs.csv.txt'
finalEq_file = 'data/gen-results.csv.txt'

def evalFunc(individual):
    #pass UCBFunctionToGet
    #play game n times with n seeds, return avg score overall
    seeds = random.sample(range(10000), number_of_games_per_worker)
    score = main(seeds, individual, False) 

    return score,

def originalMCTSFunc():
	new_individual = gp.PrimitiveTree.from_string("add(truediv(child_win_score, child_visit_count), (mul(1.414,sqrt(mul(2.0,truediv(log(current_visit_count),child_visit_count))))) )", pset)
	return new_individual

def eachGenResultsToWrite(toWriteHeader, g=None, num_sims=None, pop_size=None, pop=None, current_time=None):
	if(toWriteHeader):
		output_file = open(eachGenResults_file, 'w')
		output_file.write('GEN;num-games-each-worker-plays;pop-size;max-fitness;ellapsed-time;\n')
		output_file.close()
	else:
		output_file = open(eachGenResults_file, 'a')
		output_file.write(str(g) + ';' + str(num_sims) + ";" + str(pop_size) + ";" + str(max([p.fitness for p in pop])) + ';' + str(time.time()-current_time) + ';\n')
		output_file.close()

def writeOriginalEquations(pop):
	sys.stdout = open(originalEq_file, 'w')
	print('Original Individual;')
	for p in pop:
		print(str(p) + ';')
	sys.stdout = sys.__stdout__

def writeFinalEquations(pop):
	global toolbox

	sys.stdout = open(finalEq_file, 'w')
	print('Individual;Fitness;')
	for fp in toolbox.select(pop, k = 3):
		print(str(fp) + ";" + str(fp.fitness) + ";")
		print(str(prettyPrint(fp)) + ";" + str(fp.fitness) + ";\n")
	sys.stdout = sys.__stdout__

def createThePset():
	global pset

	# pset = gp.PrimitiveSetTyped('MAIN', [float, float, float, float], float)
	# pset.renameArguments(ARG0='child_win_score', ARG1='child_visit_count', ARG2='current_visit_count', ARG3='total_number_of_available_moves')
	
	pset = gp.PrimitiveSetTyped('MAIN', [float, float, float], float)
	pset.renameArguments(ARG0='child_win_score', ARG1='child_visit_count', ARG2='current_visit_count')
	pset.addPrimitive(operator.add, [float, float], float)
	pset.addPrimitive(operator.mul, [float, float], float)
	pset.addPrimitive(operator.truediv, [float, float], float)
	pset.addPrimitive(math.sqrt, [float], float)
	#pset.addPrimitive(math.log, [float], float)
	for i in range(10):
		pset.addTerminal(random.uniform(0, 10), float)

def createTheCreator():
	creator.create('FitnessMax', base.Fitness, weights=(1.0,))
	creator.create('Individual', gp.PrimitiveTree, fitness=creator.FitnessMax,
	              pset=pset)

def createTheToolbox():
	global toolbox
	toolbox = base.Toolbox()
	toolbox.register('compile', gp.compile, pset=pset)
	toolbox.register('indvCreation', individualCreation, pset=pset, min_=2, max_=6)
	toolbox.register('expr', gp.genHalfAndHalf, pset=pset, min_=2, max_=6)
	toolbox.register('individual', tools.initIterate, creator.Individual,
					toolbox.indvCreation)

	toolbox.register('evaluate', evalFunc)
	toolbox.register('map', pool.map)
		
	toolbox.register('population', tools.initRepeat, list, toolbox.individual)
	toolbox.register('select', tools.selBest)
	toolbox.register('mate', gp.cxOnePoint)
	toolbox.register('mutate', mutationFunction, expr=toolbox.expr, pset=pset)

	#for the single uct individual
	toolbox.register('create_initial_uct', originalMCTSFunc)
	toolbox.register('initial_uct', tools.initIterate, creator.Individual, toolbox.create_initial_uct)

def mutateConstant(individual, expr, pset):
	candidates = []
	for term in individual:
		if isinstance(term, gp.Terminal) and 'ARG' not in term.name:
			candidates.append((term, individual.index(term)))
    
	if len(candidates) == 0:
		return gp.mutUniform(individual, expr=expr, pset=pset)[0]
    
	chosen, index = random.choice(candidates)
	new_candidate = gp.PrimitiveTree(gp.genFull(pset=pset, max_=0, min_=0))
	while chosen.name == new_candidate[0].name or 'ARG' in new_candidate[0].name:
		new_candidate = gp.PrimitiveTree(gp.genFull(pset=pset, max_=0, min_=0))
        
	return gp.PrimitiveTree(individual[:index] + [new_candidate[0]] + individual[index+1:])

def mutationFunction(individual, expr, pset):
	r = random.uniform(0, 1)
	if r > 0.5:
		return mutateConstant(individual, expr, pset)
        
	return gp.mutUniform(individual, expr=expr, pset=pset)[0]

def individualCreation(pset, min_, max_):
	return simplifyFunction(gp.PrimitiveTree(toolbox.expr()))

def simplifyFunction(tree):
	global toolbox
	result = list(tree)
    
	offset = 0
    
	for i in range(0, len(tree)):
		index = i
		p = tree[i]
		subtree_slice = tree.searchSubtree(index)
		diff_index = subtree_slice.stop - subtree_slice.start - 1
		if diff_index <= 2 and diff_index > 0:
			temp = tree[subtree_slice.start+1:subtree_slice.stop]
            
			isReducible = True
            
			for i in temp:
				if not isinstance(i, gp.Terminal):
					isReducible = False
					break
				else:
					try:
						float(i.name)
					except:
						isReducible = False
						break
            
			if isReducible:
				subtree = [p] + temp
				subtree_ind = gp.PrimitiveTree(subtree)
				subtree_func = toolbox.compile(subtree_ind)
				subtree_result = subtree_func(0,0,0)
                
				new_terminal = gp.Terminal(subtree_result, False, float)
                
				result = result[:subtree_slice.start-offset] + [new_terminal] + result[subtree_slice.stop-offset:]
                
				offset += diff_index
    
	if len(tree) == len(result):
		return tree

	return creator.Individual(simplifyFunction(gp.PrimitiveTree(result)))

def produceCompiledPop(pop):
	func_globals = globals()
	func_globals['add'] = operator.add
	func_globals['mul'] = operator.mul
	func_globals['truediv'] = operator.truediv
	func_globals['sqrt'] = math.sqrt
	#func_globals['log'] = math.log

	compiled_pop = []
	for i in range(len(pop)):
		UCBFunc_code = marshal.dumps(toolbox.compile(pop[i]).__code__)
		compiled_pop.append(UCBFunc_code)

	# data_buffer = ""
	# for i in range(0, len(compiled_pop)):
	# 	data_buffer += str(compiled_pop[i])
	# 	if i < len(compiled_pop) - 1:
	# 		data_buffer += "\n"

	return compiled_pop

def initialPop():
	#create population
	#population of 5 so computer doesnt cry
	pop = toolbox.population (pop_size)
	#initial_uct_indiv = toolbox.initial_uct()
	#pop.append(initial_uct_indiv)
	# writeOriginalEquations(pop)
	return pop


if __name__ == "__main__":
	results_filename = str(uuid.uuid4()) + ".txt"
	temp_file = createFile(results_filename)

	eachGenResultsToWrite(True)

	pool = mp.Pool()
	#set up
	createThePset()
	createTheCreator()
	createTheToolbox()

	#then test generations
	#population of 5 so computer doesnt cry
	pop = initialPop()

	pop_data_buffer = ""
	for i in range(0, len(pop)):
		pop_data_buffer += str(pop[i])
		if i < len(pop) - 1:
			pop_data_buffer += "\n"
	output_file_pop = createFile("starting_gen_pop.txt")
	writeToFile(output_file_pop, 'Original Individual;')
	writeToFile(output_file_pop, pop_data_buffer)
	closeFile(output_file_pop)

	current_time = time.time()

	for g in range(ngen):
		compiled_pop = produceCompiledPop(pop)
		print("before map for gen", g)
		evals = toolbox.map(toolbox.evaluate, compiled_pop)
		print("after map for gen", g)
		for i in range(len(compiled_pop)):
			pop[i].fitness = evals[i]

		eachGenResultsToWrite(False, g=g, num_sims=number_of_games_per_worker, pop_size=pop_size, pop=pop, current_time=current_time)
		addToFileWithBreakline(results_filename, "Best for Generation " + str(g))
		for fp in toolbox.select(pop, k = int(len(pop))):
			addToFileWithBreakline(results_filename, (str(fp) + ";" + str(fp.fitness) + "; " + str(time.time() - current_time) + ";") )
		addToFile(results_filename, "\n")

		print('gen started')
		current_time = time.time()

		elite_size = int(len(pop) / 10)
		mutation_size = int(elite_size * 4.5)
		crossover_size = int(len(pop) - elite_size - mutation_size)
	
		elite = toolbox.select(pop, elite_size)

		candidates = toolbox.select(pop, int(len(pop) / 2))
		candidates = toolbox.clone(candidates)

		mutation_individuals = []
		sample_individuals_indexes = random.sample(range(int(len(pop) / 2)), mutation_size)
		for i in sample_individuals_indexes:
			mutation_individuals.append(simplifyFunction(toolbox.mutate(candidates[i])))

		candidates = toolbox.select(pop, int(len(pop) / 2))
		candidates = toolbox.clone(candidates)

		crossover_individuals = []
		pairings = tuple(itertools.combinations(candidates, 2))
			
		selected = random.sample(pairings, crossover_size)
		for pair in selected:
			try:
				child1, child2 = toolbox.mate(toolbox.clone(pair[0]), toolbox.clone(pair[1]))
				crossover_individuals.append(simplifyFunction(child1))
				if len(crossover_individuals) <= crossover_size - 1:
					crossover_individuals.append(simplifyFunction(child2))
				if len(crossover_individuals) == crossover_size:
					break
			except:
				raise

		pop = elite + mutation_individuals + crossover_individuals

		print('gen done')

	#the very last produced gen needs to be played
	print("playing last gen")
	compiled_pop = produceCompiledPop(pop)
	print("before map for gen", ngen)
	evals = toolbox.map(toolbox.evaluate, compiled_pop)
	print("after map for gen", ngen)
	for i in range(len(compiled_pop)):
		pop[i].fitness = evals[i]

	eachGenResultsToWrite(False, g=ngen, num_sims=number_of_games_per_worker, pop_size=pop_size, pop=pop, current_time=current_time)

	results_file = open('data/gen-results.csv.txt', 'a')
	results_file.write('Individual;Fitness;\n')
	for fp in toolbox.select(pop, k = len(pop)):
		results_file.write(str(fp) + ";" + str(fp.fitness) + ";\n")
		results_file.write(str(prettyPrint(fp)) + ";" + str(fp.fitness) + ";\n\n")
	results_file.close()

	for fp in toolbox.select(pop, k = int(len(pop))):
		addToFileWithBreakline(results_filename, (str(fp) + ";" + str(fp.fitness) + "; " + str(time.time() - current_time) + ";") )

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