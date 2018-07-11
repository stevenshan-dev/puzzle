import sys
import json

SIZE = 150

def coord2index(x, y):
	return y * 150 + x

def index2coord(index):
	quotient, rem = divmod(index, SIZE)
	return (rem, quotient)

if __name__ == "__main__":
	# load adjacency list
	adjList = json.load(open("adjlist.txt"))

	start_x, start_y = sys.argv[1], sys.argv[2]
	end_x, end_y = sys.argv[3], sys.argv[4]

	start_index = coord2index(start_x, start_y)
	end_index = coord2index(end_x, end_y)

	print("Finding route from (" + str(start_x) + ", " + str(start_y) + 
		") to (" + str(end_x) + ", " + str(end_y) + ")")
	print("Start index: " + str(start_index))
	print("End index: " + str(end_index))

	# run BFS
	queue = [start_index]
	visited = [False] * (SIZE * SIZE)
	visited[start_index] = True

	while len(queue) > 0:
		tempQueue = []
		for position in queue:
			_tempQueue = adjList[visited]
