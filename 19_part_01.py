def parser(filename):
	with open(filename) as infile:
		raw = infile.read()
	parts = raw.split("\n\n")
	tokens = parts[0].split(", ")
	targets = [line.strip() for line in parts[1].split("\n") if line.strip() != ""]
	return tokens, targets


def main():
	tokens, targets = parser("19_input.txt")
	result = 0
	for target in targets:
		if can_build(tokens, target):
			result += 1
	print(result)


def can_build(tokens, target):

	if len(target) == 0:
		return True

	for token in tokens:
		if target.startswith(token):
			if can_build(tokens, target[len(token):]):
				return True

	return False


main()
