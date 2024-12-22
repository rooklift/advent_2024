import itertools


def parser(filename):
	with open(filename) as infile:
		return [int(s) for s in infile.readlines() if s.strip() != ""]


def iterate(n):
	n ^= n * 64
	n %= 16777216
	n ^= n // 32
	n %= 16777216
	n ^= n * 2048
	n %= 16777216
	return n


class Monkey():
	def __init__(self, num):
		self.make_seq(num)
		self.make_diffs()
		self.make_lookup()

	def make_seq(self, num):
		self.seq = [num]
		for n in range(2000):
			num = iterate(num)
			self.seq.append(num)

	def make_diffs(self):
		self.diffs = [None]
		for i in range(1, len(self.seq)):
			self.diffs.append((self.seq[i] % 10) - (self.seq[i - 1] % 10))

	def make_lookup(self):
		self.lookup = dict()
		for i in range(3, len(self.diffs)):
			key = (self.diffs[i - 3], self.diffs[i - 2], self.diffs[i - 1], self.diffs[i])
			if key in self.lookup:
				continue
			self.lookup[key] = self.seq[i] % 10


def diffs_are_possible(diffs):
	# Top is the highest possible value of the principal thing, bottom the lowest
	top = 9
	bottom = 0
	for diff in diffs:
		top += diff
		bottom += diff
		top = min(9, top)
		bottom = max(bottom, 0)
		if bottom >= 10 or top < 0:
			return False
	return True


def main():

	monkeys = [Monkey(num) for num in parser("22_input.txt")]

	p2_best = 0

	for foo in itertools.product(range(-9, 10), repeat = 4):
		if not diffs_are_possible(foo):
			continue
		print(list(foo))
		p2_try = 0
		for m in monkeys:
			try:
				p2_try += m.lookup[tuple(foo)]
			except KeyError:
				pass
		if p2_try > p2_best:
			p2_best = p2_try

	print(p2_best)


main()
