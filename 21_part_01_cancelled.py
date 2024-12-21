def parser(filename):
	with open(filename) as infile:
		return [line.strip() for line in infile.readlines() if line.strip() != ""]

big = [				# Note that these arrays have [y][x] format - but we convert them in make_keypad_grid()
	"789",
	"456",
	"123",
	".0A",
]

small = [
	".^A",
	"<v>",
]


def make_keypad_grid(lines):
	grid = [[], [], []]
	for line in lines:
		for x, c in enumerate(line):
			grid[x].append(c)
	return grid


def make_grid_lookup(grid):

	ret = dict()	# startc --> endc --> cost to move AND push (i.e. Manhat dist + 1)

	width = len(grid)
	height = len(grid[0])

	for x in range(width):
		for y in range(height):
			startc = grid[x][y]
			if startc == ".":
				continue
			for i in range(width):
				for j in range(height):
					endc = grid[i][j]
					if endc == ".":
						continue
					if startc not in ret:
						ret[startc] = dict()
					ret[startc][endc] = abs(x - i) + abs(y - j) + 1

	return ret


def total_cost(lookup, sequence):
	ret = 0
	current_pos = "A"
	for c in sequence:
		ret += lookup[current_pos][c]
		current_pos = c
	return ret


def main():

	codes = parser("21_input.txt")

	big_grid = make_keypad_grid(big)
	small_grid = make_keypad_grid(small)

	big_lookup = make_grid_lookup(big_grid)
	small_lookup = make_grid_lookup(small_grid)

	# But I'm not sure all of this is even useful.

	# The exact route of the robot arm matters very much since it impacts
	# the costs at the levels above it.




main()
