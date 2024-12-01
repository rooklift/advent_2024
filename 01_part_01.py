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
	left.sort()
	right.sort()
	count = 0
	for i in range(len(left)):
		count += abs(left[i] - right[i])
	print(count)

main()
