import random

def parser(filename):
	with open(filename) as infile:
		lines = [line.strip() for line in infile.readlines() if line.strip() != ""]
	return [tuple(line.split("-")) for line in lines]

def main():
	pairs = parser("23_input.txt")
	graph = dict()					# token --> set of connections
	for a, b in pairs:
		if a not in graph:
			graph[a] = set()
		if b not in graph:
			graph[b] = set()
		graph[a].add(b)
		graph[b].add(a)
	solve_both(graph)

def solve_both(graph):

	# This is a simple algorithm based on finding all cliques (whether maximal or not)
	# at size n and then building up for n+1 etc etc. See the part2() function for better.

	cliques = [None, set(), set(), set(), set(), set(), set(), set(), set(), set(), set(), set(), set(), set()]

	cliques[1] = {(c,) for c in graph.keys()}		# Set of len-1 cliques as tuples like ("ab",)

	for size in range(2, 14):
		smaller_cliques = cliques[size - 1]
		for cliq in smaller_cliques:				# Each cliq will be a tuple like ("ab", "si", "zd")
			first_member_connections = graph[cliq[0]]
			for c in first_member_connections:
				if c <= cliq[-1]:					# Only form new cliques alphabetically sorted
					continue
				if c in cliq:
					assert(False)
				ok = True
				for friend in cliq[1:]:
					if c not in graph[friend]:
						ok = False
						break
				if ok:
					new_cliq = cliq + (c,)
					cliques[size].add(new_cliq)

	p1 = 0
	for a, b, c in cliques[3]:
		if a[0] == "t" or b[0] == "t" or c[0] == "t":
			p1 += 1

	p2 = ",".join(list(cliques[13])[0])

	print("Part 1:", p1)
	print("Part 2:", p2)


main()

# -------------------------------------------------------------------------------------------------
# This code is unused now since I finally found a way to do it without using
# algorithms I didn't know and had to ask Claude about...

def part2(graph):

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
	p2_recurse(graph, all_maximal_cliques, set(), set(graph.keys()), set())

	largest = max(all_maximal_cliques, key = len)
	return ",".join(sorted(list(largest)))

def p2_recurse(graph, all_maximal_cliques, clique, prospective, excluded):

	# graph is needed for edge lookup - dict of name --> set of connections.
	# all_maximal_cliques is our globally available storage for maximal (not largest) cliques.
	# The other 3 things are just sets that store only node names.

	if len(prospective) == 0 and len(excluded) == 0:
		all_maximal_cliques.add(tuple(clique))
		return

	pivot = random.choice(list(prospective | excluded))		# Good enough.

	for v in list(prospective):
		if v not in graph[pivot]:
			clique.add(v)
			prospective_prime = set()
			excluded_prime = set()
			for foo in graph[v]:
				if foo in prospective:
					prospective_prime.add(foo)
				if foo in excluded:
					excluded_prime.add(foo)
			p2_recurse(graph, all_maximal_cliques, clique, prospective_prime, excluded_prime)
			clique.remove(v)
			prospective.remove(v)
			excluded.add(v)
