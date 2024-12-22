import functools

def parser(filename):
	with open(filename) as infile:
		return [int(s) for s in infile.readlines() if s.strip() != ""]

@functools.cache
def iterate(n):
	n ^= n * 64
	n %= 16777216
	n ^= n // 32
	n %= 16777216
	n ^= n * 2048
	n %= 16777216
	return n

def main():
	nums = parser("22_input.txt")
	result = 0
	for num in nums:
		for n in range(2000):
			num = iterate(num)
		result += num
	print(result)

main()
