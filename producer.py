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
#import multiprocessing as mp
from prettyPrintTree import prettyPrint

from global_functions import *
from config import *

import sys

import sympy
from sympy import Symbol, sqrt
from sympy.parsing.sympy_parser import parse_expr

#global variables
pool = None
pset = None
toolbox = None

num_sims = number_of_games_per_worker
pop_size = number_of_individuals

cxpb=0.5
mutpb=0.2
ngen=number_of_generations

#files
current_directory = "data/generation-0/"

input_filename_prefix = "ind-"
input_filename_sufix = ".txt"

output_filename = "test.txt"

results_filename = "data/gen-output-" + str(uuid.uuid4()) + ".txt"
temp_file = createFile(results_filename)
closeFile(temp_file)

total = 0.0

# output_filename = "current_gen_info.txt"
# time.sleep(0.5)

# consumer_gen_file = "consumer_current_gen_info.txt"
# createFile(consumer_gen_file)
# time.sleep(0.5)


eachGenResults_file = 'data/output.csv.txt'
originalEq_file = 'data/original_population_eqs.csv.txt'
finalEq_file = 'data/gen-results.csv.txt'


child_win_score = Symbol('child_win_score')
child_visit_count = Symbol('child_visit_count')
current_visit_count = Symbol('current_visit_count')
total_number_of_available_moves = Symbol('total_number_of_available_moves')
ARG3 = Symbol('ARG3')

def originalMCTSFunc():
	new_individual = gp.PrimitiveTree.from_string("add(truediv(child_win_score, child_visit_count), (mul(1.414,sqrt(mul(2.0,truediv(log(current_visit_count),child_visit_count))))) )", pset)
	return new_individual

def eachGenResultsToWrite(toWriteHeader, g=None, num_sims=None, pop_size=None, pop_highscore=None, current_time=None):
	if(toWriteHeader):
		sys.stdout = open(eachGenResults_file, 'w')
		print('GEN;num-sims;pop-size;max-fitness;ellapsed-time;')
	else:
		sys.stdout = open(eachGenResults_file, 'a')
		print(str(g) + ';' + str(num_sims) + ";" + str(pop_size) + ";" + str(pop_highscore) + ';' + str(current_time) + ';')
	sys.stdout = sys.__stdout__

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

	pset = gp.PrimitiveSetTyped('MAIN', [float, float, float, float], float)
	pset.renameArguments(ARG0='child_win_score', ARG1='child_visit_count', ARG2='current_visit_count', ARG3='total_number_of_available_moves')
	# pset = gp.PrimitiveSetTyped('MAIN', [float, float, float], float)
	# pset.renameArguments(ARG0='child_win_score', ARG1='child_visit_count', ARG2='current_visit_count')
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
	indiv = simplifyFunction(gp.PrimitiveTree(toolbox.expr())) 
	
	while(isinstance(indiv[0], gp.Terminal)):
		indiv = simplifyFunction(gp.PrimitiveTree(toolbox.expr())) 
	
	return indiv

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
				subtree_result = subtree_func(0,0,0, 0)
                
				new_terminal = gp.Terminal(subtree_result, False, float)
                
				result = result[:subtree_slice.start-offset] + [new_terminal] + result[subtree_slice.stop-offset:]
                
				offset += diff_index
    
	if len(tree) == len(result):
		return tree

	return creator.Individual(simplifyFunction(gp.PrimitiveTree(result)))

def produceCompiledPop(pop, current_iteration):
	func_globals = globals()
	func_globals['add'] = operator.add
	func_globals['mul'] = operator.mul
	func_globals['truediv'] = operator.truediv
	func_globals['sqrt'] = math.sqrt
	#func_globals['log'] = math.log

	compiled_pop = []
	compiled_pop.append(str(current_iteration))
	for i in range(len(pop)):
		UCBFunc_code = marshal.dumps(toolbox.compile(pop[i]).__code__)
		compiled_pop.append(UCBFunc_code)

	data_buffer = ""
	for i in range(0, len(compiled_pop)):
		data_buffer += str(compiled_pop[i])
		if i < len(compiled_pop) - 1:
			data_buffer += "\n"

	#save current population equations
	# lock = LockFile("data/" + output_filename)
	# lock.acquire()
	#delete current content
	# fd = open("data/" + output_filename, "r+")
	# fd.seek(0)
	# fd.truncate()
	#output_file = createFile(output_filename)
	# writeToFile(fd, data_buffer)
	# closeFile(fd)
	# lock.release()

	return data_buffer

