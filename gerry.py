import json
import math
import random
import os

n = 10 # size of grid
SIZE = n * n # number of blocks
D = 20 # number of districts
PROB = 0.6

# load voters
_voters = json.load(open("voters.json"))["voters_by_block"]
voters = [(_voters["party_A"][x], _voters["party_B"][x]) for x in range(SIZE)]

#test
# PROB = 1
# voters = [(1, 0)] * 20 + [(0, 1)] * 30

populations = [sum(x) for x in voters]

# some key stats
totalPopulation = sum(populations)

# some helper functions

index2coord = lambda index: divmod(index, n)
coord2index = lambda x, y: x * n + y 

districtPopulation = lambda district: sum([populations[x] for x in district])

def getFinalDistrict(district, final, merges):
	if district not in merges:
		return district
	if district in final:
		return final[district]
	temp = getFinalDistrict(merges[district], final, merges)
	final[district] = temp
	return temp

def districtMapping2Answer(districtMapping, merges = {}):
	finalDistricts = {}
	index = 0
	district2district = {}
	for block in districtMapping:
		district = getFinalDistrict(districtMapping[block], finalDistricts, merges)

		if district in district2district:
			district2district[district][1].append(block)	
		else:
			district2district[district] = (index, [block])
			index += 1

	answer = [None] * len(district2district)
	for district in district2district:
		index, blocks = district2district[district]
		answer[index] = blocks

	return answer

def finalMetrics(districtMapping, merges = {}):
	answer = districtMapping2Answer(districtMapping, merges)

	numDistricts = len(answer)
	meanDistrictPop = float(totalPopulation) / numDistricts
	districtPopulations = [districtPopulation(x) for x in answer]

	# district population imbalance
	squareDiffs = [(x - meanDistrictPop) ** 2 for x in districtPopulations]
	districtPopulationImbalance = sum(squareDiffs)

	districtsWon = 0
	# expected efficiency gap
	wastedA = 0
	wastedB = 0
	for districtIndex in range(len(answer)):
		district = answer[districtIndex]
		population = districtPopulations[districtIndex]
		majorityVotes = int(math.floor(population / 2.0 + 1))

		# check who expect to win
		votersA = 0
		votersB = 0
		for block in district:
			a, b = voters[block]
			x = a * PROB
			y = b * PROB
			votersA += x + (b - y)
			votersB += y + (a - x)


		if votersA > votersB:
			districtsWon += 1

			wastedA += votersA - majorityVotes
			wastedB += votersB
		else:
			wastedA += votersA
			wastedB += votersB - majorityVotes

	expectedGap = (wastedA - wastedB) / float(totalPopulation)

	return (districtsWon, districtPopulationImbalance, expectedGap)

def verifyMetrics(metric):
	return (
		metric[0] > 9,
		metric[1] < (200 * (10 ** 10)),
		metric[2] > -0.04		
	)	

def printMap(answer):
	districtMapping = {}
	for districtIndex in range(len(answer)):
		district = answer[districtIndex]
		for block in district:
			districtMapping[block] = districtIndex

	lk = {}

	# numbers = list(range(1, 21))
	# limit = 19
	# while limit >= 0:
	# 	i = random.randint(0, limit)
	# 	lk[20 - limit - 1] = numbers[i]
	# 	numbers[i], numbers[limit] = numbers[limit], numbers[i]
	# 	limit -= 1

	for x in range(20):
		lk[x] = x

	f = lambda x: str(lk[x]).ljust(2, " ")
	text = [[0 for y in range(n)] for x in range(n)]
	for i in range(SIZE):
		x, y = index2coord(i)
		text[x][y] = f(districtMapping[i])

	text = "\n".join(["  ".join(x) for x in text])
	print(text)

def rateMerge(merge):

	_mapping = dict(districtMapping)

	# make sure they are from different districts
	if _mapping[merge[0]] == _mapping[merge[1]]:
		return False

	# do merge
	districtMerges = {}
	district1 = _mapping[merge[0]]
	district2 = _mapping[merge[1]]
	districtMerges[max(district1, district2)] = min(district1, district2)

	# apply merges directly into district mapping
	changes = True
	finalDistricts = {}
	for block in _mapping:
		district = _mapping[block]
		_mapping[block] = getFinalDistrict(district, finalDistricts, districtMerges)

	metric = finalMetrics(_mapping)

	return (_mapping, metric)

def compare(merge1, merge2):
	if merge2 == -1:
		return 1

	v1 = verifyMetrics(merge1)
	v2 = verifyMetrics(merge2)

	if not v1[1] and v2[1]:
		return -1

	if merge1[1] < merge2[1]:
		return 1
	elif merge1[0] > merge2[0]:
		return 1
	return 0

	if v1[1]:
		if merge1[0] > merge2[0]:
			return 1
	else:
		if merge1[1] < merge2[1]:
			return 1

districtMapping = {}

# make each block it's own district
for i in range(SIZE):
	districtMapping[i] = i
numDistricts = SIZE


while numDistricts > D:
	numDistricts -= 1

	bestMerge = (-1, -1)
	bestMergeScore = -1
	bestMergeMap = districtMapping

	def testMerge(merge):
		global bestMergeScore, bestMerge, bestMergeMap
		r = rateMerge(merge)

		if r == False:
			return

		_mapping, rating = r

		if compare(rating, bestMergeScore) == 1:
			bestMerge = merge
			bestMergeScore = rating
			bestMergeMap = dict(_mapping)

	# horizontal merges
	for x in range(n):
		for y in range(n - 1):
			merge = (coord2index(x, y), coord2index(x, y + 1))
			testMerge(merge)

	# vertical merges
	for x in range(n - 1):
		for y in range(n):
			merge = (coord2index(x, y), coord2index(x + 1, y))
			testMerge(merge)

	# apply changes
	districtMapping = bestMergeMap

answer = districtMapping2Answer(districtMapping)
printMap(answer)
print("\n")
metric = finalMetrics(districtMapping)

verification = verifyMetrics(metric)
print(str("Districts: " + str(metric[0])).ljust(55) + " - " + ("Good" if verification[0] else "Bad"))
print(str("District Population Imbalance: " + str(metric[1])).ljust(55) + " - " + ("Good" if verification[1] else "Bad"))
print(str("Expected Efficiency Gap: " + str(metric[2])).ljust(55) + " - " + ("Good" if verification[2] else "Bad"))

print(str(int((200.0 * 10 ** 10 - metric[1]) / (200 * 10 ** 10) * 100)) + "%")
