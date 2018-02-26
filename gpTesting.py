import operator
import math
import game
import marshal
import random
import time
import uuid
from deap import base
from deap import creator
from deap import gp
from deap import tools
from deap import algorithms
import multiprocessing as mp
from prettyPrintTree import prettyPrint

from global_functions import *
from config import *
import consumer

#from contextlib import redirect_stdout
import sys

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

log_filename = "log.txt"

results_filename = "gen-output-" + str(uuid.uuid4()) + ".txt"

eachGenResults_file = 'data/output.csv.txt'
originalEq_file = 'data/original_population_eqs.csv.txt'
finalEq_file = 'data/gen-results.csv.txt'


def runConsumer(individual_spot, q):
	consumer.compute(individual_spot, q)

def evalFunc(individual, n):
	print("consumer playing game")
	#pass UCBFunctionToGet
	#play game n times with n seeds, return avg score overall
	score = game.main([0,n], individual, False)
	return score

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
	pset.addPrimitive(math.log, [float],float)
	pset.addTerminal(1.414, float)
	pset.addTerminal(0.5, float)
	pset.addTerminal(2.0, float)
	pset.addTerminal(3.0, float)
	pset.addTerminal(4.0, float)
	pset.addTerminal(5.0, float)

def createTheCreator():
	creator.create('FitnessMax', base.Fitness, weights=(1.0,))
	creator.create('Individual', gp.PrimitiveTree, fitness=creator.FitnessMax,
	              pset=pset)

def createTheToolbox():
	global toolbox
	toolbox = base.Toolbox()
	toolbox.register('compile', gp.compile, pset=pset)
	toolbox.register('expr', gp.genFull, pset=pset, min_=5, max_=5)
	toolbox.register('individual', tools.initIterate, creator.Individual,
	                toolbox.expr)

	toolbox.register('evaluate', evalFunc, n=num_sims)
	
	toolbox.register('working_workers', runConsumer, q=queue)
	
	toolbox.register('population', tools.initRepeat, list, toolbox.individual)
	toolbox.register('select', tools.selBest)
	toolbox.register('mate', gp.cxOnePoint)
	toolbox.register('mutate', gp.mutUniform, expr=toolbox.expr, pset=pset)

	toolbox.register('map', pool.map, chunksize=1)
	toolbox.register('map_async', pool.apply_async)
	#for the single uct individual
	toolbox.register('create_initial_uct', originalMCTSFunc)
	toolbox.register('initial_uct', tools.initIterate, creator.Individual, toolbox.create_initial_uct)



def produceCompiledPop(pop, current_iteration):
	func_globals = globals()
	func_globals['add'] = operator.add
	func_globals['mul'] = operator.mul
	func_globals['truediv'] = operator.truediv
	func_globals['sqrt'] = math.sqrt
	func_globals['log'] = math.log

	compiled_pop = []
	compiled_pop.append(str(current_iteration))
	for i in range(len(pop)):
		UCBFunc_code = marshal.dumps(toolbox.compile(pop[i]).__code__)
		compiled_pop.append(UCBFunc_code)

	#save current population equations
	output_file = createFile(output_filename)
	writeToFile(output_file, compiled_pop)
	closeFile(output_file)

	return compiled_pop

def initialPop():
	#create population
	#population of 5 so computer doesnt cry
	pop = toolbox.population (pop_size-1)
	initial_uct_indiv = toolbox.initial_uct()
	pop.append(initial_uct_indiv)
	writeOriginalEquations(pop)
	return pop

def getResultsFromFiles():
	evals = []
	
	for i in range(1, pop_size+1):
		file_pointer = openFile("output_"+str(i)+".txt")
		file_data = readFromFile(file_pointer)
		closeFile(file_pointer)

		evals.append(float(file_data[0]))
	return evals