def initialPop():
	#create population
	#population of 5 so computer doesnt cry
	pop = toolbox.population (number_of_individuals)
	
	#check for duplicates
	indiv_to_pop = []
	for i in range(1, len(pop)):
		indiv_1 = parse_expr(prettyPrint(pop[i]))
		for j in range(0, i):
			indiv_2 = parse_expr(prettyPrint(pop[j]))
			if indiv_1 - indiv_2 == 0:
				indiv_to_pop.append(pop[i])
	
	for i in indiv_to_pop:
		pop.remove(i)

	while(len(pop) < number_of_individuals):
		indiv = simplifyFunction(gp.PrimitiveTree(toolbox.expr())) 
		while(isinstance(indiv[0], gp.Terminal)):
			indiv = simplifyFunction(gp.PrimitiveTree(toolbox.expr())) 
		add_to_pop = True
		indiv_to_check = parse_expr(prettyPrint(indiv))
		for i in pop:
			indiv_before = parse_expr(prettyPrint(i))
			if indiv_to_check - indiv_before == 0:
				add_to_pop = False
				break
		if add_to_pop:
			pop.append(indiv)
	#initial_uct_indiv = toolbox.initial_uct()
	#pop.append(initial_uct_indiv)
	# writeOriginalEquations(pop)
	return pop


def getResultsFromFiles():
	evals = []
	
	"data/generation-0/ind-#.txt"
	for i in range(number_of_individuals):
		input_file = openFile(current_directory + input_filename_prefix + str(i) + input_filename_sufix)
		input_data = readLineFromFile(input_file)
		closeFile(input_file)
		
		# temp_data = [float(x) for x in input_data]
		#input_data guaranteeded to have at least number_of_simulations guys
		#temp_data = [float(input_data[x]) for x in range(0, number_of_simulations)]
		temp_data = []
		for x in range(0, number_of_simulations):
			temp_data.append(float(input_data[x]))
		average = sum(temp_data) / float(len(temp_data))
		
		evals.append(float(average))
	
	return evals

