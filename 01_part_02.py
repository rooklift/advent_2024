def parser(filename):
	left = []
	right = []
	with open(filename) as infile:
		lines = [line.strip() for line in infile.readlines() if line.strip() != ""]
	for line in lines:
		tokens = line.split()
		left.append(int(tokens[0]))
		right.append(int(tokens[1]))
	return left, right

def main():
	left, right = parser("01_input.txt")
	right_dict = dict()
	for n in right:
		if n in right_dict:
			right_dict[n] += 1
		else:
			right_dict[n] = 1
	count = 0
	for n in left:
		if n in right_dict:
			count += n * right_dict[n]
	print(count)

main()
