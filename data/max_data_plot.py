import sys
import os
import numpy as np

import matplotlib.pyplot as plt

def readFromFile(file_pointer):
	result = []
	
	#skip the first line
	next(file_pointer)

	for line in file_pointer:
		value_str = line.split('\n')[0]
		result.append(float(line.split('\n')[0]))
	
	return result

#data for each generation
#scores, size length = # of generation
#position 0 = array of scores from only_scores.txt in gen-1
scores_for_each_gen = []

gen = 1
current_directory = "generation-" + str(gen) + "/"
while os.path.exists(current_directory):
	#grab the data
	file_name = "only_scores.txt"
	fp_my_scores = open(current_directory + file_name)
	scores_list = readFromFile(fp_my_scores)
	scores_for_each_gen.append(scores_list)

	gen += 1
	current_directory = "generation-" + str(gen) + "/"

#max_score_per_gen
max_score_per_gen_list = []

#mix_score_per_gen
min_score_per_gen_list = []

#median_score_per_gen
median_score_per_gen = []
for i in scores_for_each_gen:
	max_score_per_gen_list.append(np.max(i))
	min_score_per_gen_list.append(np.min(i))
	median_score_per_gen.append(np.median(i))

xAxis = [i for i in range(len(scores_for_each_gen))]

plt.plot(xAxis, max_score_per_gen_list, color='r', label="MAX")
plt.plot(xAxis, min_score_per_gen_list, color='g', label="MIN")
plt.plot(xAxis, median_score_per_gen, color='b', label="MED")
plt.legend(prop={'size': 15})
plt.show()