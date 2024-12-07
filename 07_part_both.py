def parser(filename):
	with open(filename) as infile:
		lines = [line.strip() for line in infile.readlines() if line.strip() != ""]
	ret = dict()
	for line in lines:
		foo = line.split(":")
		key = int(foo[0])
		vals = [int(s) for s in foo[1].split()]
		if key in ret:
			raise ValueError								# Ensure each key is unique in the input...
		ret[key] = vals
	return ret


def main():
	data = parser("07_input.txt")
	p1 = 0
	p2 = 0
	for key in data:
		p1 += test(key, data[key][0], data[key][1:])
		p2 += test(key, data[key][0], data[key][1:], True)
	print(p1)
	print(p2)


def test(target, acc, vals, concat = False):				# Either returns target or 0
	if len(vals) == 0:
		if acc == target:
			return target
		else:
			return 0
	add = acc + vals[0]
	mult = acc * vals[0]
	if test(target, add, vals[1:], concat) or test(target, mult, vals[1:], concat):
		return target
	elif concat:
		foo = int(str(acc) + str(vals[0]))
		if test(target, foo, vals[1:], True):
			return target
		else:
			return 0
	else:
		return 0


main()
