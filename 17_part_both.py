def parser(filename):
	with open(filename) as infile:
		parts = infile.read().split("\n\n")
	regs = parts[0].split("\n")
	a = int(regs[0].split("A:")[1])
	b = int(regs[1].split("B:")[1])
	c = int(regs[2].split("C:")[1])
	program = [int(s) for s in parts[1].split(":")[1].split(",")]
	return a, b, c, program


class Halt(Exception):
    pass


class Computer():

	def __init__(self, a, b, c, program):
		self.reset(a, b, c, program)


	def reset(self, a, b, c, program):
		self.reset_fast(a, b, c)
		self.program = program
		self.program_string = ",".join([str(n) for n in program])


	def reset_fast(self, a, b, c):			# Since program doesn't change.
		self.a = a
		self.b = b
		self.c = c
		self.i = 0
		self.outputs = []


	def get_output(self):
		while True:
			try:
				self.step()
			except Halt:
				return self.outputs


	def get_output_string(self):
		return ",".join([str(n) for n in self.get_output()])


	def step(self):
		if self.i >= len(self.program):
			raise Halt
		self.act(self.program[self.i], self.program[self.i + 1])


	def act(self, opcode, value):			# Where value is the raw number at i+1

		# Note: operands may be either literals or combos, depending on the opcode.

		next_i = self.i + 2					# usually true

		if opcode == 0:						# adv (division using combo, save to A)
			self.a = self.a // (2 ** self.interpret_combo(value))
		elif opcode == 1:					# bxl (bitwise xor using literal, save to B)
			self.b = self.b ^ value
		elif opcode == 2:					# bst (combo modulo 8, save to B)
			self.b = self.interpret_combo(value) % 8
		elif opcode == 3:					# jnz (conditional jump using literal)
			if self.a == 0:
				pass
			else:
				next_i = value
		elif opcode == 4:					# bxc (bitwise xor of a^b, save to B)
			self.b = self.b ^ self.c
		elif opcode == 5:					# out (output combo modulo 8)
			self.outputs.append(self.interpret_combo(value) % 8)
		elif opcode == 6:					# bdv (like adv but save to B)
			self.b = self.a // (2 ** self.interpret_combo(value))
		elif opcode == 7:					# cdv (like adv but save to C)
			self.c = self.a // (2 ** self.interpret_combo(value))

		self.i = next_i


	def interpret_combo(self, n):
		if n <= 3:
			return n
		if n == 4:
			return self.a
		if n == 5:
			return self.b
		if n == 6:
			return self.c
		if n == 7:
			raise ValueError


def dfs(start, end, computer):
	candidates = []
	for n in range(start, end + 1):
		computer.reset_fast(n, 0, 0)
		output = computer.get_output()
		if output == computer.program:
			return n
		if output == computer.program[-len(output):]:
			candidates.append(n)
	for n in candidates:
		ret = dfs(n * 8, n * 8 + 7, computer)
		if ret != None:
			return ret


def main():
	computer = Computer(*parser("17_input.txt"))
	print(computer.get_output_string())
	print(dfs(1, 7, computer))


main()
