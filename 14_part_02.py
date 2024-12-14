import sys, time
from PIL import Image


WIDTH = 101		# So indexes 0 to 100 inclusive
HEIGHT = 103	#            0 to 102


class Robot():
	def __init__(self, x, y, vx, vy):
		self.x = x
		self.y = y
		self.vx = vx
		self.vy = vy

	def position_after(self, ticks):	# In Python anyway, -1 % 4 == 3
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
	robots = parser("14_input.txt")
	for i in range(0, WIDTH * HEIGHT):		# After this many ticks everything will be back where it started, I think.
		positions = set()
		for robot in robots:
			x, y = robot.position_after(i)
			positions.add((x, y))
		draw_positions(positions, f"./14_images/{i}.png")


def draw_positions(positions, outfilename):
	img = Image.new("RGB", (WIDTH, HEIGHT), color = "black")
	for x, y in positions:
		img.putpixel((x, y), (255, 255, 255))
	img.save(outfilename)


main()
