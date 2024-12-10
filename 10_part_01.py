def parser(filename):
	with open(filename) as infile:
		lines = [line.strip() for line in infile.readlines() if line.strip() != ""]
	ret = []
	for c in lines[0]:
		ret.append([])
	for line in lines:
		for x, c in enumerate(line):
			ret[x].append(int(c))
	return ret


def recurse(grid, x, y):		# Returns set of all 9s reachable from the point

	ret = set()

	val = grid[x][y]

	if val == 9:
		ret.add((x, y))
		return ret

	vecs = []

	if x > 0:
		vecs.append([-1, 0])
	if x < len(grid) - 1:
		vecs.append([1, 0])
	if y > 0:
		vecs.append([0, -1])
	if y < len(grid) - 1:
		vecs.append([0, 1])

	for vec in vecs:
		if grid[x + vec[0]][y + vec[1]] == val + 1:
			ret.update(recurse(grid, x + vec[0], y + vec[1]))

	return ret


def main():
	grid = parser("10_input.txt")

	width = len(grid)
	height = len(grid[0])

	score = 0

	for x in range(width):
		for y in range(height):
			if grid[x][y] == 0:
				score += len(recurse(grid, x, y))

	print(score)


main()
