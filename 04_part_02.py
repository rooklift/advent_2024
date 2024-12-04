def parser(filename):
	with open(filename) as infile:
		lines = [line.strip() for line in infile.readlines() if line.strip() != ""]
	ret = []
	for c in lines[0]:
		ret.append([])
	for line in lines:
		for x, c in enumerate(line):
			ret[x].append(c)
	return ret

def read(arr, x, y, dx, dy, length):
	s = ""
	for i in range(0, length):
		ax = x + dx * i
		ay = y + dy * i
		if ax < 0 or ay < 0:
			s += "."
		else:
			try:
				s += arr[ax][ay]
			except:
				s += "."
	return s

def validate(arr, x, y):
	return read(arr, x - 1, y - 1, 1, 1, 3) in ["SAM", "MAS"] and read(arr, x - 1, y + 1, 1, -1, 3) in ["SAM", "MAS"]

def main():
	arr = parser("04_input.txt")
	count = 0
	for x in range(len(arr) - 1):
		for y in range(len(arr[0]) - 1):
			if validate(arr, x, y):
				count += 1
	print(count)

main()
