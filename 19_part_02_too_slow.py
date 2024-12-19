def parser(filename):
	with open(filename) as infile:
		raw = infile.read()
	parts = raw.split("\n\n")
	tokens = parts[0].split(", ")
	targets = [line.strip() for line in parts[1].split("\n") if line.strip() != ""]
	return tokens, targets


def main():
	tokens, targets = parser("19_input.txt")
	p1 = 0
	p2 = 0
	for target in targets:
		ways = ways_to_build(tokens, target)
		if ways > 0:
			p1 += 1
			p2 += ways
	print(p1)
	print(p2)


def ways_to_build(tokens, target):
	if len(target) == 0:
		return 1
	ret = 0
	for token in tokens:
		if target.startswith(token):
			ret += ways_to_build(tokens, target[len(token):])
	return ret


main()
