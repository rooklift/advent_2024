from collections import deque

WIDTH = 71
HEIGHT = 71

TAR_X = 70
TAR_Y = 70

def parser(filename):
	with open(filename) as infile:
		lines = [line.strip() for line in infile.readlines() if line.strip() != ""]
	ret = []
	for line in lines:
		x = int(line.split(",")[0])
		y = int(line.split(",")[1])
		ret.append((x, y))
	return ret

def neighbours(x, y, avoid):
	ret = []
	if x > 0:
		ret.append((x - 1, y))
	if x < WIDTH - 1:
		ret.append((x + 1, y))
	if y > 0:
		ret.append((x, y - 1))
	if y < HEIGHT - 1:
		ret.append((x, y + 1))
	return [item for item in ret if item not in avoid]

def part1_bfs(data):
	x = 0
	y = 0

	distances = dict(); distances[(x, y)] = 0
	todo = deque(); todo.append((x, y))

	while len(todo) > 0:

		current = todo.popleft()

		for neigh in neighbours(current[0], current[1], data[:1024]):

			if neigh in distances:
				continue

			if neigh == (TAR_X, TAR_Y):
				return distances[current] + 1

			distances[neigh] = distances[current] + 1
			todo.append(neigh)

	assert(False)

def main():
	data = parser("18_input.txt")
	print(part1_bfs(data))


main()
