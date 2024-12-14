WIDTH = 101		# So indexes 0 to 100 inclusive
HEIGHT = 103	#            0 to 102

class Robot():
	def __init__(self, x, y, vx, vy):
		self.x = x
		self.y = y
		self.vx = vx
		self.vy = vy

	def position_after(self, ticks):

		# In Python anyway, -1 % 4 == 3

		return (self.x + (self.vx * ticks)) % WIDTH, (self.y + (self.vy * ticks)) % HEIGHT


def parser(filename):
	with open(filename) as infile:
		lines = [line.strip() for line in infile.readlines() if line.strip() != ""]
	ret = []
	for line in lines:
		x = int(line.split("p=")[1].split(",")[0])
		y = int(line.split(",")[1].split(" v=")[0])
		vx = int(line.split("v=")[1].split(",")[0])
		vy = int(line.split(",")[2])
		ret.append(Robot(x, y, vx, vy))
	return ret

def main():

	if True:
		robots = parser("14_input.txt")
	else:
		robots = parser("14_test.txt")
		global WIDTH
		global HEIGHT
		WIDTH = 11
		HEIGHT = 7

	count_nw = 0
	count_ne = 0
	count_sw = 0
	count_se = 0

	MIDX = (WIDTH - 1) // 2
	MIDY = (HEIGHT - 1) // 2

	for robot in robots:
		x, y = robot.position_after(100)

		if x < MIDX and y < MIDY:
			count_nw += 1
		elif x > MIDX and y < MIDY:
			count_ne += 1
		elif x < MIDX and y > MIDY:
			count_sw += 1
		elif x > MIDX and y > MIDY:
			count_se += 1

	print(count_nw * count_ne * count_sw * count_se)

main()
