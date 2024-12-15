def parser(filename):

	with open(filename) as infile:
		raw = infile.read()

	parts = raw.split("\n\n")
	maze_lines = parts[0].split("\n")

	maze = []
	for c in maze_lines[0]:
		maze.append([])

	for line in maze_lines:
		for i, c in enumerate(line):
			maze[i].append(c)

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
		rx, ry = update(maze, c, rx, ry)			# Also updates maze as a side-effect

	result = 0

	for x in range(width):
		for y in range(height):
			if maze[x][y] == "O":
				result += x + y * 100

	print(result)


def box_can_move(maze, direction, box_x, box_y):

	new_x = box_x + vecs[direction][0]
	new_y = box_y + vecs[direction][1]

	if maze[new_x][new_y] == ".":
		return True

	if maze[new_x][new_y] == "#":
		return False

	assert(maze[new_x][new_y] == "O")

	return box_can_move(maze, direction, new_x, new_y)


def move_box(maze, direction, box_x, box_y):

	# Rather than shove all the boxes in the way, we proceed as if the first box will
	# teleport to the first open space. This is equivalent.

	maze[box_x][box_y] = "."

	while True:
		box_x += vecs[direction][0]
		box_y += vecs[direction][1]
		if maze[box_x][box_y] == ".":
			maze[box_x][box_y] = "O"
			return


def update(maze, direction, rx, ry):		# Update maze... return robot_x, robot_y

	assert(maze[rx][ry] == ".")

	new_x = rx + vecs[direction][0]
	new_y = ry + vecs[direction][1]

	if maze[new_x][new_y] == "#":
		return rx, ry

	if maze[new_x][new_y] == ".":
		return new_x, new_y

	assert(maze[new_x][new_y] == "O")

	if box_can_move(maze, direction, new_x, new_y):
		move_box(maze, direction, new_x, new_y)
		return new_x, new_y
	else:
		return rx, ry


main()