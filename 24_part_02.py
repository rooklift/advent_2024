def parser(filename):
	with open(filename) as infile:
		parts = infile.read().strip().split("\n\n")
	initial_wires = dict()
	for line in parts[0].split("\n"):
		key, val = line.split(": ")
		initial_wires[key] = True if val == "1" else False
	connections = []
	for line in parts[1].split("\n"):
		tokens = line.split(" ")
		connections.append(Gate(tokens[0], tokens[1], tokens[2], tokens[4]))
	return initial_wires, connections

class Gate():
	def __init__(self, in1, op, in2, out):
		self.in1 = in1
		self.in2 = in2
		self.op = op
		self.out = out

	def __str__(self):
		return f"{self.in1} {self.op} {self.in2} -> {self.out}"

def logic(in1, in2, op):
	if op == "XOR":
		return (in1 or in2) and not (in1 and in2)
	if op == "AND":
		return in1 and in2
	if op == "OR":
		return in1 or in2
	raise ValueError

def wires_to_digit(all_wires, prefix):
	result = 0
	wire_names = sorted([key for key in all_wires if key.startswith(prefix)])
	for key in wire_names[::-1]:
		result *= 2
		result += 1 if all_wires[key] == True else 0
	return result

def digit_to_wires(val, prefix, bits):
	ret = dict()
	s = "{0:0{1}b}".format(val, bits)
	for i, c in enumerate(s[::-1]):
		assert(c == "0" or c == "1")
		wire_name = "{}{:02}".format(prefix, i)
		ret[wire_name] = True if c == "1" else False
	return ret

def simulate(x, y, gates):
	wires = dict()
	wires |= digit_to_wires(x, "x", 45)
	wires |= digit_to_wires(y, "y", 45)
	todo = gates[:]
	while True:
		for gate in todo:
			if gate.in1 in wires and gate.in2 in wires:
				wires[gate.out] = logic(wires[gate.in1], wires[gate.in2], gate.op)
		todo = [gate for gate in todo if gate.out not in wires]
		if len(todo) == 0:
			break
	return wires_to_digit(wires, "z")

# -------------------------------------------------------------------------------------------------

def main():
	wires, gates = parser("24_input.txt")

	# We rewrote the simulator to take actual int values for x and y, then infer the wires.
	# (For Part 1 we are given the wires, but for Part 2 need to be able to use arbitrary x and y.)

	print("PART ONE:")
	x = wires_to_digit(wires, "x")
	y = wires_to_digit(wires, "y")
	z_actual = simulate(x, y, gates)
	print(f"x = {x}")
	print(f"y = {y}")
	print(f"z = {x + y} (expected)")
	print(f"z = {z_actual} (actual, diff = {(x + y) - z_actual}")

	# So there's probably some way to find the defective wires...


main()
