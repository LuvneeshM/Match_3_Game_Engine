import operator
import math
import game
from deap import base
from deap import creator
from deap import gp
from deap import tools
from deap import algorithms


#pset = gp.PrimitiveSet(“MAIN”, arity=1)

def findMax(a, b):
   return max([a, b])

def gpStuff():
	pset = gp.PrimitiveSetTyped('MAIN', [float, float, float], float)
	pset.renameArguments(ARG0='child_win_score', ARG1='child_visit_count', ARG2='current_visit_count')
	pset.addPrimitive(operator.add, [float, float], float)
	pset.addPrimitive(operator.mul, [float, float], float)
	pset.addPrimitive(operator.truediv, [float, float], float)
	pset.addPrimitive(operator.pow, [float, float], float)
	pset.addPrimitive(math.log, [float],float)
	#pset.addPrimitive(findMax, [int, int], int)
	#pset.addTerminal(5, int)
	#pset.addTerminal(10, int)

	creator.create('FitnessMax', base.Fitness, weights=(1.0,))
	creator.create('Individual', gp.PrimitiveTree, fitness=creator.FitnessMax,
	              pset=pset)

	toolbox = base.Toolbox()
	toolbox.register('compile', gp.compile, pset=pset)
	toolbox.register('expr', gp.genFull, pset=pset, min_=1, max_=1)
	toolbox.register('individual', tools.initIterate, creator.Individual,
	                toolbox.expr)

	new_individual = gp.PrimitiveTree.from_string("add(truediv(child_win_score, child_visit_count), (mul(1.414,pow(mul(2.0,truediv(log(current_visit_count),child_visit_count)),0.5))) )", pset)

	UCBFunctionToGet = toolbox.compile(new_individual)
	#print(UCBFunctionToGet(2,3,4),)

	return UCBFunctionToGet


def evaluate(individual, n, logData):
	#pass UCBFunctionToGet
	#play game n times with n seeds, return avg score overall

	game.main([0,n], individual, logData)


if __name__ == '__main__':
	indiv = gpStuff()
	evaluate(indiv, 1, True)


'''
toolbox.register('population', tools.initRepeat, list, toolbox.individual)
toolbox.register('select', tools.selBest)
toolbox.register('mate',gp.cxOnePoint)
toolbox.register('mutate',gp.mutUniform, expr=toolbox.expr, pset=pset)

def evalFunc(ind):
	func = toolbox.compile(ind)

	return (func(2, 3, 4),)

toolbox.register('evaluate',evalFunc)

#pop = toolbox.population(5)

#print (pop[0])
#print(toolbox.evaluate(pop[0]))
#print (pop[1])
#print (toolbox.evaluate(pop[1]))
#print (toolbox.mate(pop[0], pop[1])[0])
#print (toolbox.mate(pop[0], pop[1])[1])
#print (toolbox.mutate(pop[0])[0])

#final_pop = algorithms.eaSimple(pop, toolbox, cxpb=0.5, mutpb=0.2, ngen=100)

#for fp in toolbox.select(final_pop[0], k=3):
#	print (fp)
#	print (fp.fitness)
'''