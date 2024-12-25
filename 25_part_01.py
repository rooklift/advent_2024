# I decided to do this the cutest possible way, by turning keys and
# locks into binary numbers, which can be checked for overlap with &

def parser(filename):
	with open(filename) as infile:
		schema = [item.strip() for item in infile.read().split("\n\n")]
	items = []
	for item in schema:
		items.append(parse_item(item))
	return items

def parse_item(item):
	lines = item.split("\n")
	s = "0b"
	for line in lines:
		for c in line:
			if c == ".":
				s += "0"
			elif c == "#":
				s += "1"
			else:
				raise ValueError
	return int(s, 2)

def main():
	items = parser("25_input.txt")
	result = 0
	for i, item in enumerate(items):
		for j, other in enumerate(items[i + 1:]):
			if not (item & other):
				result += 1
	print(result)

main()
