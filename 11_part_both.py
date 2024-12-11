from collections import defaultdict

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
		return [int(a), int(b)]
	return [stone * 2024]

def main():
	raw_vals = parser("11_input.txt")
	stones = defaultdict(int)			# Val --> count
	for val in raw_vals:
		stones[val] += 1
	for n in range(75):
		next_stones = defaultdict(int)
		for stone, count in stones.items():
			update = act(stone)
			for val in update:
				next_stones[val] += count
		stones = next_stones
		if n in [24, 74]:
			result = 0
			for stone, count in stones.items():
				result += count
			print(result)

main()
