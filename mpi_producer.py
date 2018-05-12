#import pyximport; pyximport.install()
from cythoned import *

import operator
import math
import marshal
import random
import time
import uuid
import itertools
import os
import mpi_consumer
from deap import base
from deap import creator
from deap import gp
from deap import tools
from deap import algorithms
from prettyPrintTree import prettyPrint

from global_functions import *
from config import *

import sys

import sympy
from sympy import Symbol, sqrt
from sympy.parsing.sympy_parser import parse_expr

from mpi4py import MPI

#global variables
pool = None
pset = None
toolbox = None

num_sims = number_of_games_per_worker
pop_size = number_of_individuals

cxpb=0.5
mutpb=0.2
ngen=number_of_generations

child_win_score = Symbol('child_win_score')
child_visit_count = Symbol('child_visit_count')
current_visit_count = Symbol('current_visit_count')
total_number_of_available_moves = Symbol('total_number_of_available_moves')
ARG3 = Symbol('ARG3')

def eachGenResultsToWrite(toWriteHeader, g=None, num_sims=None, pop_size=None, pop_highscore=None, current_time=None):
	if(toWriteHeader):
		sys.stdout = open(eachGenResults_file, 'w')
		print('GEN;num-sims;pop-size;max-fitness;ellapsed-time;')
	else:
		sys.stdout = open(eachGenResults_file, 'a')
		print(str(g) + ';' + str(num_sims) + ";" + str(pop_size) + ";" + str(pop_highscore) + ';' + str(current_time) + ';')
	sys.stdout = sys.__stdout__

def createThePset():
	global pset

	pset = gp.PrimitiveSetTyped('MAIN', [float, float, float, float], float)
	pset.renameArguments(ARG0='child_win_score', ARG1='child_visit_count', ARG2='current_visit_count', ARG3='total_number_of_available_moves')

	pset.addPrimitive(operator.add, [float, float], float)
	pset.addPrimitive(operator.mul, [float, float], float)
	pset.addPrimitive(operator.truediv, [float, float], float)
	pset.addPrimitive(math.sqrt, [float], float)

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

	return data_buffer

def initialPop():
	#create population
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
	
	return pop

def getResultsFromFiles():
	evals = []
	
	"data/generation-0/ind-#.txt"
	for i in range(number_of_individuals):
		input_file = openFile(current_directory + input_filename_prefix + str(i) + input_filename_sufix)
		input_data = readLineFromFile(input_file)
		closeFile(input_file)
		
		#input_data guaranteeded to have at least number_of_simulations guys
		temp_data = []
		for x in range(0, number_of_simulations):
			temp_data.append(float(input_data[x]))
		average = sum(temp_data) / float(len(temp_data))
		
		evals.append(float(average))
	
	return evals

