import operator

from deap import base
from deap import creator
from deap import gp
from deap import tools
from deap import algorithms

#pset = gp.PrimitiveSet(“MAIN”, arity=1)

def findMax(a, b):
   return max([a, b])

pset = gp.PrimitiveSetTyped('MAIN', [int, int], int)
pset.renameArguments(ARG0='child_win_ratio', ARG1='y')
pset.addPrimitive(operator.add, [int, int], int)
pset.addPrimitive(operator.sub, [int, int], int)
pset.addPrimitive(operator.mul, [int, int], int)
pset.addPrimitive(findMax, [int, int], int)
pset.addTerminal(5, int)
pset.addTerminal(10, int)


creator.create('FitnessMax', base.Fitness, weights=(1.0,))
creator.create('Individual', gp.PrimitiveTree, fitness=creator.FitnessMax,
              pset=pset)

toolbox = base.Toolbox()
toolbox.register('compile', gp.compile, pset=pset)
toolbox.register('expr', gp.genFull, pset=pset, min_=2, max_=2)
toolbox.register('individual', tools.initIterate, creator.Individual,
                toolbox.expr)


#new_individual = gp.PrimitiveTree.from_string("add(ARG0, 10)", pset)

toolbox.register('population', tools.initRepeat, list, toolbox.individual)
toolbox.register('select', tools.selBest)
toolbox.register('mate',gp.cxOnePoint)
toolbox.register('mutate',gp.mutUniform, expr=toolbox.expr, pset=pset)

def evalFunc(ind):
	func = toolbox.compile(ind)

	return (func(100, 200),)

toolbox.register('evaluate',evalFunc)

pop = toolbox.population(100)

#print (pop[0])
#print (pop[1])
#print (toolbox.mate(pop[0], pop[1])[0])
#print (toolbox.mate(pop[0], pop[1])[1])
#print al(toolbox.mutate(pop[0])[0])

final_pop = algorithms.eaSimple(pop, toolbox, cxpb=0.5, mutpb=0.2, ngen=100)

for fp in toolbox.select(final_pop[0], k=3):
	print (fp)
	print (fp.fitness)