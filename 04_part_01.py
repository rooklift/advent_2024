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

vectors = [[1, 0], [1, 1], [1, -1], [0, 1], [0, -1], [-1, 0], [-1, 1], [-1, -1]]

def main():
	arr = parser("04_input.txt")
	count = 0
	for x in range(len(arr)):
		for y in range(len(arr[0])):
			for vec in vectors:
				if read(arr, x, y, vec[0], vec[1], 4) == "XMAS":
					count += 1
	print(count)

main()
