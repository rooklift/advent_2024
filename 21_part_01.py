def parser(filename):
	with open(filename) as infile:
		return [line.strip() for line in infile.readlines() if line.strip() != ""]

big_lines = [												# These arrays have [y][x] format - convert them in make_keypad_grid()
	"789",
	"456",
	"123",
	".0A",
]

small_lines = [
	".^A",
	"<v>",
]


def make_keypad_dict(lines):								# Dict: c --> (x, y)
	ret = dict()
	for y, line in enumerate(lines):
		for x, c in enumerate(line):
			ret[c] = (x, y)
	return ret


vectors = {
	">":	(1, 0),
	"<":	(-1, 0),
	"^":	(0, -1),
	"v":	(0, 1),
}


def next_position(kp_dict, c, move):						# Given our position at c and a movement in "<>^v", what char are we at next?
	assert(move in "<>^v")
	x, y = kp_dict[c]
	dx, dy = vectors[move]
	x += dx
	y += dy
	for key in kp_dict:
		if kp_dict[key] == (x, y):
			return key
	raise AssertionError


def next_moves(kp_dict, c1, c2):							# Given our position at c1, return 1 or 2 possible next moves if we want to push c2.
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
		# if c1 in ["7", "4"] and c2 in ["0", "A"] and move == "v":			# (Our actual input doesn't contain these cases.)
		#	continue
		if c1 == "A" and c2 in ["7", "4", "1"] and move == "<":
			continue
		if c1 == "A" and c2 == "<" and move == "<":
			continue
		ret.append(move)

	return ret


def action_sequences(kp_dict, c1, c2, last_move = None):	# Given our position at c1, return all sane sequences to go to c2, AND PUSH IT.
	if c1 == c2:
		return [["A"]]
	all_next = next_moves(kp_dict, c1, c2)
	if last_move in all_next:
		all_next = [last_move]
	ret = []
	for move in all_next:
		next_c = next_position(kp_dict, c1, move)
		for foo in action_sequences(kp_dict, next_c, c2, move):
			ret.append([move] + foo)
	return ret


def full_sequences(kp_dict, c1, buttons):					# Given buttons, with arm at c1, return all sane sequences to press them.
	curr_c = c1
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
	return ret


def score(s, push_count):									# Score for code s given how many buttons the human presses.
	return int(s[0:3]) * push_count


def solve_code(big_kp_dict, small_kp_dict, code, intermediate_robots):
	result = 0
	seqs = full_sequences(big_kp_dict, "A", code)
	for n in range(intermediate_robots):
		next_level = []
		for seq in seqs:
			next_level += full_sequences(small_kp_dict, "A", seq)
		seqs = next_level
	min_buttons = None
	for seq in seqs:
		if min_buttons == None or len(seq) < min_buttons:
			min_buttons = len(seq)
	return score(code, min_buttons)


def main():
	codes = parser("21_input.txt")
	big_kp_dict = make_keypad_dict(big_lines)
	small_kp_dict = make_keypad_dict(small_lines)
	result = 0
	for code in codes:
		print(code)
		result += solve_code(big_kp_dict, small_kp_dict, code, 2)
	print(result)


# I suspect the secret of Part 2 involves some combination of caching
# and exploiting the fact that the robots are ending at A whenever
# they are causing the robot above them to push any button.


main()
