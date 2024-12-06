UP = 1
DOWN = 2
RIGHT = 3
LEFT = 4

turns = {UP: RIGHT, RIGHT: DOWN, DOWN: LEFT, LEFT: UP}

vectors = {UP: [0, -1], RIGHT: [1, 0], DOWN: [0, 1], LEFT: [-1, 0]}


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


def main():

	grid = parser("06_input.txt")

	width = len(grid)
	height = len(grid[0])

	for x in range(width):
		for y in range(height):
			if grid[x][y] == "^":
				initialx = x
				initialy = y

	gx = initialx
	gy = initialy
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

	print(len(visited))				# Part 1 answer

	# -------------------------------------------------------

	count = 0

	i = 0
	for x, y in visited:
		i += 1
		print(i)
		if (x, y) == (initialx, initialy):
			continue
		if test_obstruction(grid, x, y, initialx, initialy):
			count += 1

	print(count)


def test_obstruction(grid, obx, oby, initialx, initialy):

	width = len(grid)
	height = len(grid[0])

	gx = initialx
	gy = initialy
	direction = UP

	states = set()		# This is now just to detect cycles

	while True:

		nextx = gx + vectors[direction][0]
		nexty = gy + vectors[direction][1]

		if nextx < 0 or nextx >= width or nexty < 0 or nexty >= height:
			return False

		if grid[nextx][nexty] == "#" or (nextx == obx and nexty == oby):
			direction = turns[direction]
			continue

		gx = nextx
		gy = nexty

		if (gx, gy, direction) in states:
			return True

		states.add((gx, gy, direction))


main()