if __name__ == "__main__":
	#set up
	createThePset()
	createTheCreator()
	createTheToolbox()

	current_iteration = 1
	last_iteration = 0	

	pop = None
	compiled_pop = None
	offspring = None
		
	start = time.time()

	start_from_previous_gen = True

	if start_from_previous_gen:
		if current_iteration == 1:
			current_directory = "data/generation-" + str(current_iteration) + "/"
			#find the generation we left off at + 1
			while(os.path.exists(current_directory)):
				current_iteration += 1
				current_directory = "data/generation-" + str(current_iteration) + "/"
			#for example, we stopped at generation 72
			#generation 71 is finished and we were in middle of generation 72
			#so current_iteration will be 73
			#go back one to finish up generation 72
			current_iteration -= 1
			current_directory = "data/generation-" + str(current_iteration) + "/"

			#produce(); read data from file named my_pop.txt
			test_pointer = openFile("data/generation-" + str(current_iteration) + "/" + "my_pop.txt")
			pop = readFromFile(test_pointer)
			closeFile(test_pointer)
			for i in range(0, len(pop)):
				pop[i] = creator.Individual(gp.PrimitiveTree.from_string(pop[i], pset))
	else:
		if current_iteration == 1:
			eachGenResultsToWrite(True)
			
			current_directory = "data/generation-" + str(current_iteration) + "/"
			if not os.path.exists(current_directory):
				os.makedirs(current_directory)
			#produce()
			pop = initialPop()
			#create the file for the population
			pop_data_buffer = ""
			for i in range(0, len(pop)):
				pop_data_buffer += str(pop[i])
				if i < len(pop) - 1:
					pop_data_buffer += "\n"
			output_file_pop = createFile(current_directory + "my_pop.txt")
			writeToFile(output_file_pop, pop_data_buffer)
			closeFile(output_file_pop)

			compiled_pop = produceCompiledPop(pop, current_iteration)
			output_file = createFile(current_directory + output_filename)
			writeToFile(output_file, compiled_pop)
			closeFile(output_file)

	
	last_iteration = current_iteration
	
	
	spacing_from_total_games_worker_play = 20 # 100 / 5 = 20

	while True:
		# length_of_data_1 = 0
		# length_of_data_2 = 0
		length_of_data_array = [0] * spacing_from_total_games_worker_play
		failed = 0
		try:
			for i in range(0, spacing_from_total_games_worker_play):
				failed = i
				test_pointer = openFile(current_directory + "ind-" + str(number_of_individuals-i-1) + ".txt")
				test_data = readLineFromFile(test_pointer)
				closeFile(test_pointer)
				length_of_data_array[i] = len(test_data)
			
		except:
			print ("File", current_directory + "ind-" + str(failed) + ".txt", " doesn't exist")
			time.sleep(SLEEP_TIME_PRODUCER)
			continue

		print ("Data len: ", float(sum(length_of_data_array)) / len(length_of_data_array))
		print ("all done", all(i >= number_of_simulations for i in length_of_data_array))
		if all(i >= number_of_simulations for i in length_of_data_array):
		#if length_of_data_1 >= number_of_simulations and length_of_data_2 >= number_of_simulations:
			print("Compiling generation ", current_iteration)
			evals = getResultsFromFiles()

			for i in range(len(evals)):
				pop[i].fitness = (evals[i],)	#for maximizing score
				# pop[i].fitness = (-1 * evals[i],) #for minimizing score

			addToFileWithBreakline(results_filename, "Best for Generation " + str(current_iteration))
			for fp in toolbox.select(pop, k = int(len(pop))):
				addToFileWithBreakline(results_filename, (str(fp) + ";" + str(fp.fitness) + "; " + str(time.time() - start) + ";") )

			max_score = max([p.fitness for p in pop])
			print("old max", Board.winning_score)
			if (max_score[0] > Board.winning_score):
				Board.winning_score = max_score[0]
				print("change to score")
			print("new max", Board.winning_score)
			addToFile(results_filename, "\n")
			eachGenResultsToWrite(False, g=current_iteration, num_sims=num_sims, pop_size=pop_size, pop_highscore=max_score, current_time=str(time.time() - start))
			start = time.time()
			current_iteration += 1

		if current_iteration >= number_of_generations+1:
			break
	
		if current_iteration > last_iteration:
			print("Making new generation ", current_iteration)

			elite_size = int(len(pop) / 10)
			mutation_size = int(elite_size * 4.5)
			crossover_size = int(len(pop) - elite_size - mutation_size)
		
			current_time = time.time()
			elite = toolbox.select(pop, elite_size)

			candidates = toolbox.select(pop, int(len(pop) / 2))
			candidates = toolbox.clone(candidates)

			mutation_individuals = []
			sample_individuals_indexes = random.sample(range(int(len(pop) / 2)), mutation_size)
			curr_index = 0
			while curr_index < len(sample_individuals_indexes):
			# for i in sample_individuals_indexes:
				i = sample_individuals_indexes[curr_index]
				mutated_individual = simplifyFunction(toolbox.mutate(candidates[i]))

				while( isinstance(mutated_individual[0], gp.Terminal) ):
					mutated_individual = simplifyFunction(toolbox.mutate(candidates[i]))

				#check the mutated_indiv against previous guys and elitist
				mutated_individual_dup = parse_expr(prettyPrint(mutated_individual))
				passed_elitist = True
				for e in elite:
					elitist = parse_expr(prettyPrint(e))
					if mutated_individual_dup - elitist == 0:
						passed_elitist = False
						break

				add_to_mutated = True
				if passed_elitist:
					if len(mutation_individuals) > 0:
						for m in mutation_individuals:
							curr_m = parse_expr(prettyPrint(m))
							if mutated_individual_dup - curr_m == 0:
								add_to_mutated = False
								break
					if add_to_mutated:
						mutation_individuals.append(mutated_individual)
						curr_index += 1

			candidates = toolbox.select(pop, int(len(pop) / 2))
			candidates = toolbox.clone(candidates)

			crossover_individuals = []
			pairings = list(itertools.combinations(candidates, 2))
			
			random.shuffle(pairings)
			selected = pairings
			crossover_size_copy = crossover_size
			counter = 0
			while counter < crossover_size_copy:
				child1, child2 = toolbox.mate(toolbox.clone(selected[counter][0]), toolbox.clone(selected[counter][1]))
				child1 = simplifyFunction(child1)
				child2 = simplifyFunction(child2)
				while(isinstance(child1[0], gp.Terminal) or isinstance(child2[0], gp.Terminal) ):
					counter += 1
					crossover_size_copy += 1
					child1, child2 = toolbox.mate(toolbox.clone(selected[counter][0]), toolbox.clone(selected[counter][1]))
					child1 = simplifyFunction(child1)
					child2 = simplifyFunction(child2)

				child1_dup = parse_expr(prettyPrint(child1))
				child2_dup = parse_expr(prettyPrint(child2))
				#check cross over guys against elitist
				passed_elitist = True
				passed_mutated = True
				for e in elite:
					elitist = parse_expr(prettyPrint(e))
					if child1_dup - elitist == 0 or child2_dup - elitist == 0:
						passed_elitist = False
						break
				#check against mutated
				if passed_elitist:
					for m in mutation_individuals:
						curr_m = parse_expr(prettyPrint(m))
						if child1_dup - curr_m == 0 or child2_dup - elitist == 0:
							passed_mutated = False
							break
					add_to_crossover = True
					#check against prev cross overs
					if passed_mutated:
						for c in crossover_individuals:
							curr_c = parse_expr(prettyPrint(c))
							if child1_dup - curr_c == 0 or child2_dup - curr_c == 0:
								add_to_crossover = False
								break
						if add_to_crossover:
							crossover_individuals.append(simplifyFunction(child1))
							if len(crossover_individuals) <= crossover_size - 1:
								crossover_individuals.append(simplifyFunction(child2))
							if len(crossover_individuals) == crossover_size:
								break

							counter +=1

			pop = elite + mutation_individuals + crossover_individuals

			current_directory = "data/generation-" + str(current_iteration) + "/"
			if not os.path.exists(current_directory):
				os.makedirs(current_directory)
			#produce()
			pop_data_buffer = ""
			for i in range(0, len(pop)):
				pop_data_buffer += str(pop[i])
				if i < len(pop) - 1:
					pop_data_buffer += "\n"
			output_file_pop = createFile(current_directory + "my_pop.txt")
			writeToFile(output_file_pop, pop_data_buffer)
			closeFile(output_file_pop)

			compiled_pop = produceCompiledPop(pop, current_iteration)
			output_file = createFile(current_directory + output_filename)
			writeToFile(output_file, compiled_pop)
			closeFile(output_file)
			
			last_iteration = current_iteration
		
		time.sleep(SLEEP_TIME_PRODUCER)