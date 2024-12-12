# Just like the other solution, except using proper BFS to make the fields.

from collections import deque

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
		fp = field_points(grid, x, y)
		fields.append(fp)
		for x, y in fp:
			remaining.remove((x, y))
	return fields

def field_points(grid, x, y):
	width = len(grid)
	height = len(grid[0])
	result = set()
	result.add((x, y))
	queue = deque()
	queue.append((x, y))
	while queue:
		x, y = queue.popleft()
		for vec in vecs:
			newx = x + vec[0]
			newy = y + vec[1]
			if (newx, newy) not in result:
				if newx >= 0 and newx < width and newy >= 0 and newy < height:
					if grid[newx][newy] == grid[x][y]:
						result.add((newx, newy))			# Must add to result as soon as discovered, or else
						queue.append((newx, newy))			# it will end up in the queue multiple times.
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

def fence_count(field):

	# A fence is an uninterrupted stretch where there is field crop on one side and not on the other.

	ret = 0

	x1, y1, x2, y2 = bounds(field)

	# Horizontal scans...  (fixme: should look both ways at once?)

	for y in range(y1, y2):
		saw_fence_last_iter = False
		for x in range(x1, x2):
			if (x, y) not in field:
				saw_fence_last_iter = False
				continue
			if (x, y - 1) not in field:
				if not saw_fence_last_iter:
					ret += 1
				saw_fence_last_iter = True
			else:
				saw_fence_last_iter = False

	for y in range(y1, y2):
		saw_fence_last_iter = False
		for x in range(x1, x2):
			if (x, y) not in field:
				saw_fence_last_iter = False
				continue
			if (x, y + 1) not in field:
				if not saw_fence_last_iter:
					ret += 1
				saw_fence_last_iter = True
			else:
				saw_fence_last_iter = False

	# Vertical scans...  (fixme: should look both ways at once?)

	for x in range(x1, x2):
		saw_fence_last_iter = False
		for y in range(y1, y2):
			if (x, y) not in field:
				saw_fence_last_iter = False
				continue
			if (x - 1, y) not in field:
				if not saw_fence_last_iter:
					ret += 1
				saw_fence_last_iter = True
			else:
				saw_fence_last_iter = False

	for x in range(x1, x2):
		saw_fence_last_iter = False
		for y in range(y1, y2):
			if (x, y) not in field:
				saw_fence_last_iter = False
				continue
			if (x + 1, y) not in field:
				if not saw_fence_last_iter:
					ret += 1
				saw_fence_last_iter = True
			else:
				saw_fence_last_iter = False

	return ret

def bounds(field):
	x1 = 9999
	y1 = 9999
	x2 = -1
	y2 = -1
	for x, y in field:
		if x < x1:
			x1 = x
		if y < y1:
			y1 = y
		if x > x2:
			x2 = x
		if y > y2:
			y2 = y
	return x1, y1, x2 + 1, y2 + 1

def main():
	grid = parser("12_input.txt")
	fields = get_all_fields(grid)
	p1 = 0
	p2 = 0
	for field in fields:
		p1 += len(field) * perimeter(field)
		p2 += len(field) * fence_count(field)
	print(p1)
	print(p2)

main()
