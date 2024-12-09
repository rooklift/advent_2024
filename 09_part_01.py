def parser(filename):
	with open(filename) as infile:
		data = infile.read().strip()
	return data


def main():
	data = parser("09_input.txt")

	blocks = []

	fid = -1
	empty = True

	for c in data:

		n = int(c)

		empty = not empty
		if not empty:
			fid += 1

		for i in range(n):
			if not empty:
				blocks.append(fid)
			else:
				blocks.append(None)

	blocks = fragment(blocks)
	print(checksum(blocks))


def fragment(blocks):

	blocks = blocks.copy()

	for i in range(len(blocks) - 1, -1, -1):

		fid = blocks[i]

		empty_i = blocks.index(None)

		if empty_i >= i:
			break

		blocks[empty_i] = fid
		blocks[i] = None

	return blocks


def checksum(blocks):
	ret = 0
	for i, item in enumerate(blocks):
		if item == None:
			continue
		ret += i * item
	return ret


main()
