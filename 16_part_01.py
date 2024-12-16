import copy
from PIL import Image


def parser(filename):
	with open(filename) as infile:
		lines = [line.strip() for line in infile.readlines() if line.strip() != ""]
	grid = []
	for i in range(len(lines[0])):
		grid.append([])
	for y, line in enumerate(lines):
		for x, c in enumerate(line):
			if c in "#.":
				grid[x].append(c)
			else:
				grid[x].append(".")
				if c == "S":
					startx = x
					starty = y
				if c == "E":
					endx = x
					endy = y
	return grid, startx, starty, endx, endy


def width_height(grid):
	return len(grid), len(grid[0])


def grid_to_png(grid, outfilename):

	width, height = width_height(grid)
	img = Image.new("RGB", (width, height), color = "white")

	for x in range(width):
		for y in range(height):
			if grid[x][y] == "#":
				img.putpixel((x, y), (0, 0, 0))
			if grid[x][y] == "O":
				img.putpixel((x, y), (0, 0, 0))

	img.save(outfilename)

# -------------------------------------------------------------------------------------------------

RIGHT = (1, 0)
LEFT = (-1, 0)
UP = (0, -1)
DOWN = (0, 1)

ALL_DIRECTIONS = [UP, RIGHT, DOWN, LEFT]

def perpendicular_directions(d):
	turns = {
		RIGHT: [UP, DOWN],
		LEFT: [UP, DOWN],
		UP: [LEFT, RIGHT],
		DOWN: [LEFT, RIGHT],
	}
	return turns[d]

# -------------------------------------------------------------------------------------------------

def main():

	original, startx, starty, endx, endy = parser("16_input.txt")
	width, height = width_height(original)

	# Remove dead ends from the grid... this simplifies various things.

	grid = anti_dead_end(original, startx, starty, endx, endy)

	# We should construct a set of nodes. Departing an x,y start in 2 different directions
	# counts as 2 different nodes.

	all_connections = dict()					# startx, starty, (dx, dy)  -->  endx, endy, (dx, dy), cost

	# For each node-start we could also add as connections the cost of turning as a connection...

	possible_states = all_possible_states(grid, startx, starty, endx, endy)

	for state in possible_states:
		all_connections[state] = get_connection(grid, possible_states, state[0], state[1], state[2])

	print(all_connections)




def get_connection(grid, possible_states, x, y, d):

	cost = 0

	nextx = x + d[0]
	nexty = y + d[1]

	if grid[nextx][nexty] != ".":
		return None

	while True:

		# Move...

		x = x + d[0]
		y = y + d[1]
		cost += 1

		# Check if we reached a new node...

		if (x, y, d) in possible_states:
			return (x, y, d, cost)

		# Is it OK to continue moving?

		nextx = x + d[0]
		nexty = y + d[1]

		if grid[nextx][nexty] != ".":

			# We're either turning left or right.

			cost += 1000

			choices = 0

			for nextd in perpendicular_directions(d):
				nextx = x + nextd[0]
				nexty = y + nextd[1]
				if grid[nextx][nexty] == ".":
					d = nextd
					choices += 1

			try:
				assert(choices == 1)
			except:
				print(x, y)
				raise AssertionError

# -------------------------------------------------------------------------------------------------

def all_possible_states(grid, startx, starty, endx, endy):

	# Returns all possible states the robot can be in, at the moment when it has to make decisions.
	# Probably this only works if dead ends have been removed.

	width, height = width_height(grid)

	foo = []													# startx, starty, (dx, dy)

	for x in range(width):
		for y in range(height):
			if grid[x][y] == ".":
				dirs_out = directions_out(grid, x, y)
				if len(dirs_out) > 2:
					for d in ALL_DIRECTIONS:
						foo.append((x, y, d))

	start_present = False
	end_present = False
	for state in foo:
		if state[0] == startx and state[1] == starty:
			start_present = True
		if state[0] == endx and state[1] == endy:
			end_present = True

	assert(start_present == False and end_present == False)		# This will make life easier.

	for d in ALL_DIRECTIONS:
		foo.append((startx, starty, d))

	for d in ALL_DIRECTIONS:
		foo.append((endx, endy, d))

	return foo

# -------------------------------------------------------------------------------------------------

def directions_out(grid, x, y):
	assert(grid[x][y] == ".")
	ret = []
	if grid[x - 1][y] == ".":
		ret.append(LEFT)
	if grid[x + 1][y] == ".":
		ret.append(RIGHT)
	if grid[x][y - 1] == ".":
		ret.append(UP)
	if grid[x][y + 1] == ".":
		ret.append(DOWN)
	return ret


def neighbours(grid, x, y):
	assert(grid[x][y] == ".")
	ret = []
	if grid[x - 1][y] == ".":
		ret.append((x - 1, y))
	if grid[x + 1][y] == ".":
		ret.append((x + 1, y))
	if grid[x][y - 1] == ".":
		ret.append((x, y - 1))
	if grid[x][y + 1] == ".":
		ret.append((x, y + 1))
	return ret


def all_dead_ends(grid):					# All points that connect only to 1 other point.
	width, height = width_height(grid)
	ret = []
	for x in range(width):
		for y in range(height):
			if grid[x][y] == ".":
				if len(neighbours(grid, x, y)) == 1:
					ret.append((x, y))
	return ret


def anti_dead_end(original, startx, starty, endx, endy):

	width, height = width_height(original)
	grid = copy.deepcopy(original)

	queue = all_dead_ends(grid)
	been_in_queue = set(queue)
	qi = 0

	while qi < len(queue):
		x, y = queue[qi]

		all_neighbours = neighbours(grid, x, y)
		assert(len(all_neighbours) == 1)
		neighbour = all_neighbours[0]

		grid[x][y] = "O"					# FIXME? - dangerous to have 2 types of wall.

		if len(neighbours(grid, neighbour[0], neighbour[1])) == 1:
			if neighbour not in been_in_queue:
				if (neighbour[0] != startx or neighbour[1] != starty) and (neighbour[0] != endx or neighbour[1] != endy):
					queue.append((neighbour[0], neighbour[1]))
					been_in_queue.add(neighbour)

		qi += 1

	return grid

# -------------------------------------------------------------------------------------------------

main()
