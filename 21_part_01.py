def parser(filename):
	with open(filename) as infile:
		return [line.strip() for line in infile.readlines() if line.strip() != ""]

big_lines = [		# Note that these arrays have [y][x] format - but we convert them in make_keypad_grid()
	"789",
	"456",
	"123",
	".0A",
]

small_lines = [
	".^A",
	"<v>",
]


def make_keypad_dict(lines):			# Locations of everything
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


def next_position(kp_dict, c, move):		# Given our position at c and a movement, what char are we at next?

	assert(move in "><^v")

	x, y = kp_dict[c]

	x += vectors[move][0]
	y += vectors[move][1]

	for key in kp_dict:
		if kp_dict[key] == (x, y):
			return key

	raise AssertionError


def next_moves(kp_dict, c1, c2):		# Given our position at c1, return all sane next moves if we want to push c2

	assert(c1 != c2)

	x1, y1 = kp_dict[c1]
	x2, y2 = kp_dict[c2]

	dx = x2 - x1
	dy = y2 - y1

	ret = []
	poss = []

	if dx > 0:
		poss.append(">")
	if dx < 0:
		poss.append("<")
	if dy > 0:
		poss.append("v")
	if dy < 0:
		poss.append("^")

	for move in poss:
		next_c = next_position(kp_dict, c1, move)
		if next_c != ".":
			ret.append(move)

	return ret


def action_sequences(kp_dict, c1, c2):		# Given our position at c1, return all sane sequences to go to c2, AND PUSH IT.

	if c1 == c2:
		return [["A"]]

	all_next = next_moves(kp_dict, c1, c2)

	ret = []

	for move in all_next:
		next_c = next_position(kp_dict, c1, move)

		for foo in action_sequences(kp_dict, next_c, c2):
			ret.append([move] + foo)

	return ret


def full_sequences(kp_dict, c1, buttons):		# Given buttons, with arm at c1, return all sane sequences to press them.

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


def main():

	codes = parser("21_input.txt")

	big = make_keypad_dict(big_lines)
	small = make_keypad_dict(small_lines)

	for foo in full_sequences(big, "A", "029A"):
		print("".join(foo))



main()
