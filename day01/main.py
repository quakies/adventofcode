import numpy as np

# Doing a quick and dirty script - hard-coding the input-data file

# Difference Score
data = np.loadtxt('input-data', dtype=int)

list0 = data[:, 0]
list1 = data[:, 1]

list0.sort()
list1.sort()

# Absolute difference
abs_diff = np.abs(list0 - list1)
sum_of_diffs = np.sum(abs_diff)

print(f'Difference Score Info')
print(f'Number items in list0: ', list0.size)
print(f'Number items in list1: ', list1.size)
print(f'Number items in abs_diff: ', abs_diff.size)
print(f'sum of differences: ', sum_of_diffs)

# Similarity Score

print('\n')
print(f'Similarity Score Info')

sim_score_hash = {}

# Count occurrences in the second list
for element in list1:
    element = int(element)
    if element in sim_score_hash:
        sim_score_hash[element] += 1
    else:
        sim_score_hash[element] = 1

# Calc the sim_score using the first list
sim_score = 0
for element in list0:
    element = int(element)
    if element in sim_score_hash:
        sim_score += (element * sim_score_hash[element])

print(f'sim_score: ', sim_score)


