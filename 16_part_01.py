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


def main():
	original, startx, starty, endx, endy = parser("16_input.txt")
	grid = anti_dead_end(original, startx, starty, endx, endy)
	grid_to_png(grid, "16_anti.png")


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

		grid[x][y] = "O"

		if len(neighbours(grid, neighbour[0], neighbour[1])) == 1:
			if neighbour not in been_in_queue:
				if (neighbour[0] != startx or neighbour[1] != starty) and (neighbour[0] != endx or neighbour[1] != endy):
					queue.append((neighbour[0], neighbour[1]))
					been_in_queue.add(neighbour)

		qi += 1

	return grid


main()
