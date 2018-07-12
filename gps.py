import sys
import json

SIZE = 150

def copy2clip(txt):
    cmd='echo '+txt.strip()+'|clip'
    return subprocess.check_call(cmd, shell=True)

def coord2index(x, y):
	return y * SIZE + x

def index2coord(index):
	quotient, rem = divmod(index, SIZE)
	return (rem, quotient)

def bfs(start_index, end_index):
	queue = [start_index]
	visited = [False] * (SIZE * SIZE)
	n = SIZE ** 2
	visited = [[False, []] for i in range(n)]	
	visited[start_index] = [True, [start_index]]

	while len(queue) > 0:
		if end_index in queue:
			return (True, visited[end_index][1])

		tempQueue = []
		for position in queue:
			_tempQueue = adjList[position]
			
			# remove already visited nodes
			_tempQueue = [x for x in _tempQueue if not visited[x][0]]

			# add paths
			for nextPosition in _tempQueue:
				visited[nextPosition][0] = True
				visited[nextPosition][1] = visited[position][1] + [nextPosition]

			tempQueue += _tempQueue

		queue = tempQueue

	return (False, [])

if __name__ == "__main__":
	# load adjacency list
	adjList = json.load(open("adjlist.txt"))
	argv = lambda x: int(sys.argv[x])

	start_x, start_y = argv(1), argv(2)
	end_x, end_y = argv(3), argv(4)

	start_index = coord2index(start_x, start_y)
	end_index = coord2index(end_x, end_y)

	print("Finding route from (" + str(start_x) + ", " + str(start_y) + 
		") to (" + str(end_x) + ", " + str(end_y) + ")")
	print("Start index: " + str(start_index))
	print("End index: " + str(end_index))

	pathExists, path = bfs(start_index, end_index)

	if not pathExists:
		print("No path exists")
	else:
		dirPath = []
		for i in range(0, len(path) - 1):
			current_x, current_y = index2coord(path[i])
			next_x, next_y = index2coord(path[i + 1])

			delta_x = next_x - current_x
			delta_y = next_y - current_y

			if delta_x == 1:
				dirPath.append("Right")
			elif delta_x == -1:
				dirPath.append("Left")
			elif delta_y == 1:
				dirPath.append("Down")
			elif delta_y == -1:
				dirPath.append("Up")

		dirPath = ["move" + x for x in dirPath]
		text = "[" + ", ".join(dirPath) + "]"
		print(text)

