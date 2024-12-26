import zlib
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

	best_score = None
	best_string = None
	best_i = None

	for i in range(0, WIDTH * HEIGHT):		# After this many ticks everything will be back where it started, I think.
		positions = set()
		for robot in robots:
			x, y = robot.position_after(i)
			positions.add((x, y))
		s = get_string(positions)
		score = get_string_score(s)
		if best_score == None or score < best_score:
			best_score = score
			best_string = s
			best_i = i
	print(best_i)
	draw_string(best_string, "14_image.png")


def get_string(positions):
	chars = ["." for i in range(WIDTH * HEIGHT)]
	for x, y in positions:
		i = y * WIDTH + x
		chars[i] = "#"
	return "".join(chars)


def get_string_score(s):
	data = s.encode("utf-8")
	return len(zlib.compress(data))


def draw_string(s, outfilename):
	img = Image.new("RGB", (WIDTH, HEIGHT), color = "black")
	x, y = 0, 0
	for c in s:
		if c == "#":
			img.putpixel((x, y), (255, 255, 255))
		x += 1
		if x >= WIDTH:
			x = 0
			y += 1
	img.save(outfilename)


main()
