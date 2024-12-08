def parser(filename):
	ret = dict()
	with open(filename) as infile:
		lines = [line.strip() for line in infile.readlines() if line.strip() != ""]
	width = len(lines[0])
	height = len(lines)
	for y, line in enumerate(lines):
		for x, c in enumerate(line):
			if c != ".":
				if c in ret:
					ret[c].append((x, y))
				else:
					ret[c] = [(x, y)]
	return ret, width, height


def get_p1_antinodes(data, width, height, x1, y1, x2, y2):
	ret = []
	dx = x2 - x1
	dy = y2 - y1
	newx1 = x1 - dx
	newy1 = y1 - dy
	if newx1 >= 0 and newx1 < width and newy1 >= 0 and newy1 < height:
		ret.append((newx1, newy1))
	newx2 = x2 + dx
	newy2 = y2 + dy
	if newx2 >= 0 and newx2 < width and newy2 >= 0 and newy2 < height:
		ret.append((newx2, newy2))
	return ret


def get_p2_antinodes(data, width, height, x1, y1, x2, y2):
	ret = set()
	dx = x2 - x1
	dy = y2 - y1
	ax = x1
	ay = y1
	while ax >= 0 and ax < width and ay >= 0 and ay < width:
		ret.add((ax, ay))
		ax += dx
		ay += dy
	ax = x1
	ay = y1
	while ax >= 0 and ax < width and ay >= 0 and ay < width:
		ret.add((ax, ay))
		ax -= dx
		ay -= dy
	return list(ret)


def main():
	data, width, height = parser("08_input.txt")
	p1_antinodes = set()
	p2_antinodes = set()
	for c in data:
		locs = data[c]
		for i in range(len(locs)):
			x1, y1 = locs[i]
			for j in range(i + 1, len(locs)):
				x2, y2 = locs[j]
				for a in get_p1_antinodes(data, width, height, x1, y1, x2, y2):
					p1_antinodes.add(a)
				for a in get_p2_antinodes(data, width, height, x1, y1, x2, y2):
					p2_antinodes.add(a)
	print(len(p1_antinodes))
	print(len(p2_antinodes))


main()
