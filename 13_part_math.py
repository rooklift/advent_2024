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

	def same_direction(self, other):			# OK I asked Claude how to check this. Only used for assertions anyway.
		return self.x * other.y == self.y * other.x

# -------------------------------------------------------------------------------------------------

class Machine():

	def __init__(self, a, b, prize):			# Where everything is a Vector.
		self.a = a
		self.b = b
		self.prize = prize
		self.check_directions()

	def check_directions(self):
		assert(not self.prize.same_direction(self.a))
		assert(not self.prize.same_direction(self.b))
		assert(not self.a.same_direction(self.b))

# -------------------------------------------------------------------------------------------------
# https://www.geeksforgeeks.org/program-for-point-of-interception-of-two-lines/

def line_line_intercept(A, B, C, D):

	# Line AB represented as a1x + b1y = c1

	a1 = B.y - A.y
	b1 = A.x - B.x
	c1 = a1 * A.x + b1 * A.y

	# Line CD represented as a2x + b2y = c2

	a2 = D.y - C.y
	b2 = C.x - D.x
	c2 = a2 * C.x + b2 * C.y

	determinant = a1 * b2 - a2 * b1

	if (determinant == 0):
		return None
	else:
		x = (b2 * c1 - b1 * c2) / determinant
		y = (a1 * c2 - a2 * c1) / determinant
		return Vector(x, y)

# -------------------------------------------------------------------------------------------------

def cost_mathy(mc):

	intercept = line_line_intercept(Vector(0, 0), mc.a, mc.prize, Vector(mc.prize.x + mc.b.x, mc.prize.y + mc.b.y))

	if intercept == None:
		return 0

	if intercept.x < 0 or intercept.y < 0 or intercept.x > mc.prize.x or intercept.y > mc.prize.y:
		return 0

	intercept.x = round(intercept.x)			# This might be quite a big adjustment but we only need the
	intercept.y = round(intercept.y)			# closest ints to the real intercept since we validate later.

	pa = intercept.x // mc.a.x
	pb = (mc.prize.x - intercept.x) // mc.b.x

	# Validate that pa presses of A and pb presses of B actually work...

	if pa * mc.a.x + pb * mc.b.x != mc.prize.x:
		return 0

	if pa * mc.a.y + pb * mc.b.y != mc.prize.y:
		return 0

	return (pa * A_COST) + (pb * B_COST)

# -------------------------------------------------------------------------------------------------

def main():
	machines1, machines2 = parser("13_input.txt")
	p1 = 0
	for machine in machines1:
		p1 += cost_mathy(machine)
	p2 = 0
	for machine in machines2:
		p2 += cost_mathy(machine)
	print(p1)
	print(p2)

main()
