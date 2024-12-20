def parser(filename):
	with open(filename) as infile:
		lines = [line.strip() for line in infile.readlines() if line.strip() != ""]

	grid = []

	for line in lines:
		grid.append([])

	startx, starty = 0, 0
	endx, endy = 0, 0

	for y, line in enumerate(lines):
		for x, c in enumerate(line):

			if c == "S":
				startx, starty = x, y
			if c == "E":
				endx, endy = x, y

			if c in [".", "S", "E"]:
				grid[x].append(".")
			else:
				grid[x].append("#")

	return grid, startx, starty, endx, endy


def saving(grid, distances, x, y):			# How much is saved by making this cut.

	links = []

	for vec in [(1, 0), (-1, 0), (0, -1), (0, 1)]:
		if grid[x + vec[0]][y + vec[1]] == ".":
			links.append((x + vec[0], y + vec[1]))

	if len(links) < 2:
		return 0

	if len(links) > 2:
		return 2				# Might not be true generally, but correct for this exact puzzle.

	return abs(distances[links[0]] - distances[links[1]]) - 2


def main():

	grid, startx, starty, endx, endy = parser("20_input.txt")

	width = len(grid)
	height = len(grid[0])

	distances = dict()

	distances[(startx, starty)] = 0

	x, y = startx, starty

	while x != endx or y != endy:
		for vec in [(1, 0), (-1, 0), (0, -1), (0, 1)]:
			if grid[x + vec[0]][y + vec[1]] != ".":
				continue
			if (x + vec[0], y + vec[1]) in distances:
				continue
			distances[(x + vec[0], y + vec[1])] = distances[(x, y)] + 1
			x = x + vec[0]
			y = y + vec[1]
			break

	good_cheats = 0

	for x in range(1, width - 1):
		for y in range(1, height - 1):
			if grid[x][y] != "#":
				continue
			if saving(grid, distances, x, y) >= 100:
				good_cheats += 1

	print(good_cheats)


main()
