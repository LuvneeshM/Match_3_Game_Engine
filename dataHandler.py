import csv
import numpy as np
import ast 
import matplotlib.pyplot as plt


def print_data(dict_list):
	for x in dict_list:
		print (x)
		print (int(x['Time_Limit']))
		print (int(x['Turn_#']))
		print (tuple(x['Move_Made']))
		print (np.array(x['Board']))
		print (int(x['Points']))
		#print (dict(x['List_Of_Moves']))
		list_of_moves = ast.literal_eval(x['List_Of_Moves'])
		print(list_of_moves)	

def csv_to_dict_list(fileName):
	reader = csv.DictReader(open(fileName, 'rt'), delimiter=';')

	dict_list = []

	for line in reader:
		dict_list.append(line)

	return dict_list

mctsVsRandom_dict_list = csv_to_dict_list('results.csv')
#print(len(mctsVsRandom_dict_list)) #printed 3,200,000
#print_data(mctsVsRandom_dict_list)

#mcts points per game
mcts_points_list = []
random_points_list = []
for data_line in mctsVsRandom_dict_list:
	if (int(data_line['Turn_#'])==19 and data_line['Agent']=="MCTS"):
		mcts_points_list.append(int(data_line['Points']))
	if (int(data_line['Turn_#'])==19 and data_line['Agent']=="RAND"):
		random_points_list.append(int(data_line['Points']))

print ("******MCTS******")
print ("Number of Games: {}".format(len(mcts_points_list)))
print ("Mean: {}".format(np.mean(mcts_points_list)))
print ("Max: {} ".format(max(mcts_points_list)))
print ("Min: {} ".format(min(mcts_points_list)))
print ("******RAND******")
print ("Number of Games: {}".format(len(random_points_list)))
print ("Mean: {}".format(np.mean(random_points_list)))
print ("Max: {} ".format(max(random_points_list)))
print ("Min: {} ".format(min(random_points_list)))
print ("****************")
compareList = list(map(lambda x,y: x > y, mcts_points_list, random_points_list))
print ("MCTS Won: {}".format(compareList.count(True)))
ties = len(set(mcts_points_list).intersection(random_points_list))
print ("MCTS Lost: {} (Does not include Ties)".format(compareList.count(False) - ties))
print ("MCTS Tied: {}".format(ties))

colors = (0,0,0)
area = np.pi*3

xAxis = [a for a in range(len(compareList))]

#plt.scatter(xAxis[0:5],mcts_points_list[0:5], color='b', marker='s', label='MCTS')
#plt.scatter(xAxis[0:5],random_points_list[0:5], color='r', marker='o', label='RAND')
plt.plot(xAxis,mcts_points_list, color='b', label='MCTS')
plt.plot(xAxis,random_points_list, color='r', label='RAND')
plt.legend(loc='upper left');
plt.title('wutface')
plt.xlabel('GameNumber')
plt.ylabel('Points')
plt.show()