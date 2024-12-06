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

	p1_result = test_path(grid, None, None, initialx, initialy)
	print(len(p1_result.visited))								# Part 1 answer

	count = 0

	for x, y in p1_result.visited:
		if (x, y) == (initialx, initialy):
			continue
		foo = test_path(grid, x, y, initialx, initialy)
		if not foo.escaped:
			count += 1

	print(count)												# Part 2 answer


class Result():
	def __init__(self, visited, escaped):
		self.visited = visited
		self.escaped = escaped


def test_path(grid, obx, oby, initialx, initialy):				# Returns spots visited if the guard escapes, otherwise returns -1

	width = len(grid)
	height = len(grid[0])

	gx = initialx
	gy = initialy
	direction = UP

	visited = set()		# Detect spots visited
	states = set()		# Detect cycles

	visited.add((gx, gy))
	states.add((gx, gy, direction))

	while True:

		nextx = gx + vectors[direction][0]
		nexty = gy + vectors[direction][1]

		if nextx < 0 or nextx >= width or nexty < 0 or nexty >= height:
			return Result(visited, True)

		if grid[nextx][nexty] == "#" or (nextx == obx and nexty == oby):
			direction = turns[direction]
			continue

		gx = nextx
		gy = nexty

		if (gx, gy, direction) in states:
			return Result(visited, False)

		visited.add((gx, gy))
		states.add((gx, gy, direction))


main()
