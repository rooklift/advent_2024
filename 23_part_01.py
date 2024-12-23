def parser(filename):
	with open(filename) as infile:
		lines = [line.strip() for line in infile.readlines() if line.strip() != ""]
	return [tuple(line.split("-")) for line in lines]

def main():
	pairs = parser("23_input.txt")
	nodes = dict()					# token --> set of connections

	for a, b in pairs:
		if a not in nodes:
			nodes[a] = set()
		if b not in nodes:
			nodes[b] = set()
		nodes[a].add(b)
		nodes[b].add(a)

	print(part1(nodes))

def part1(nodes):
	all_triples = set()
	for a in nodes:
		for b in nodes[a]:			# So a-b definitely exists
			for c in nodes[b]:		# So b-c definitely exists
				if c in nodes[a]:
					all_triples.add(tuple(sorted([a, b, c])))		# Sort to deduplicate

	p1 = 0
	for a, b, c in all_triples:
		if a[0] == "t" or b[0] == "t" or c[0] == "t":
			p1 += 1

	return p1

main()
