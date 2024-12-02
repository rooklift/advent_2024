def parser(filename):

	with open(filename) as infile:
		rawlines = [line.strip() for line in infile.readlines() if line.strip() != ""]

	token_lists = [line.split() for line in rawlines]

	return [[int(s) for s in l] for l in token_lists]


def same_sign(a, b):				# Don't care about cases where either number is zero
	if a < 0 and b < 0:
		return True
	if a > 0 and b > 0:
		return True
	return False


def main():

	num_list = parser("02_input.txt")

	count = 0

	for line in num_list:
		last_diff = None
		for i in range(len(line) - 1):
			diff = line[i + 1] - line[i]
			if abs(diff) < 1 or abs(diff) > 3:
				break
			if last_diff != None and not same_sign(diff, last_diff):
				break
			last_diff = diff
		else:						# The "else" is run if the inner for loop is NOT broken.
			count += 1

	print(count)


main()