if __name__ == "__main__":
	# eraseFile(log_filename)
	# temp_file = createFile(results_filename)
	# closeFile(temp_file)

	eachGenResultsToWrite(True)

	m = mp.Manager()
	queue = m.Queue()
	
	number_of_consumers = pop_size
	print(number_of_consumers)
	pool = mp.Pool(processes=number_of_consumers,  maxtasksperchild=1)
	
	#set up
	createThePset()
	createTheCreator()
	createTheToolbox()

	current_iteration = 1
	last_iteration = 0

	pop = None
	compiled_pop = None
	offspring = None
	
	while True:
		#first time
		if current_iteration == 1 and last_iteration == 0: 
			pop = initialPop()
			compiled_pop = produceCompiledPop(pop, current_iteration)
			#pool.map(runConsumer, range(1,len(compiled_pop)), chunksize=1)
			#toolbox.map(toolbox.working_workers,range(1,len(compiled_pop)))
			for i in range(1,len(compiled_pop)):
				pool.apply_async(runConsumer, args = (i, queue))
			
			last_iteration = current_iteration

		# log_file = openFile(log_filename)
		# log_data = readFromFile(log_file)
		# closeFile(log_file)
		# print("log file length", len(log_data))
		# eraseFile(log_filename)
		# print("prod queue size", queue.qsize())

		#all workers are done
		if queue.qsize() >= pop_size:
			#empty the queue
			while(queue.qsize() > 0):
				queue.get()
			evals = getResultsFromFiles()

			for i in range(len(evals)):
				pop[i].fitness = evals[i]
						
			print('gen started')
			current_time = time.time()
			pop = toolbox.select(pop, len(pop))

			offspring = toolbox.clone(pop)
			i = 0
			while i < len(offspring) - 1:
				random_n = random.uniform(0, 1)
				if random_n <= cxpb:
					ind1, ind2 = toolbox.mate(offspring[i], offspring[i+1])
					offspring[i] = ind1
					offspring[i+1] = ind2

				i += 2

			for i in range(len(offspring)):
				random_n = random.uniform(0, 1)
				if random_n <= mutpb:
					offspring[i] = toolbox.mutate(offspring[i])[0]

			print(pop)
			pop = offspring
			print(offspring)
			print('gen done')

			eachGenResultsToWrite(False, g=current_iteration, num_sims=num_sims+1, pop_size=pop_size, pop=pop, current_time=current_time)
			addToFile(results_filename, "Best for Generation " + str(current_iteration))
			for fp in toolbox.select(pop, k = 3):
				addToFile(results_filename, (str(fp) + ";" + str(fp.fitness))  )
			addToFile(results_filename, "\n")
			current_iteration += 1


		if current_iteration >= number_of_generations+1:
			break

		if current_iteration > last_iteration:
			print("Next Evolve")
			compiled_offspring = produceCompiledPop(offspring, current_iteration)
			last_iteration = current_iteration

		time.sleep(SLEEP_TIME_PRODUCER)
		
	print("FREE")

	
	

	# print("before map")
	# evals = toolbox.map(toolbox.evaluate, compiled_pop)
	# print("after map")
	# for i in range(len(compiled_pop)):
	#     pop[i].fitness = evals[i]

	# for g in range(ngen):
	#     print('gen started')
	#     current_time = time.time()
	#     pop = toolbox.select(pop, len(pop))

	#     offspring = toolbox.clone(pop)
	#     i = 0
	#     while i < len(offspring) - 1:
	#         random_n = random.uniform(0, 1)
	#         if random_n <= cxpb:
	#             ind1, ind2 = toolbox.mate(offspring[i], offspring[i+1])
	#             offspring[i] = ind1
	#             offspring[i+1] = ind2

	#         i += 2

	#     for i in range(len(offspring)):
	#         random_n = random.uniform(0, 1)
	#         if random_n <= mutpb:
	#             offspring[i] = toolbox.mutate(offspring[i])[0]

	#     compiled_offspring = []
	#     for i in range(len(offspring)):
	#         UCBFunc_code = marshal.dumps(toolbox.compile(offspring[i]).__code__)

	#         compiled_offspring.append(UCBFunc_code)

	#     evals = toolbox.map(toolbox.evaluate, compiled_offspring)
	#     for i in range(len(compiled_offspring)):
	#         offspring[i].fitness = evals[i]

	#     pop = offspring

	#     print('gen done')

	#     eachGenResultsToWrite(False, g=g, num_sims=num_sims+1, pop_size=pop_size, pop=pop, current_time=current_time)
	
	writeFinalEquations(pop)

	pool.terminate()

	print('done')

