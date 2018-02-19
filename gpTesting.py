import operator
import math
import game
import marshal
import random
import time
from deap import base
from deap import creator
from deap import gp
from deap import tools
from deap import algorithms

from prettyPrintTree import prettyPrint

from contextlib import redirect_stdout

import multiprocessing as mp

#toolbox.evaluate 

def evalFunc(individual, n):
    #print (prettyPrint(individual))
    #print (individual)
    #UCBFunctionToGet = toolbox.compile(individual)
    #pass UCBFunctionToGet
    #play game n times with n seeds, return avg score overall
    n = 1
    score = game.main([0,n], individual, False)

    return score,

def originalMCTSFunc():
	new_individual = gp.PrimitiveTree.from_string("add(truediv(child_win_score, child_visit_count), (mul(1.414,sqrt(mul(2.0,truediv(log(current_visit_count),child_visit_count))))) )", pset)

	#UCBFunctionToGet = toolbox.compile(new_individual)
	#print(UCBFunctionToGet(2,3,4),)

	return new_individual

def eachGenResultsToWrite(toWriteHeader, g=None, num_sims=None, pop_size=None, pop=None, current_time=None):
	if(toWriteHeader):
		output_file = open('output.csv.txt', 'w')
		output_file.write('GEN;num-sims;pop-size;max-fitness;ellapsed-time;\n')
		output_file.close()
	else:
		output_file = open('output.csv.txt', 'a')
		output_file.write(str(g) + ';' + str(num_sims) + ";" + str(pop_size) + ";" + str(max([p.fitness for p in pop])) + ';' + str(time.time()-current_time) + ';\n')
		output_file.close()


if __name__ == "__main__":
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

	num_sims = 1
	toolbox.register('evaluate', evalFunc, n=num_sims)

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
	pop_size = 5
	pop = toolbox.population (pop_size-1)
	pop.append(initial_uct_indiv)

	#final_pop = algorithms.eaSimple(pop, toolbox=toolbox, cxpb=0.5, mutpb=0.2, ngen=2)
	
	results_file = open('gen-results.csv.txt', 'w')
	results_file.write('Original Individual;\n')
	for p in pop:
		results_file.write(str(p) + ';\n')
		results_file.write(prettyPrint(p) + ';\n\n')
	results_file.write('\n\n')
	results_file.close()

	cxpb=0.5
	mutpb=0.2
	ngen=5

	func_globals = globals()
	func_globals['add'] = operator.add
	func_globals['mul'] = operator.mul
	func_globals['truediv'] = operator.truediv
	func_globals['sqrt'] = math.sqrt
	func_globals['log'] = math.log

	compiled_pop = []
	for i in range(len(pop)):
	    UCBFunc_code = marshal.dumps(toolbox.compile(pop[i]).__code__)

	    compiled_pop.append(UCBFunc_code)

	#output_file = open('output.csv.txt', 'w')
	#output_file.write('GEN;num-sims;pop-size;max-fitness;ellapsed-time;\n')
	#output_file.close()
	eachGenResultsToWrite(toWriteHeader=True)

	print("before map")
	evals = toolbox.map(toolbox.evaluate, compiled_pop)
	print("after map")
	for i in range(len(compiled_pop)):
	    pop[i].fitness = evals[i]

	for g in range(ngen):
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

	    compiled_offspring = []
	    for i in range(len(offspring)):
	        UCBFunc_code = marshal.dumps(toolbox.compile(offspring[i]).__code__)

	        compiled_offspring.append(UCBFunc_code)

	    evals = toolbox.map(toolbox.evaluate, compiled_offspring)
	    for i in range(len(compiled_offspring)):
	        offspring[i].fitness = evals[i]

	    pop = offspring

	    print('gen done')

	    eachGenResultsToWrite(False, g=g, num_sims=num_sims+1, pop_size=pop_size, pop=pop, current_time=current_time)
	    # output_file = open('output.csv.txt', 'a')
	    # output_file.write(str(g) + ';' + str(num_sims) + ";" + str(pop_size) + ";" + str(max([p.fitness for p in pop])) + ';' + str(time.time()-current_time) + ';\n')
	    # output_file.close()

	results_file = open('gen-results.csv.txt', 'a')
	results_file.write('Individual;Fitness;\n')
	for fp in toolbox.select(pop, k = 3):
		results_file.write(str(fp) + ";" + str(fp.fitness) + ";\n")
		results_file.write(str(prettyPrint(fp)) + ";" + str(fp.fitness) + ";\n\n")
	results_file.close()

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