import random

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
	print(part2(nodes))

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

def part2(nodes):

	"""
	WHAT CLAUDE SAYS ONE NEEDS TO DO TO MAKE ... Bron-Kerbosch Largest Clique Algorithm:

	The algorithm maintains three sets of vertices:

		R - the current growing clique being built
		P - prospective vertices that could expand the current clique
		X - excluded vertices that have already been processed

	The core idea is to recursively grow cliques while being smart about which vertices to consider or exclude. Here's how it works:
	Starting with R empty, P containing all vertices, and X empty:

	If both P and X are empty, R is a maximal clique - save it to a globally available set
	Otherwise, choose a pivot vertex u from P ∪ X
	For each vertex v in P that's not connected to u:

		Add v to R (growing the clique)
		Create new P' with only v's neighbors that were in P
		Create new X' with only v's neighbors that were in X
		Recurse with these new sets
		After recursion, move v from P to X

	MY NOTES:

	A maximal clique is one that cannot grown any larger, but not necessarily the largest clique in the graph.
	So we need to look through our cliques and choose the correct one.

	"""

	all_maximal_cliques = set()
	p2_recurse(nodes, all_maximal_cliques, set(), set(nodes.keys()), set())

	largest = max(all_maximal_cliques, key = len)
	return ",".join(sorted(list(largest)))

def p2_recurse(nodes, all_maximal_cliques, clique, prospective, excluded):

	# nodes is needed for edge lookup (the last 3 items are all sets that only store a name).
	# Return value: are we done modifying clique?

	if len(prospective) == 0 and len(excluded) == 0:
		all_maximal_cliques.add(tuple(clique))
		return

	pivot = random.choice(list(prospective | excluded))		# Good enough.

	for v in list(prospective):
		if v not in nodes[pivot]:
			clique.add(v)
			prospective_prime = set()
			excluded_prime = set()
			for foo in nodes[v]:
				if foo in prospective:
					prospective_prime.add(foo)
				if foo in excluded:
					excluded_prime.add(foo)
			p2_recurse(nodes, all_maximal_cliques, clique, prospective_prime, excluded_prime)
			clique.remove(v)
			prospective.remove(v)
			excluded.add(v)

main()
