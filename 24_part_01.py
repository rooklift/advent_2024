def parser(filename):
	with open(filename) as infile:
		parts = infile.read().strip().split("\n\n")

	input_dict = dict()

	for line in parts[0].split("\n"):
		key, val = line.split(": ")
		input_dict[key] = True if val == "1" else False

	connections = []

	for line in parts[1].split("\n"):
		tokens = line.split(" ")
		connections.append(Gate(tokens[0], tokens[1], tokens[2], tokens[4]))

	return input_dict, connections



class Gate():
	def __init__(self, in1, op, in2, out):
		self.in1 = in1
		self.in2 = in2
		self.op = op
		self.out = out
		self.handled = False

	def __str__(self):
		return f"{self.in1} {self.op} {self.in2} --> {self.out}"


def handle_gate(in1, in2, op):
	if op == "XOR":
		return (in1 or in2) and not (in1 and in2)
	if op == "AND":
		return in1 and in2
	if op == "OR":
		return in1 or in2
	raise ValueError


def main():
	input_dict, gates = parser("24_input.txt")

	wires = dict()		# e.g. kpf --> True

	for wire in input_dict:
		wires[wire] = input_dict[wire]

	todo = gates[:]

	while True:

		for gate in todo[::-1]:
			if gate.in1 in wires and gate.in2 in wires:
				assert(gate.out not in wires)
				wires[gate.out] = handle_gate(wires[gate.in1], wires[gate.in2], gate.op)
				gate.handled = True

		todo = [gate for gate in todo if not gate.handled]

		if len(todo) == 0:
			break

	z_wire_names = sorted([key for key in wires if key[0] == "z"], reverse = True)

	final_z_vals = []

	for name in z_wire_names:
		final_z_vals.append(wires[name])

	result = 0

	for val in final_z_vals:
		result = result * 2
		result += int(val)

	print(result)


main()