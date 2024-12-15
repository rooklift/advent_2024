def parser(filename):

	with open(filename) as infile:
		raw = infile.read()

	raw = raw.replace("#", "##")
	raw = raw.replace("O", "[]")
	raw = raw.replace(".", "..")
	raw = raw.replace("@", "@.")

	parts = raw.split("\n\n")
	maze_lines = parts[0].split("\n")

	maze = []
	for c in maze_lines[0]:
		maze.append([])

	for line in maze_lines:
		for x, c in enumerate(line):
			maze[x].append(c)

	directions = []

	for c in parts[1]:
		if c in "^>v<":
			directions.append(c)

	return maze, "".join(directions)


vecs = {
	"<": [-1, 0],
	">": [1, 0],
	"^": [0, -1],
	"v": [0, 1]
}

# -------------------------------------------------------------------------------------------------
# Note we store moveables as (c, x, y) where c is "[" or "]"

def this_half(maze, x, y):
	assert(maze[x][y] in "[]")
	return (maze[x][y], x, y)


def other_half(maze, x, y):
	assert(maze[x][y] in "[]")
	if maze[x][y] == "[":
		return ("]", x + 1, y)
	else:
		return ("[", x - 1, y)

# -------------------------------------------------------------------------------------------------

def get_moveables(maze, direction, box_x, box_y):
	if direction in "<>":
		return get_moveables_horizontal(maze, direction, box_x, box_y)
	else:
		return get_moveables_vertical(maze, direction, box_x, box_y)


def get_moveables_horizontal(maze, direction, x, y):

	ret = []
	ret.append(this_half(maze, x, y))

	while True:
		x += vecs[direction][0]
		if maze[x][y] == ".":
			return ret
		elif maze[x][y] == "#":
			return []
		elif maze[x][y] in "[]":
			ret.append(this_half(maze, x, y))
		else:
			raise AssertionError


def get_moveables_vertical(maze, direction, box_x, box_y):

	items = get_connected_vertical(maze, direction, box_x, box_y)

	ret = []

	for item in items:

		x = item[1]
		y = item[2]

		new_y = y + vecs[direction][1]

		if maze[x][new_y] == "#":
			return []
		else:
			ret.append(item)

	return ret


def get_connected_vertical(maze, direction, x, y):

	result = set();
	result.add(this_half(maze, x, y))
	result.add(other_half(maze, x, y))

	queue = [
		this_half(maze, x, y),
		other_half(maze, x, y)
	]

	while len(queue) > 0:

		item = queue.pop(0)

		x = item[1]
		y = item[2]

		new_y = y + vecs[direction][1]

		if maze[x][new_y] in "[]":
			result.add(this_half(maze, x, new_y))
			result.add(other_half(maze, x, new_y))
			queue.append(this_half(maze, x, new_y))
			queue.append(other_half(maze, x, new_y))

	return list(result)

# -------------------------------------------------------------------------------------------------

def main():

	maze, directions = parser("15_input.txt")

	width = len(maze)
	height = len(maze[0])

	for x in range(width):
		for y in range(height):
			if maze[x][y] == "@":
				rx = x
				ry = y
				maze[x][y] = "."

	for c in directions:
		rx, ry = update(maze, c, rx, ry)				# Also updates maze as a side-effect

	result = 0

	for x in range(width):
		for y in range(height):
			if maze[x][y] == "[":
				result += x + y * 100

	print(result)


def update(maze, direction, rx, ry):				# Update maze... return robot_x, robot_y

	assert(maze[rx][ry] == ".")

	next_robot_x = rx + vecs[direction][0]
	next_robot_y = ry + vecs[direction][1]

	if maze[next_robot_x][next_robot_y] == "#":		# Wall in our way
		return rx, ry

	if maze[next_robot_x][next_robot_y] == ".":		# Moving to empty space
		return next_robot_x, next_robot_y

	assert(maze[next_robot_x][next_robot_y] in "[]")

	moveables = get_moveables(maze, direction, next_robot_x, next_robot_y)

	if len(moveables) == 0:							# Box is in our way but can't be moved
		return rx, ry

	for item in moveables:
		maze[item[1]][item[2]] = "."

	for item in moveables:
		new_x = item[1] + vecs[direction][0]
		new_y = item[2] + vecs[direction][1]
		maze[new_x][new_y] = item[0]

	return next_robot_x, next_robot_y				# We moved some boxes


main()
