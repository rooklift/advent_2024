def parser(filename):
	with open(filename) as infile:
		raw = infile.read()
	ret = []
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
		prize = Vector(prizex, prizey)
		ret.append(Machine(a, b, prize))
	return ret

class Vector():
	def __init__(self, x, y):
		self.x = x
		self.y = y

class Machine():
	def __init__(self, a, b, prize):		# Where everything is a Vector
		self.a = a
		self.b = b
		self.prize = prize

	def __str__(self):
		return f"A: {self.a.x}, {self.a.y};  B: {self.b.x}, {self.b.y};  Pz: {self.prize.x}, {self.prize.y}"

def main():
	machines = parser("13_input.txt")
	p1 = 0
	for machine in machines:
		p1 += cost(machine)
	print(p1)

A_COST = 3
B_COST = 1

def cost(mc):								# Return 0 if impossible
	best = None
	for pa in range(100):
		x = mc.a.x * pa
		y = mc.a.y * pa
		if x > mc.prize.x or y > mc.prize.y:
			break
		dx = mc.prize.x - x
		dy = mc.prize.y - y
		pb = None
		if dx % mc.b.x == 0 and dy % mc.b.y == 0:
			if dx // mc.b.x == dy // mc.b.y:
				pb = dx // mc.b.x
		else:
			continue
		if pb == None:
			continue
		this_cost = (pa * A_COST) + (pb * B_COST)
		if best == None or this_cost < best:
			best =  this_cost
	if best == None:
		return 0
	else:
		return best

main()
