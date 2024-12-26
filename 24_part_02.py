# Here we really consider the names in the input as specifying the names of
# gates rather than wires as it says (my way makes more sense to me).
#
# A gate has 2 inputs (aside from the input gates which are just always
# outputting 0 or 1. The output of a gate can be used by multiple other
# gates.
#
# We are thus trying to swap the positions of 4 pairs of gates.
# This means just swapping their names (as interpreted above).

def parser(filename):
	with open(filename) as infile:
		parts = infile.read().strip().split("\n\n")
	inputs = dict()
	for line in parts[0].split("\n"):
		key, val = line.split(": ")
		inputs[key] = True if val == "1" else False
	connections = []
	for line in parts[1].split("\n"):
		tokens = line.split(" ")
		connections.append(Gate(tokens[0], tokens[1], tokens[2], tokens[4]))
	return inputs, connections

class Gate():
	def __init__(self, in1, op, in2, name):
		self.in1 = in1
		self.op = op
		self.in2 = in2
		self.name = name

	def __str__(self):
		return f"{self.in1} {self.op} {self.in2} -> {self.name}"

	def copy(self):
		return Gate(self.in1, self.op, self.in2, self.name)

def logic(in1, in2, op):
	if op == "XOR":
		return (in1 or in2) and not (in1 and in2)
	if op == "AND":
		return in1 and in2
	if op == "OR":
		return in1 or in2
	raise ValueError

def known_gates_to_digit(known, prefix):
	result = 0
	wire_names = sorted([key for key in known if key.startswith(prefix)])
	for key in wire_names[::-1]:
		result *= 2
		result += 1 if known[key] == True else 0
	return result

def digit_to_inputs(val, prefix, bits):
	ret = dict()
	s = "{0:0{1}b}".format(val, bits)
	for i, c in enumerate(s[::-1]):
		assert(c == "0" or c == "1")
		input_name = "{}{:02}".format(prefix, i)
		ret[input_name] = True if c == "1" else False
	return ret

def simulate(x, y, gates):
	outputs = dict()
	outputs |= digit_to_inputs(x, "x", 45)
	outputs |= digit_to_inputs(y, "y", 45)
	todo = gates[:]
	while True:
		did_something = False
		for gate in todo:
			if gate.in1 in outputs and gate.in2 in outputs:
				outputs[gate.name] = logic(outputs[gate.in1], outputs[gate.in2], gate.op)
				did_something = True
		if not did_something:
			raise ValueError
		todo = [gate for gate in todo if gate.name not in outputs]
		if len(todo) == 0:
			break
	return known_gates_to_digit(outputs, "z")

def test_swaps(x, y, swaps, gates_original):
	gates = [gate.copy() for gate in gates_original]
	for swap in swaps:
		fixme = []
		for gate in gates:
			if gate.name in swap:
				fixme.append(gate)
		assert(len(fixme) == 2)
		fixme[0].name, fixme[1].name = fixme[1].name, fixme[0].name
	return simulate(x, y, gates)

# -------------------------------------------------------------------------------------------------

def main():
	inputs, gates = parser("24_input.txt")

	# We rewrote the simulator to take actual int values for x and y, then infer the wires.
	# (For Part 1 we are given the wires, but for Part 2 need to be able to use arbitrary x and y.)

	print("PART ONE:")
	x = known_gates_to_digit(inputs, "x")
	y = known_gates_to_digit(inputs, "y")
	z_actual = simulate(x, y, gates)
	print(f"x = {x}")
	print(f"y = {y}")
	print(f"z = {x + y} (expected)")
	print(f"z = {z_actual} (actual, diff = {(x + y) - z_actual}")

	# Some swaps determined by visualising the circuit...
	# Print all possibilities which work...

	print("PART TWO:")

	all_intermediate_names = []

	for gate in gates:
		if gate.name.startswith("z"):
			continue
		all_intermediate_names.append(gate.name)

	for i, name in enumerate(all_intermediate_names):
		for other in all_intermediate_names[i + 1:]:

			swaps = []
			swaps.append(("gpr", "z10"))		# 100% certain
			swaps.append(("z21", "nks"))		# 100% certain
			swaps.append(("z33", "ghp"))		# Pretty certain
			swaps.append((name, other))

			try:
				z_actual = test_swaps(x, y, swaps, gates)
				if z_actual == x + y:
					print(swaps)
			except ValueError:
				pass

main()
