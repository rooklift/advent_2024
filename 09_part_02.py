
class Item():										# Either a file or a region of empty space
	def __init__(self, fid, location, length):
		self.fid = fid
		self.location = location
		self.length = length

	def checksum(self):
		ret = 0
		for i in range(self.location, self.location + self.length):
			ret += self.fid * i
		return ret


def parser(filename):

	with open(filename) as infile:
		data = infile.read().strip()

	files = []
	spaces = []

	location = 0

	for i, c in enumerate(data):
		val = int(c)
		empty = i % 2 == 1
		if not empty:
			fid = i // 2
			files.append(Item(fid, location, val))
		else:
			spaces.append(Item(None, location, val))
		location += val

	return files, spaces


def main():

	files, spaces = parser("09_input.txt")

	for file in files[::-1]:
		for space in spaces:
			if space.location > file.location:
				break
			if file.length <= space.length:
				file.location = space.location
				space.length -= file.length
				space.location += file.length
				break

	# We rely on the fact that we never need to merge empty spaces.

	result = 0

	for file in files:
		result += file.checksum()

	print(result)


main()
