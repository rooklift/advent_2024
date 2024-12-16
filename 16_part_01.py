import copy, time

# -------------------------------------------------------------------------------------------------

RIGHT = (1, 0)
LEFT = (-1, 0)
UP = (0, -1)
DOWN = (0, 1)

ALL_DIRECTIONS = [UP, RIGHT, DOWN, LEFT]

perpendicular_directions = {
	RIGHT: [UP, DOWN],
	LEFT: [UP, DOWN],
	UP: [LEFT, RIGHT],
	DOWN: [LEFT, RIGHT],
}

# -------------------------------------------------------------------------------------------------

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

# -------------------------------------------------------------------------------------------------

class State():

	# A state is a robot pointing in a certain direction, at a certain place.
	#
	# In general, it will have 2 or 3 options:
	#   - Turn left
	#   - Turn right
	#   - Go forward if possible (might not be)
	#
	# Note that turning 180 is not considered an option (but it can reach that state by 2 moves).

	def __init__(self, x, y, d):
		self.x = x
		self.y = y
		self.d = d
		self.connections = dict()           # (x, y, d) --> cost
		self.tiles_forward = set()          # set of (x, y) only  =  the tiles you go over when going forward, inclusive of both nodes

		if self.d in [RIGHT, LEFT]:
			self.connections[(self.x, self.y, UP)] = 1000
			self.connections[(self.x, self.y, DOWN)] = 1000
		else:
			self.connections[(self.x, self.y, LEFT)] = 1000
			self.connections[(self.x, self.y, RIGHT)] = 1000

	def __hash__(self):
		return hash(self.as_tuple())

	def __eq__(self, other):
		return self.as_tuple() == other.as_tuple()

	def as_tuple(self):
		return (self.x, self.y, self.d)

	def add_forward_connection(self, grid, possible_states):

		tiles = set()
		tiles.add((self.x, self.y))

		x = self.x
		y = self.y
		d = self.d

		cost = 0

		nextx = x + d[0]
		nexty = y + d[1]

		if grid[nextx][nexty] != ".":
			return

		while True:

			# Move...

			x = x + d[0]
			y = y + d[1]
			cost += 1

			tiles.add((x, y))

			# Check if we reached a new node...

			if (x, y, d) in possible_states:
				self.connections[(x, y, d)] = cost
				self.tiles_forward = tiles
				return

			# Is it OK to continue moving?

			nextx = x + d[0]
			nexty = y + d[1]

			if grid[nextx][nexty] != ".":

				# We're either turning left or right.

				cost += 1000

				choices = 0

				for nextd in perpendicular_directions[d]:
					nextx = x + nextd[0]
					nexty = y + nextd[1]
					if grid[nextx][nexty] == ".":
						d = nextd
						choices += 1

				assert(choices == 1)

# -------------------------------------------------------------------------------------------------

def all_possible_states(grid, startx, starty, endx, endy):

	# Returns all possible states the robot can be in, at the moment when it has to make decisions.
	# As a dictionary of (x, y, d) --> State object.

	width, height = width_height(grid)

	foo = dict()

	start_present = False
	end_present = False

	for x in range(width):
		for y in range(height):
			if grid[x][y] == ".":
				dirs_out = directions_out(grid, x, y)
				if len(dirs_out) != 2:						# i.e. it's neither a dead-end nor a junction
					for d in ALL_DIRECTIONS:
						foo[(x, y, d)] = State(x, y, d)
					if x == startx and y == starty:
						start_present = True
					if x == endx and y == endy:
						end_present = True

	if not start_present:
		for d in ALL_DIRECTIONS:
			foo[(startx, starty, d)] = State(startx, starty, d)

	if not end_present:
		for d in ALL_DIRECTIONS:
			foo[(endx, endy, d)] = State(endx, endy, d)

	return foo

# -------------------------------------------------------------------------------------------------

def all_dead_ends(grid):                    # All points that connect only to 1 other point.
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

		grid[x][y] = "O"                    # FIXME? - dangerous to have 2 types of wall.

		if len(neighbours(grid, neighbour[0], neighbour[1])) == 1:
			if neighbour not in been_in_queue:
				if (neighbour[0] != startx or neighbour[1] != starty) and (neighbour[0] != endx or neighbour[1] != endy):
					queue.append((neighbour[0], neighbour[1]))
					been_in_queue.add(neighbour)

		qi += 1

	return grid

# -------------------------------------------------------------------------------------------------
# So I asked Claude in general terms how to implement Dijkstra and Claude told me this:

"""
	1. Start with your starting city. Mark its "distance from start" as 0, and all other cities as "infinity" distance.
	2. Keep a list of "cities to consider" and "cities we're done with". Initially, only your starting city is "to consider".
	3. Among all cities you're currently considering, look at the one with shortest "distance from start". Call this the "current city":
		3.1. If this "current city" is in the "done" list, skip it (go back to step 3).
	4. Look at all roads leading out from the current city. For each one:
		4.1. Calculate total distance if you went through current city to reach that neighbor
		4.2. If this total is less than that neighbor's currently recorded distance:
			4.3. Update the neighbor's recorded distance
			4.4. Add the neighbor to "cities to consider" (even if it's been considered before)
	5. Mark current city as "done" - we've found the shortest possible path to it
	6. Repeat steps 3-5 until you reach your destination city
"""

# WARNING: I AM NOT 100% SURE ABOUT THE GENERAL CORRECTNESS OF THIS!

def my_dijkstra(possible_states, start, end):			# Returns distance only

	# Step 1:

	distances = dict()			# state --> dist from start

	for state in possible_states.values():
		distances[state] = 999999999

	distances[start] = 0

	# Step 2:

	consider = [start]
	done = set()

	while True:

		# Step 3:

		consider.sort(key = lambda foo : distances[foo])
		current = consider.pop(0)

		# Step 3.1:

		if current in done:
			continue

		# Step 4:

		for neighbour_tup, distance in current.connections.items():

			neighbour = possible_states[neighbour_tup]

			# Step 4.1:

			total_to_neighbour = distances[current] + distance

			if total_to_neighbour < distances[neighbour]:				# Step 4.2
				distances[neighbour] = total_to_neighbour				# Step 4.3
				consider.append(neighbour)								# Step 4.4

		# Step 5:

		done.add(current)

		if end in done:
			return distances[end]

# -------------------------------------------------------------------------------------------------

def main():

	original, startx, starty, endx, endy = parser("16_input.txt")
	width, height = width_height(original)

	# Remove dead ends from the grid... this simplifies various things...

	t = time.time()
	grid = anti_dead_end(original, startx, starty, endx, endy)
	print(f"Dead-end removal took: {time.time() - t}")

	# Find all possible states the robot can be in while deciding what to do...

	t = time.time()
	possible_states = all_possible_states(grid, startx, starty, endx, endy)
	print(f"Possible state creation took: {time.time() - t}")

	# When states are created they auto-add their trivial moves, but need to update themselves
	# with any real move, once the grid exists...

	t = time.time()
	for state in possible_states.values():
		state.add_forward_connection(grid, possible_states)
	print(f"Forward connections took: {time.time() - t}")

	# Now solve...

	start = possible_states[(startx, starty, RIGHT)]
	end = possible_states[(endx, endy, UP)]				# Empirically known to be the best way to end.

	t = time.time()
	result = my_dijkstra(possible_states, start, end)
	print(f"Dijkstra took: {time.time() - t}")
	print("----")
	print(f"RESULT: {result}")

main()