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


def sequence_is_safe(arr):
	last_diff = None
	for i in range(len(arr) - 1):
		diff = arr[i + 1] - arr[i]
		if abs(diff) < 1 or abs(diff) > 3:
			return False
		if last_diff != None and not same_sign(diff, last_diff):
			return False
		last_diff = diff
	return True


def main():

	num_list = parser("02_input.txt")

	count = 0
	for line in num_list:
		if sequence_is_safe(line):
			count += 1

	print(count)


main()
