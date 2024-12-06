def parser(filename):
	with open(filename) as infile:
		lines = [line.strip() for line in infile.readlines() if line.strip() != ""]
	ret = []
	for c in lines[0]:
		ret.append([])
	for line in lines:
		for x, c in enumerate(line):
			ret[x].append(c)
	return ret

UP = 1
DOWN = 2
RIGHT = 3
LEFT = 4

turns = {UP: RIGHT, RIGHT: DOWN, DOWN: LEFT, LEFT: UP}

vectors = {UP: [0, -1], RIGHT: [1, 0], DOWN: [0, 1], LEFT: [-1, 0]}

def main():
	grid = parser("06_input.txt")

	width = len(grid)
	height = len(grid[0])

	for x in range(width):
		for y in range(height):
			if grid[x][y] == "^":
				gx = x
				gy = y

	direction = UP

	visited = set()
	visited.add((gx, gy))

	while True:

		nextx = gx + vectors[direction][0]
		nexty = gy + vectors[direction][1]

		if nextx < 0 or nextx >= width or nexty < 0 or nexty >= height:
			break

		if grid[nextx][nexty] == "#":
			direction = turns[direction]
			continue

		gx = nextx
		gy = nexty
		visited.add((gx, gy))

	print(len(visited))

main()
