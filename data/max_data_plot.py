import sys
import os
import numpy as np

import matplotlib.pyplot as plt

def readFromFileHPCRUN(file_pointer):
	result = []
	
	#skip the first line
	next(file_pointer)

	for line in file_pointer:
		value_str = line.split('\n')[0]
		result.append(float(line.split('\n')[0]))
	
	return result

def readFromFile(file_pointer):
	result = []
	
	for line in file_pointer:
		value_str = line.split('\n')[0]
		result.append(float(line.split('\n')[0]))
	
	return result

#data for each generation
#scores, size length = # of generation
#position 0 = array of scores from only_scores.txt in gen-1
scores_for_each_gen = []
vanilla_for_each_gen = []
random_for_each_gen = []

gen = 1
current_directory = "generation-" + str(gen) + "/"
while os.path.exists(current_directory):
	#grab the data
	#grab hpc run data (max)
	file_name = "only_scores.txt"
	fp_my_scores = open(current_directory + file_name)
	scores_list = readFromFileHPCRUN(fp_my_scores)
	scores_for_each_gen.append(scores_list)

	#grab lab comp run vanilla and rand
	file_name = "vanilla_mcts_scores.txt"
	fp_my_scores = open(current_directory + file_name)
	scores_list = readFromFile(fp_my_scores)
	vanilla_for_each_gen.append(scores_list)

	file_name = "random_scores.txt"
	fp_my_scores = open(current_directory + file_name)
	scores_list = readFromFile(fp_my_scores)
	random_for_each_gen.append(scores_list)

	gen += 1
	current_directory = "generation-" + str(gen) + "/"

#max_score_per_gen
max_score_per_gen_list = []
#mix_score_per_gen
min_score_per_gen_list = []
#median_score_per_gen
median_score_per_gen = []
#save the scores
for i in scores_for_each_gen:
	max_score_per_gen_list.append(np.max(i))
	min_score_per_gen_list.append(np.min(i))
	median_score_per_gen.append(np.median(i))

#vanilla
vanilla_avg_score_per_gen_list = []
for i in vanilla_for_each_gen:
	vanilla_avg_score_per_gen_list.append(np.average(i))
#random
random_avg_score_per_gen_list = []
for i in random_for_each_gen:
	random_avg_score_per_gen_list.append(np.average(i))

xAxis = [i for i in range(len(scores_for_each_gen))]

plt.xlabel('Generation', fontsize=20)
plt.ylabel('Scores', fontsize=20)
plt.title('Maxizing MCTS, Vanilla MCTS, Random', fontsize=20)

plt.plot(xAxis, max_score_per_gen_list, color='r', label="MAX")
plt.plot(xAxis, min_score_per_gen_list, color='g', label="MIN")
plt.plot(xAxis, median_score_per_gen, color='b', label="MED")
plt.plot(xAxis, vanilla_avg_score_per_gen_list, color='c', label="VAN")
plt.plot(xAxis, random_avg_score_per_gen_list, color='orange',label="RAN")
plt.legend(prop={'size': 15})
plt.show()