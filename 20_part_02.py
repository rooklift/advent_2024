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


def good_cheat_count(grid, distances, x, y, debug_totals):

	print(x, y)

	visited = set()

	width = len(grid)
	height = len(grid[0])

	ret = 0

	for max_dx in range(20 + 1):
		max_dy = 20 - max_dx

		for i in range(-max_dx, max_dx + 1):

			if x + i < 0 or x + i >= width:
				continue

			for j in range(-max_dy, max_dy + 1):

				if y + j < 0 or y + j >= height:
					continue

				if (x + i, y + j) in visited:
					continue

				visited.add((x + i, y + j))

				if grid[x + i][y + j] == ".":

					saving = distances[(x, y)] - distances[(x + i, y + j)] - abs(i) - abs(j)

					if saving >= 100:

						if saving in debug_totals:
							debug_totals[saving] += 1
						else:
							debug_totals[saving] = 1

						ret += 1

	return ret


def main():

	grid, startx, starty, endx, endy = parser("20_input.txt")

	width = len(grid)
	height = len(grid[0])

	distances = dict()

	distances[(startx, starty)] = 0

	x, y = startx, starty

	while x != endx or y != endy:
		print(x, y)
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

	debug_totals = dict()

	for x in range(1, width - 1):
		for y in range(1, height - 1):
			if grid[x][y] != ".":			# The opposite way from part 1.
				continue
			good_cheats += good_cheat_count(grid, distances, x, y, debug_totals)

	print()
	print(good_cheats)


main()
