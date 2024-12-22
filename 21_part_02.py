# OK, basic idea:
#
# For each level, have an object storing:
# - The sequences that need to be pressed by the robot below.
#
# e.g. to move to push   0: <A
#                        2: ^A
#                        9: ^^>A
#                        A: vvvA
#
# Since each of those sequences below ends in A, the order of
# those sequences doesn't matter, so store a dict of:
#
# - sequence --> count of them
#
# e.g. {
#         "<A"   : 1,
#         "^A"   : 1,
#         "^^>A" : 1,
#         "vvvA" : 1,
# }
#
# There's some subtleties since one sequence can be better than another.
#
# But then it should be easy to cache what the best way to generate each
# of the possible sequences is.
#
# --------------------- UPDATE -----------------------------------------
#
# So this works for 2 intermediate robots (part 1) but not 25 (part 2).

import functools

vectors = {
	">":    (1, 0),
	"<":    (-1, 0),
	"^":    (0, -1),
	"v":    (0, 1),
}

big_lines = [       # These arrays have [y][x] format - convert them in make_keypad_grid()
	"789",
	"456",
	"123",
	".0A",
]

small_lines = [
	".^A",
	"<v>",
]

def make_keypad_dict(lines):                                # Dict: c --> (x, y)
	ret = dict()
	for y, line in enumerate(lines):
		for x, c in enumerate(line):
			ret[c] = (x, y)
	return ret

big_kp_dict = make_keypad_dict(big_lines)
small_kp_dict = make_keypad_dict(small_lines)

# -------------------------------------------------------------------------------------------------

def parser(filename):
	with open(filename) as infile:
		return [line.strip() for line in infile.readlines() if line.strip() != ""]

def main():
	input_filename = "21_paulson.txt"						# p1: 224326 , p2: 279638326609472
	codes = parser(input_filename)
	p1 = 0
	p2 = 0
	for code in codes:
		p1 += solve(code, 2)
		p2 += solve(code, 25)
	print(p1)
	print(p2)
	print(f"Input file was: {input_filename}")

def solve(code, intermediate_robot_count):

	top_level_possibles = full_sequences(True, code)        # ['<^^^A<A>>AvvvA', '^^^<A<A>>AvvvA']

	possible_dicts = []

	for poss in top_level_possibles:
		possible_dicts.append(count_components(poss))

	best = None

	for d in possible_dicts:
		for n in range(intermediate_robot_count):
			d = next_level_dict(d)
		if best == None or dict_direct_score(d) < best:
			best = dict_direct_score(d)

	return best * int(code[0:3])


def count_components(seq):								# "<^^^A<A>>AvvvA" --> {"<^^^A": 1, "<A": 1, ">>A": 1, "vvvA": 1}
	ret = []
	tokens = [s + "A" for s in seq.split("A")]
	tokens = tokens[:-1]                                # The very last one is spurious with this comprehension
	tokens_set = set(tokens)
	return {token: tokens.count(token) for token in tokens_set}


# -------------------------------------------------------------------------------------------------

def dict_direct_score(d):
	score = 0
	for token in d:
		score += len(token) * d[token]
	return score


def dict_maker_score(d):
	score = 0
	for token in d:
		score += len(best_maker(token)) * d[token]
	return score


def next_level_dict(d):
	next_d = dict()
	for token in d:
		full_seq = best_maker(token)
		foo = count_components(full_seq)
		for t2 in foo:
			if t2 in next_d:
				next_d[t2] += foo[t2] * d[token]
			else:
				next_d[t2] = foo[t2] * d[token]
	return next_d


@functools.cache
def best_maker(buttons):			# Some string like "v<<A" --> something longer that will likely contain multiple A

	possible_makers = full_sequences(False, buttons)

	best_maker = None
	best_score = None

	for maker in possible_makers:

		possible_maker_makers = full_sequences(False, maker)

		if best_maker == None or len(possible_maker_makers[0]) < best_score:
			best_maker = maker
			best_score = len(possible_maker_makers[0])

	return best_maker

# -------------------------------------------------------------------------------------------------

def only_smallest(arr):
	smallest = None
	for item in arr:
		if smallest == None or len(item) < smallest:
			smallest = len(item)
	return [item for item in arr if len(item) == smallest]

# -------------------------------------------------------------------------------------------------

def full_sequences(use_big, buttons):
	assert(use_big in [True, False])
	kp_dict = big_kp_dict if use_big else small_kp_dict
	curr_c = "A"
	next_c = buttons[0]
	ret = action_sequences(kp_dict, curr_c, next_c)
	for button in buttons[1:]:
		curr_c = next_c
		next_c = button
		additional = action_sequences(kp_dict, curr_c, next_c)
		new_ret = []
		for add in additional:
			for partial in ret:
				new_ret.append(partial + add)
		ret = new_ret
	return only_smallest(ret)


def action_sequences(kp_dict, c1, c2, last_move = None):    # Given our position at c1, return all sane sequences to go to c2, AND PUSH IT.
	if c1 == c2:
		return ["A"]
	all_next = next_moves(kp_dict, c1, c2)
	if last_move in all_next:
		all_next = [last_move]
	ret = []
	for move in all_next:
		next_c = next_position(kp_dict, c1, move)
		for foo in action_sequences(kp_dict, next_c, c2, move):
			ret.append(move + foo)
	return only_smallest(ret)


def next_moves(kp_dict, c1, c2):                            # Given our position at c1, return 1 or 2 possible next moves if we want to push c2.
	assert(c1 != c2)
	x1, y1 = kp_dict[c1]
	x2, y2 = kp_dict[c2]
	ret = []
	poss = []
	if x1 < x2:
		poss.append(">")
	if x2 < x1:
		poss.append("<")
	if y1 < y2:
		poss.append("v")
	if y2 < y1:
		poss.append("^")
	for move in poss:
		next_c = next_position(kp_dict, c1, move)
		if next_c == ".":
			continue
		# Hard code avoiding some stupid moves:
		if c1 in ["7", "4"] and c2 in ["0", "A"] and move == "v":
			continue
		if c1 == "A" and c2 in ["7", "4", "1"] and move == "<":
			continue
		if c1 == "A" and c2 == "<" and move == "<":
			continue
		ret.append(move)

	return ret


def next_position(kp_dict, c, move):
	assert(move in "<>^v")
	x, y = kp_dict[c]
	dx, dy = vectors[move]
	x += dx
	y += dy
	for key in kp_dict:
		if kp_dict[key] == (x, y):
			return key
	raise AssertionError

# -------------------------------------------------------------------------------------------------

main()
