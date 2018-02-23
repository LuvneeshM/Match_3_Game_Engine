import operator

from deap import base
from deap import creator
from deap import gp
from deap import tools
from deap import algorithms

#pset = gp.PrimitiveSet("MAIN", arity=1)

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

toolbox.register('population', tools.initRepeat, list, toolbox.individual)
toolbox.register('select', tools.selBest)
toolbox.register('mate',gp.cxOnePoint)
toolbox.register('mutate',gp.mutUniform, expr=toolbox.expr, pset=pset)

def evalFunc(ind):
	func = toolbox.compile(ind)

	return (func(100, 200),)

toolbox.register('evaluate',evalFunc)

pop = toolbox.population(10)

print("testing start")

def gen_indiv():
	return gp.PrimitiveTree.from_string("add(child_win_ratio, 10)", pset)

toolbox.register('initial_uct', gen_indiv)
toolbox.register('indiv_uct', tools.initIterate, creator.Individual, toolbox.initial_uct)


test = toolbox.indiv_uct()
print(type(test))
print(test)
pop.append(test)
print(pop[len(pop)-1])
print("testing end")

#new_individual = gp.PrimitiveTree.from_string("add(child_win_ratio, 10)", pset)

pop.append(test)

#print (pop[0])
#print (toolbox.evaluate(pop[0]))
#print (pop[1])
#print (toolbox.mate(pop[0], pop[1])[0])
#print (toolbox.mate(pop[0], pop[1])[1])
#print (toolbox.mutate(pop[0])[0])

final_pop = algorithms.eaSimple(pop, toolbox, cxpb=0.5, mutpb=0.2, ngen=5)

for fp in toolbox.select(final_pop[0], k=3):
	print (fp)
	print (fp.fitness)