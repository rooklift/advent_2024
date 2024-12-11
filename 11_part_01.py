def parser(filename):
	with open(filename) as infile:
		raw = infile.read()
	tokens = raw.split()
	return [int(s) for s in tokens]


def act(stone):
	if stone == 0:
		return [1]
	s = str(stone)
	if len(s) % 2 == 0:
		a = s[:len(s) // 2]
		b = s[len(s) // 2:]
		while a.startswith("0") and len(a) > 1:
			a = a[1:]
		while b.startswith("0") and len(b) > 1:
			b = b[1:]
		return [int(a), int(b)]
	return [stone * 2024]


def main():
	stones = parser("11_input.txt")
	for n in range(25):
		update = []
		for stone in stones:
			update.append(act(stone))

		stones = []
		for up in update:
			for s in up:
				stones.append(s)
	print(len(stones))


main()
