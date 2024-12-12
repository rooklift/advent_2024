def parser(filename):
	with open(filename) as infile:
		lines = [line.strip() for line in infile.readlines() if line.strip() != ""]
	ret = []
	for c in lines[0]:
		ret.append([])
	for line in lines:
		for x, c in enumerate(line):
			ret[x].append(c)
	return ret

vecs = [[1, 0], [-1, 0], [0, 1], [0, -1]]

def get_all_fields(grid):
	width = len(grid)
	height = len(grid[0])
	remaining = set()
	for x in range(width):
		for y in range(height):
			remaining.add((x, y))
	fields = []
	while len(remaining) > 0:
		x, y = list(remaining)[0]
		fp = field_points(grid, x, y, None)
		fields.append(fp)
		for x, y in fp:
			remaining.remove((x, y))
	return fields

def field_points(grid, x, y, result):
	width = len(grid)
	height = len(grid[0])
	if not result:
		result = set()
	result.add((x, y))
	for vec in vecs:
		newx = x + vec[0]
		newy = y + vec[1]
		if (newx, newy) not in result:
			if newx >= 0 and newx < width and newy >= 0 and newy < height:
				if grid[newx][newy] == grid[x][y]:
					field_points(grid, newx, newy, result)
	return result

def perimeter(field):
	ret = 0
	for x, y in field:
		for vec in vecs:
			newx = x + vec[0]
			newy = y + vec[1]
			if (newx, newy) not in field:
				ret += 1
	return ret

def main():
	grid = parser("12_input.txt")
	fields = get_all_fields(grid)
	result = 0
	for field in fields:
		result += len(field) * perimeter(field)
	print(result)

main()
