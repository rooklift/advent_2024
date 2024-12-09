def parser(filename):
	with open(filename) as infile:
		data = infile.read().strip()
	return data

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

def load_data(data):

	files = []
	spaces = []

	fid = 0
	empty = False
	location = 0

	for c in data:
		val = int(c)
		if not empty:
			files.append(Item(fid, location, val))
			fid += 1
		else:
			spaces.append(Item(None, location, val))
		empty = not empty
		location += val

	return files, spaces


def main():

	files, spaces = load_data(parser("09_input.txt"))

	for file in files[::-1]:
		for space in spaces:
			if space.location > file.location:
				break
			if file.length <= space.length:
				file.location = space.location
				space.length -= file.length
				space.location += file.length
				break

	result = 0

	for file in files:
		result += file.checksum()

	print(result)



main()
