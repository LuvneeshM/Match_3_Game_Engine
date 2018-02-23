import csv
import numpy as np

reader = csv.DictReader(open('results.csv', 'rb'), delimiter=';')

dict_list = []

for line in reader:
	dict_list.append(line)

for x in dict_list[:3]:
	print x
	print int(x['Time_Limit'])
	print int(x['Turn_#'])
	print tuple(x['Move_Made'])
	print np.array(x['Board']) 
	print dict(x['List_Of_Moves'])
