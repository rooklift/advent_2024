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


def recurse(grid, x, y):		# Returns set of all 9s reachable from the point, and the rating

	ret = set()
	rating = 0

	val = grid[x][y]

	if val == 9:
		ret.add((x, y))
		return ret, 1

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
			peaks, r = recurse(grid, x + vec[0], y + vec[1])
			ret.update(peaks)
			rating += r

	return ret, rating


def main():
	grid = parser("10_input.txt")

	width = len(grid)
	height = len(grid[0])

	p1_score = 0
	p2_score = 0

	for x in range(width):
		for y in range(height):
			if grid[x][y] == 0:
				peaks, rating = recurse(grid, x, y)
				p1_score += len(peaks)
				p2_score += rating

	print(p1_score)
	print(p2_score)


main()
