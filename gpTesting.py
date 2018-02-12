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