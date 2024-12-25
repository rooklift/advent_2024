def parser(filename):
	with open(filename) as infile:
		schema = [item.strip() for item in infile.read().split("\n\n")]
	keys = []
	locks = []
	for item in schema:
		if item.endswith("#####"):
			keys.append(parse_item(item, True))
		elif item.startswith("#####"):
			locks.append(parse_item(item))
		else:
			raise ValueError
	return keys, locks


def parse_item(schematic, upsidedown = False):
	lines = schematic.split("\n")
	vals = [None, None, None, None, None]
	if upsidedown:
		lines = lines[::-1]
	for y, line in enumerate(lines):
		for x, c in enumerate(line):
			if c == "." and vals[x] == None:
				vals[x] = y - 1
	assert(None not in vals)
	return tuple(vals)


def main():
	keys, locks = parser("25_input.txt")
	result = 0
	for key in keys:
		for lock in locks:
			ok = True
			for x in range(5):
				if key[x] + lock[x] > 5:
					ok = False
					break
			if ok:
				result += 1
	print(result)


main()
