import json

n = 10 # size of grid
SIZE = n * n # number of blocks
D = 20 # number of districts

# load voters
_voters = json.load(open("voters.json"))["voters_by_block"]
voters = [(_voters["party_A"][x], _voters["party_B"][x]) for x in range(SIZE)]
populations = [sum(x) for x in voters]

# some key stats
totalPopulation = sum(populations)

print(totalPopulation)
