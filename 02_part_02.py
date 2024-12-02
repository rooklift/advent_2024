def parser(filename):
	with open(filename) as infile:
		rawlines = [line.strip() for line in infile.readlines() if line.strip() != ""]
	token_lists = [line.split() for line in rawlines]
	return [[int(s) for s in l] for l in token_lists]


def same_sign(a, b):				# Don't care about cases where either number is zero
	return (a < 0 and b < 0) or (a > 0 and b > 0)


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


def alternatives(arr):
	ret = []
	ret.append(arr.copy())
	for ri in range(len(arr)):
		alt = []
		for n in range(len(arr)):
			if n != ri:
				alt.append(arr[n])
		ret.append(alt)
	return ret


def main():
	num_list = parser("02_input.txt")
	count = 0
	for line in num_list:
		for alt in alternatives(line):
			if sequence_is_safe(alt):
				count += 1
				break
	print(count)


main()
