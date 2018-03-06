import operator
import math
import game
import marshal
import random
import time
import uuid
import itertools
from deap import base
from deap import creator
from deap import gp
from deap import tools
from deap import algorithms
#import multiprocessing as mp
from prettyPrintTree import prettyPrint

from global_functions import *
from config import *
import consumer

#from contextlib import redirect_stdout
import sys
from lockfile import LockFile


#global variables
pool = None
pset = None
toolbox = None

num_sims = number_of_games_per_worker
pop_size = population_size

cxpb=0.5
mutpb=0.2
ngen=number_of_generations

#files
output_filename = "current_gen_info.txt"
createFile(output_filename)
time.sleep(0.5)

consumer_gen_file = "consumer_current_gen_info.txt"
createFile(consumer_gen_file)
time.sleep(0.5)

log_filename = "log.txt"

results_filename = "gen-output-" + str(uuid.uuid4()) + ".txt"

eachGenResults_file = 'data/output.csv.txt'
originalEq_file = 'data/original_population_eqs.csv.txt'
finalEq_file = 'data/gen-results.csv.txt'


def originalMCTSFunc():
	new_individual = gp.PrimitiveTree.from_string("add(truediv(child_win_score, child_visit_count), (mul(1.414,sqrt(mul(2.0,truediv(log(current_visit_count),child_visit_count))))) )", pset)
	return new_individual

def eachGenResultsToWrite(toWriteHeader, g=None, num_sims=None, pop_size=None, pop=None, current_time=None):
	if(toWriteHeader):
		sys.stdout = open(eachGenResults_file, 'w')
		print('GEN;num-sims;pop-size;max-fitness;ellapsed-time;')
	else:
		sys.stdout = open(eachGenResults_file, 'a')
		print(str(g) + ';' + str(num_sims) + ";" + str(pop_size) + ";" + str(max([p.fitness for p in pop])) + ';' + str(time.time()-current_time) + ';')
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

def deleteContent(fd):
    os.ftruncate(fd, 0)
    os.lseek(fd, 0, os.SEEK_SET)

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
	for i in compiled_pop:
		data_buffer += str(i) + "\n"

	#save current population equations
	lock = LockFile("data/" + output_filename)
	lock.acquire()
	#delete current content
	fd = open("data/" + output_filename, "r+")
	fd.seek(0)
	fd.truncate()
	#output_file = createFile(output_filename)
	writeToFile(fd, data_buffer)
	closeFile(fd)
	lock.release()

	return compiled_pop

def initialPop():
	#create population
	#population of 5 so computer doesnt cry
	pop = toolbox.population (pop_size)
	#initial_uct_indiv = toolbox.initial_uct()
	#pop.append(initial_uct_indiv)
	writeOriginalEquations(pop)
	return pop

def getResultsFromFiles(compiled_pop, log_data):
	evals = []
	
	# eraseFile("fk.txt")

	for individual in compiled_pop:
		for consumer_individual in log_data:
			left_side_consumer_indiv = consumer_individual[:consumer_individual.rfind(";")]
			if (left_side_consumer_indiv == str(individual)):
				evals.append(float(consumer_individual[consumer_individual.rfind(";")+1:]))
				break
			
			
	return evals

if __name__ == "__main__":
	eraseFile(log_filename)

	temp_file = createFile(results_filename)
	closeFile(temp_file)

	eachGenResultsToWrite(True)

	#set up
	createThePset()
	createTheCreator()
	createTheToolbox()

	current_iteration = 1
	last_iteration = 0

	pop = None
	compiled_pop = None
	offspring = None
	
	current_time = time.time()

	while True:
		#first time
		if current_iteration == 1 and last_iteration == 0: 
			pop = initialPop()
			compiled_pop = produceCompiledPop(pop, current_iteration)
			last_iteration = current_iteration

		consumer_data_lock = LockFile("data/"+consumer_gen_file)
		consumer_data_lock.acquire()
		log_file = openFile(consumer_gen_file)
		log_data = readFromFile(log_file)
		closeFile(log_file)
		consumer_data_lock.release()
		
		#all workers are done
		if len(log_data) == pop_size:
			consumer_data_lock.acquire()
			eraseFile(consumer_gen_file)
			consumer_data_lock.release()
			evals = getResultsFromFiles(compiled_pop[1:], log_data)

			for i in range(len(evals)):
				pop[i].fitness = (evals[i],)

			eachGenResultsToWrite(False, g=current_iteration, num_sims=num_sims, pop_size=pop_size, pop=pop, current_time=current_time)
			addToFile(results_filename, "Best for Generation " + str(current_iteration))
			for fp in toolbox.select(pop, k = 3):
				addToFile(results_filename, (str(fp) + ";" + str(fp.fitness))  )
			addToFile(results_filename, "\n")

			current_iteration += 1

			if (current_iteration >= number_of_generations+1):
				break

			elite_size = int(len(pop) / 10)
			mutation_size = int(elite_size * 4.5)
			crossover_size = int(len(pop) - elite_size - mutation_size)
		
			current_time = time.time()
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
					
		if current_iteration > last_iteration:
			print("Next Evolve")
			compiled_pop = produceCompiledPop(pop, current_iteration)
			last_iteration = current_iteration
			print("Made Next Evolve")

		if current_iteration >= number_of_generations+1:
			break

		time.sleep(SLEEP_TIME_PRODUCER)
			
	writeFinalEquations(pop)

	lock = LockFile("data/" + output_filename)
	lock.acquire()
	fd = open("data/" + output_filename, "r+")
	fd.seek(0)
	fd.truncate()
	#output_file = createFile(output_filename)
	writeToFile(fd, str(current_iteration))
	closeFile(fd)
	lock.release()

	print('done')
