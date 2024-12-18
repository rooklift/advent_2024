from collections import deque

WIDTH = 71
HEIGHT = 71

TAR_X = 70
TAR_Y = 70

VECTORS = [(1, 0), (0, 1), (-1, 0), (0, -1)]

def parser(filename):
	with open(filename) as infile:
		lines = [line.strip() for line in infile.readlines() if line.strip() != ""]
	ret = []
	for line in lines:
		x = int(line.split(",")[0])
		y = int(line.split(",")[1])
		ret.append((x, y))
	return ret

def bfs(avoid):

	distances = dict(); distances[(0, 0)] = 0
	todo = deque(); todo.append((0, 0))

	while True:

		try:
			x, y = todo.popleft()
		except IndexError:
			return None

		for vec in VECTORS:

			new_x = x + vec[0]
			new_y = y + vec[1]

			if new_x < 0 or new_x >= WIDTH or new_y < 0 or new_y >= HEIGHT:
				continue

			if (new_x, new_y) in distances:
				continue

			if (new_x, new_y) in avoid:
				continue

			if (new_x, new_y) == (TAR_X, TAR_Y):
				return distances[(x, y)] + 1

			distances[(new_x, new_y)] = distances[(x, y)] + 1
			todo.append((new_x, new_y))


def main():

	data = parser("18_input.txt")

	print(bfs(data[:1024]))

	# -----

	lower = 0
	upper = len(data) - 1

	while True:
		mid = (upper + lower) // 2
		if bfs(set(data[:mid])) == None:
			upper = mid
		else:
			lower = mid
		if upper - lower < 5:
			break

	# I hate thinking about edge cases, just terminate the binary search when
	# there are < 5 items remaining and brute force all from there.

	for n in range(lower, upper + 1):
		if bfs(set(data[:n])) == None:
			x, y = data[n - 1]
			print(f"{x},{y}")
			break


main()
