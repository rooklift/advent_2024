A_COST = 3
B_COST = 1

def parser(filename):
	with open(filename) as infile:
		raw = infile.read()
	ret1 = []
	ret2 = []
	machines = raw.split("\n\n")
	for machine in machines:
		lines = [line.strip() for line in machine.split("\n") if line.strip() != ""]
		ax = int(lines[0].split("X+")[1].split(",")[0])
		ay = int(lines[0].split("Y+")[1])
		bx = int(lines[1].split("X+")[1].split(",")[0])
		by = int(lines[1].split("Y+")[1])
		prizex = int(lines[2].split("X=")[1].split(",")[0])
		prizey = int(lines[2].split("Y=")[1])
		a = Vector(ax, ay)
		b = Vector(bx, by)
		prize1 = Vector(prizex, prizey)
		prize2 = Vector(prizex + 10000000000000, prizey + 10000000000000)
		ret1.append(Machine(a, b, prize1))
		ret2.append(Machine(a, b, prize2))
	return ret1, ret2

# -------------------------------------------------------------------------------------------------

class Vector():
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def __str__(self):
		return f"({self.x},{self.y})"


def same_direction(vec1, vec2):					# OK I asked Claude how to check this. Only used for assertions anyway.
	return vec1.x * vec2.y == vec1.y * vec2.x

# -------------------------------------------------------------------------------------------------

class Machine():

	def __init__(self, a, b, prize):			# Where everything is a Vector.
		self.a = a
		self.b = b
		self.prize = prize
		self.a_steepness = self.a.y / self.a.x
		self.b_steepness = self.b.y / self.b.x
		self.prize_steepness = self.prize.y / self.prize.x
		self.high = self.intercept_is_high()
		self.low = self.intercept_is_low()
		self.possible = self.high or self.low
		self.check_directions()

	def check_directions(self):
		assert(not same_direction(self.prize, self.a))
		assert(not same_direction(self.prize, self.b))
		assert(not same_direction(self.a, self.b))

	def __str__(self):
		return f"A: {self.a.x}, {self.a.y};  B: {self.b.x}, {self.b.y};  Pz: {self.prize.x}, {self.prize.y}"

	def intercept_is_high(self):
		return self.a_steepness > self.prize_steepness and self.prize_steepness > self.b_steepness

	def intercept_is_low(self):
		return self.b_steepness > self.prize_steepness and self.prize_steepness > self.a_steepness

	def cost_for_a_presses(self, pa):			# Returns 0 if this is not a solution.
		ix = self.a.x * pa
		iy = self.a.y * pa
		if ix > self.prize.x or iy > self.prize.y:
			return 0
		dx = self.prize.x - ix
		dy = self.prize.y - iy
		if dx % self.b.x == 0 and dy % self.b.y == 0:
			if dx // self.b.x == dy // self.b.y:
				pb = dx // self.b.x
				return (pa * A_COST) + (pb * B_COST)
		return 0

	def presses_a_wrongness_sign(self, pa):

		# Returns -1 if this isn't enough a presses, 1 if it's too many a presses, and 0 if it's just right.

		if not self.possible:
			raise AssertionError

		x = pa * self.a.x
		y = pa * self.a.y

		dx = self.prize.x - x
		dy = self.prize.y - y

		implied_b_steepness = dy / dx

		if self.low:
			if implied_b_steepness < self.b_steepness:
				return -1
			elif implied_b_steepness > self.b_steepness:
				return 1
			else:
				return 0

		if self.high:
			if implied_b_steepness < self.b_steepness:
				return 1
			elif implied_b_steepness > self.b_steepness:
				return -1
			else:
				return 1

		raise AssertionError

# -------------------------------------------------------------------------------------------------

def cost_stupid(mc):							# Simple brute force. Return 0 if impossible.
	if not mc.possible:
		return 0
	best = None
	for pa in range(100):
		cost = mc.cost_for_a_presses(pa)
		if not cost:
			continue
		elif best == None:
			best = cost
		elif cost < best:						# Actually impossible unless vectors can align, which they don't.
			best = cost
	if best == None:
		return 0
	else:
		return best


def cost_smart(mc):

	if not mc.possible:
		return 0

	# First thing to do: binary-search for the right number of times to press A:
	# Terminating when the possibles are under 10 in number, avoid worrying about edge cases.

	lower = 0
	upper = mc.prize.x // mc.a.x

	while True:

		if upper - lower < 10:
			break

		mid = lower + (upper - lower) // 2

		wrongness_sign = mc.presses_a_wrongness_sign(mid)

		if wrongness_sign < 0:					# Need more pushes of A
			lower = mid
		elif wrongness_sign >= 0:				# Need less pushes of A, or exactly this number
			upper = mid

	# Now we have a small range of possibles:

	for pa in range(lower, upper + 1):
		ret = mc.cost_for_a_presses(pa)
		if ret:
			return ret

	return 0

# -------------------------------------------------------------------------------------------------

def main():
	machines1, machines2 = parser("13_input.txt")
	p1 = 0
	for machine in machines1:
		p1 += cost_stupid(machine)				# Original simple solution.
	p2 = 0
	for machine in machines2:
		p2 += cost_smart(machine)				# More complex solution.
	print(p1)
	print(p2)

main()
