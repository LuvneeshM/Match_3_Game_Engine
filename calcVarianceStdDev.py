import csv
import numpy as np
import random

def csv_to_dict_list(fileName):
	reader = csv.DictReader(open(fileName, 'rt'), delimiter=';')

	dict_list = []

	for line in reader:
		dict_list.append(line)

	return dict_list

mctsVsRandom_dict_list = csv_to_dict_list('results.csv')
mcts_points_list = []

for data_line in mctsVsRandom_dict_list:
	if (int(data_line['Turn_#'])==19 and data_line['Agent']=="MCTS"):
		mcts_points_list.append(int(data_line['Points']))

mcts_points_list_25 = list(mcts_points_list)
mcts_points_list_50 = list(mcts_points_list)
mcts_points_list_200 = list(mcts_points_list)
print ("Mean: {}".format(np.mean(mcts_points_list)))

#200
num_of_buckets_200 = len(mcts_points_list_200) / 200
buckets_200 = [ [0 for x in range(200)] for y in range(int(num_of_buckets_200)) ]
for i in range(len(buckets_200)):
	scores = random.sample(mcts_points_list_200, 200)
	for j in range(len(scores)):
		buckets_200[i][j] = scores[j]
		mcts_points_list_200.remove(scores[j])

avg_per_bucket_200 = []
for i in range(len(buckets_200)):
	avg_per_bucket_200.append(np.mean(buckets_200[i]))


#100
num_of_buckets = len(mcts_points_list) / 100
buckets = [ [0 for x in range(100)] for y in range(int(num_of_buckets)) ]
for i in range(len(buckets)):
	scores = random.sample(mcts_points_list, 100)
	for j in range(len(scores)):
		buckets[i][j] = scores[j]
		mcts_points_list.remove(scores[j])

avg_per_bucket = []
for i in range(len(buckets)):
	avg_per_bucket.append(np.mean(buckets[i]))

#50
num_of_buckets_50 = len(mcts_points_list_50) / 50
buckets_50 = [ [0 for x in range(50)] for y in range(int(num_of_buckets_50)) ]

for i in range(len(buckets_50)):
	scores = random.sample(mcts_points_list_50, 50)
	for j in range(len(scores)):
		buckets_50[i][j] = scores[j]
		mcts_points_list_50.remove(scores[j])

avg_per_bucket_50 = []
for i in range(len(buckets_50)):
	avg_per_bucket_50.append(np.mean(buckets_50[i]))

#25
num_of_buckets_25 = len(mcts_points_list_25) / 25
buckets_25 = [ [0 for x in range(25)] for y in range(int(num_of_buckets_25)) ]

for i in range(len(buckets_25)):
	scores = random.sample(mcts_points_list_25, 25)
	for j in range(len(scores)):
		buckets_25[i][j] = scores[j]
		mcts_points_list_25.remove(scores[j])

avg_per_bucket_25 = []
for i in range(len(buckets_25)):
	avg_per_bucket_25.append(np.mean(buckets_25[i]))

#stats
print ("******MCTS_200******")
print ("Number of Buckets: {}".format(int(num_of_buckets_200)))
print ("Standard Deviation: {}".format(np.std(avg_per_bucket_200) ))
print ("Variance: {}".format(np.var(avg_per_bucket_200)))


#stats
print ("******MCTS_100******")
print ("Number of Buckets: {}".format(int(num_of_buckets)))
print ("Standard Deviation: {}".format(np.std(avg_per_bucket) ))
print ("Variance: {}".format(np.var(avg_per_bucket)))

#stats
print ("******MCTS_50******")
print ("Number of Buckets: {}".format(int(num_of_buckets_50)))
print ("Standard Deviation: {}".format(np.std(avg_per_bucket_50) ))
print ("Variance: {}".format(np.var(avg_per_bucket_50)))

#stats
print ("******MCTS_25******")
print ("Number of Buckets: {}".format(int(num_of_buckets_25)))
print ("Standard Deviation: {}".format(np.std(avg_per_bucket_25) ))
print ("Variance: {}".format(np.var(avg_per_bucket_25)))