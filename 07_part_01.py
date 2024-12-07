def parser(filename):
	with open(filename) as infile:
		lines = [line.strip() for line in infile.readlines() if line.strip() != ""]
	ret = dict()
	for line in lines:
		foo = line.split(":")
		key = int(foo[0])
		vals = [int(s) for s in foo[1].split()]
		if key in ret:
			raise ValueError		# Ensure each key is unique in the input...
		ret[key] = vals
	return ret


def main():
	data = parser("07_input.txt")
	result = 0
	for key in data:
		print(result)
		result += test(key, data[key][0], data[key][1:])
	print(result)


def test(target, acc, vals):				# Either returns target or 0
	if len(vals) == 0:
		if acc == target:
			return target
		else:
			return 0
	add = acc + vals[0]
	mult = acc * vals[0]
	if test(target, add, vals[1:]) or test(target, mult, vals[1:]):
		return target
	else:
		return 0


main()