if __name__ == "__main__":
	if rank == 0:
		#master process

		#files
		current_directory = "data/generation-0/"

		input_filename_prefix = "ind-"
		input_filename_sufix = ".txt"

		output_filename = "test.txt"

		results_filename = "data/gen-output-" + str(uuid.uuid4()) + ".txt"
		temp_file = createFile(results_filename)
		closeFile(temp_file)

		eachGenResults_file = 'data/output.csv.txt'


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

		start_from_previous_gen = False

		#starts from the previous generation
		#will output into a new results_filename
		if start_from_previous_gen:
			if current_iteration == 1:
				#grab the previous highscore, set the  Board.winning_score to it
				fp = openFile("data/curr_high_score.txt")
				curr_h_score = readFromFile(fp)
				curr_h_score_float = float(curr_h_score[0])
				Board.winning_score = curr_h_score_float

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
		#will create a new thing from scratch
		else:
			if current_iteration == 1:
				eachGenResultsToWrite(True)
				score_fp = createFile('data/' + "curr_high_score.txt")
				writeToFile(score_fp, str(Board.winning_score))
				closeFile(score_fp)

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

		list_of_seeds = [i for i in range(99999)] #list of seeds
		num_workers = number_of_individuals

		print("about to start the while loop")

		while True:
			#repeat for each gen
			
			seeds_for_iteration = random.sample(list_of_seeds, number_of_simulations) #pick the number_of_simulations seeds			
			#SAVE THESE IN A FILE FOR THAT GEN
			seed_buffer = ""
			for i in range(0, len(seeds_for_iteration)):
				seed_buffer += str(seeds_for_iteration[i])
				if i < len(seeds_for_iteration) -1:
					seed_buffer += "\n"
			output_file_pop = createFile(current_directory + "my_seeds.txt")
			writeToFile(output_file_pop, seed_buffer)
			closeFile(output_file_pop)
			print ("about to do prep stuff")
			#track seeds I have out
			#size is equal to spacing_from_total_games_worker_play
			#since worker 1 and worker 21 will play games for same 5 inviduals
			list_seeds_number_times_given_out = [0 for i in range(spacing_from_total_games_worker_play)]
			list_seeds_number_times_given_out_got_score_back = [0 for i in range(spacing_from_total_games_worker_play)]
			sleeping_workers = 0
			workers_I_already_put_sleep = set()
			list_of_summed_scores_for_each_indiv = [0 for i in range(number_of_individuals)]
			#generation is over once all the indexes of list_seeds_number_times_given_out equals number_of_simulations
			#else we still have to keep playing while these is at least one index less than number_of_simulations
			print ("about to do open mpi stuff")
			play_games_for_id = 0
			while any(i < number_of_simulations for i in list_seeds_number_times_given_out_got_score_back):
				data = comm.recv(source=MPI.ANY_SOURCE, tag=MPI.ANY_TAG, status=status)
				source = status.Get_source() #source is also the id of that worker, starts from 1
				id = source-1
				tag = status.Get_tag()
				#cal the original indiv worker maps to
				#i.e. worker 21 maps to 1, worker 49 maps to 9, etc
				# first_indiv = id % spacing_from_total_games_worker_play

				#worker is ready to ply another round of games
				# print("GOT WORKER", id)
				# print(list_seeds_number_times_given_out)
				if tag == tags.READY:
					num_times_seed_given = list_seeds_number_times_given_out[play_games_for_id]
					temp_loop_checker = play_games_for_id
					while (num_times_seed_given >= number_of_simulations):
						play_games_for_id = (play_games_for_id + 1) % spacing_from_total_games_worker_play
						num_times_seed_given = list_seeds_number_times_given_out[play_games_for_id]
						#made a full circle, so all seeds have been played for all individuals
						if (temp_loop_checker == play_games_for_id):
							print("I will now put a worker to sleep since list_seeds_number_times_given_out is all 100")
							print(list_seeds_number_times_given_out)
							break
					if (num_times_seed_given < number_of_simulations):
						seed = seeds_for_iteration[num_times_seed_given]
						comm.send((seed, current_iteration, play_games_for_id), dest=source, tag=tags.START)
						list_seeds_number_times_given_out[play_games_for_id] += 1
					#only let worker play if his seeds are < number_of_simulations
					#we will send him the seed to play
					# num_times_seed_given = list_seeds_number_times_given_out[first_indiv]
					# if (num_times_seed_given < number_of_simulations):
					# 	seed = seeds_for_iteration[num_times_seed_given]
					# 	comm.send((seed,current_iteration), dest=source, tag=tags.START)
					# 	list_seeds_number_times_given_out[first_indiv] += 1
						print("Sending task %d to worker %d" % (seed, play_games_for_id))
						print("the number of times for (mapped % 20 first indiv)", play_games_for_id, "is", num_times_seed_given)
						print("list_seeds_number)times_given_out")
						print(list_seeds_number_times_given_out)
					#else we will tell the worker to sleep for SLEEP_TIME_CONSUMER
					else:
						# print("list_seeds_number_times_given_out")
						# print(list_seeds_number_times_given_out)
						# print("mapped to first indiv", first_indiv, "given out", list_seeds_number_times_given_out[first_indiv])
						print("WORKER GOING TO SLEEP")
						print("list_seeds_number_times_given_out_got_score_back")
						print(list_seeds_number_times_given_out_got_score_back)
						#if we are on the last generation, worker exit
						if current_iteration == number_of_generations:
							comm.send(None, dest=source, tag = tags.EXIT)
						#if we are not on last generaton, worker sleep
						else:
							comm.send(None, dest=source, tag=tags.SLEEP)
							print("put worker to sleep", id)
							if id not in workers_I_already_put_sleep:
								workers_I_already_put_sleep.add(id)
								sleeping_workers += 1
							print("length of sleeping workers is", sleeping_workers)

				#worker is done playing, lets grab the results?
				elif tag == tags.DONE:
					#data = (results, the id I was told to play as)
					#results is a list
					results = data[0] #len of results should be size 5
					id = data[1]

					i = (id % spacing_from_total_games_worker_play)
					list_seeds_number_times_given_out_got_score_back[i] += 1
					index = 0
					while i < (len(results) * spacing_from_total_games_worker_play):
						list_of_summed_scores_for_each_indiv[i] = list_of_summed_scores_for_each_indiv[i] + results[index]
						i += spacing_from_total_games_worker_play
						index += 1

					# sys.stdout = open("data/prod_data", 'a')
					# print("LENGTH OF DATA FROM", id, "IS", len(results))
					# print("list_seeds_number_times_given_out\n",list_seeds_number_times_given_out)
					# print("list_of_summed_scores_for_each_indiv\n",list_of_summed_scores_for_each_indiv)
					# print("list_seeds_number_times_given_out_got_score_back",list_seeds_number_times_given_out_got_score_back)
					# print("last indiv added to",i-spacing_from_total_games_worker_play)
					# print("results from consumer",results)
					# sys.stdout = sys.__stdout__

				elif tag == tags.EXIT:
					print("Worker %d exited" % id)
			
			#got all the info for the generation
			#now I calc this info and create my next genation
			if all(i >= number_of_simulations for i in list_seeds_number_times_given_out):
				
				# sys.stdout = open("data/prod_delme", 'a')
				# print("FINISHED PLAYING GAMES, NEXT GEN TIME")
				# print("list_seeds_number_times_given_out\n",list_seeds_number_times_given_out)
				# print("list_of_summed_scores_for_each_indiv\n",list_of_summed_scores_for_each_indiv)
				# print("list_seeds_number_times_given_out_got_score_back",list_seeds_number_times_given_out_got_score_back)
				# print("")
				# sys.stdout = sys.__stdout__
				
				print("finished playing, time to calc the data")
				for i in range(len(list_of_summed_scores_for_each_indiv)):
					len_of_number_times_seed_given = list_seeds_number_times_given_out_got_score_back[i % spacing_from_total_games_worker_play]
					score = list_of_summed_scores_for_each_indiv[i]
					avg_score_for_indiv = score / len_of_number_times_seed_given
					pop[i].fitness = (avg_score_for_indiv,)

				addToFileWithBreakline(results_filename, "Best for Generation " + str(current_iteration))
				for fp in toolbox.select(pop, k = int(len(pop))):
					addToFileWithBreakline(results_filename, (str(fp) + ";" + str(fp.fitness) + "; " + str(time.time() - start) + ";") )

				temp_file = createFile(current_directory + "results_for_this_pop.txt")
				closeFile(temp_file)
				addToFileWithBreakline(current_directory + "results_for_this_pop.txt", "Best for Generation " + str(current_iteration))
				for fp in toolbox.select(pop, k = int(len(pop))):
					addToFileWithBreakline(current_directory + "results_for_this_pop.txt", (str(fp) + ";" + str(fp.fitness)) )

				temp_file = createFile(current_directory + "only_scores.txt")
				closeFile(temp_file)
				addToFileWithBreakline(current_directory + "only_scores.txt", "Scores in order of my_pop.txt " + str(current_iteration))
				for i in range(len(list_of_summed_scores_for_each_indiv)):
					len_of_number_times_seed_given = list_seeds_number_times_given_out[i % spacing_from_total_games_worker_play]
					score = list_of_summed_scores_for_each_indiv[i]
					avg_score_for_indiv = score / len_of_number_times_seed_given
					addToFileWithBreakline(current_directory + "only_scores.txt", str(avg_score_for_indiv) )


				max_score = max([p.fitness for p in pop])
				print("old max", Board.winning_score)
				if (max_score[0] > Board.winning_score):
					Board.winning_score = max_score[0]
					#save the score, so we can restart from last saved highscore
					score_fp = createFile('data/' + "curr_high_score.txt")
					writeToFile(score_fp, str(max_score[0]))
					closeFile(score_fp)
					print("change to score")
				print("new max", Board.winning_score)
				addToFile(results_filename, "\n")
				eachGenResultsToWrite(False, g=current_iteration, num_sims=num_sims, pop_size=pop_size, pop_highscore=max_score, current_time=str(time.time() - start))
				start = time.time()
				current_iteration += 1

			if current_iteration >= number_of_generations+1:
				break

			if current_iteration > last_iteration:
				print("making new gen", current_iteration)

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

		print("Master finishing")
		#shut down workers
		for i in range(1, number_of_individuals+1):
			comm.send((seed,current_iteration), dest=i, tag=tags.EXIT)
	else:
		#consumer
		mpi_consumer.consumerFunc()
		pass
