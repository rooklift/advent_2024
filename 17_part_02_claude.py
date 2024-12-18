# Only AFTER I'd solved part 2, I discussed it with Claude and got it to write the following
# fast algorithm when I realised the basic correct strategy rather than the crude hack I used.
#
# Snippets of the prompt (after discussing the puzzle extensively...)

"""
    I considered lower values of A, starting at 1 and going upwards.

    1-7: gives a 1 digit output
    8-63: 2 digit output
    4-511: 3 digit output

    etc etc, growing like this

    But I noticed that the ends of each output were predictable from the outputs of the shorter
    sequences.

    Example: the first 1-7 outputs predict the final outputs of the outputs 8-63 in the following
    way: outputs 8-15 end with the final digit of output 1, outputs 16-23 end with the final digit
    of output 2, and so on.

    But this continues for larger sequences. For example, outputs 64-71 are 3 digits long, and the
    final 2 digits of each of them is the final 2 digits of output 8.

    Seeing this pattern, I simply looked at all the outputs of length 6, found that the ending we
    desired (5,5,0,3,3,0) was found at about 52.41% of the way through, and then it was simple to
    just do a brute force of the full length inputs starting at about the correct location.

    Knowing that this pattern exists, there should be some fast algorithm to solve this:

    * Generate the numbers for input 1-7:
    * Find what input or inputs give the right final digit
    * Now search only the correct part(s) of inputs 8-63 for the input or inputs that give the right
      final 2 digits.
    * Now search only the correct part(s) of inputs 64-511...

    etc etc
"""

# And amazingly, this was more or less enough to get it to generate the following.
# (With a bit of extra help...)

class Computer:
    def __init__(self, initial_a=0):
        self.reset(initial_a)

    def reset(self, initial_a):
        self.a = initial_a
        self.b = 0
        self.c = 0
        self.i = 0
        self.outputs = []

    def interpret_combo(self, n):
        if n <= 3:
            return n
        if n == 4:
            return self.a
        if n == 5:
            return self.b
        if n == 6:
            return self.c
        raise ValueError("Invalid combo operand")

    def act(self, opcode, value):
        next_i = self.i + 2

        if opcode == 0:      # adv
            self.a = self.a // (2 ** self.interpret_combo(value))
        elif opcode == 1:    # bxl
            self.b = self.b ^ value
        elif opcode == 2:    # bst
            self.b = self.interpret_combo(value) % 8
        elif opcode == 3:    # jnz
            if self.a != 0:
                next_i = value
        elif opcode == 4:    # bxc
            self.b = self.b ^ self.c
        elif opcode == 5:    # out
            self.outputs.append(self.interpret_combo(value) % 8)
        elif opcode == 6:    # bdv
            self.b = self.a // (2 ** self.interpret_combo(value))
        elif opcode == 7:    # cdv
            self.c = self.a // (2 ** self.interpret_combo(value))

        self.i = next_i

    def run_program(self, program):
        self.i = 0
        self.outputs = []
        while self.i < len(program) - 1:
            self.act(program[self.i], program[self.i + 1])
        return self.outputs

def find_matching_sequences(start, end, target_suffix, program):
    """Find all inputs in range that produce output sequences ending with target_suffix"""
    computer = Computer()
    matching = []
    for a in range(start, end + 1):
        computer.reset(a)
        outputs = computer.run_program(program)
        if len(outputs) >= len(target_suffix) and outputs[-len(target_suffix):] == target_suffix:
            matching.append(a)
    return matching

def solve_program(program):
    """Build up solution by finding matching sequences of increasing length"""
    target = program

    length = 1
    candidates = find_matching_sequences(1, 7, target[-1:], program)
    print(f"Length {length}: {len(candidates)} candidates ending in {target[-1:]}")

    while length < len(target):
        length += 1
        new_candidates = []

        for prev in candidates:
            start = prev << 3
            end = start + 7
            matches = find_matching_sequences(start, end, target[-length:], program)
            new_candidates.extend(matches)

        candidates = new_candidates
        print(f"Length {length}: {len(candidates)} candidates ending in {target[-length:]}")

        if not candidates:
            return None

    return candidates[0] if candidates else None

# Test with the small program
small_program = [0,3,5,4,3,0]
print("\nTesting small program:", small_program)
result = solve_program(small_program)
print(f"Solution: {result}")

if result:
    computer = Computer(result)
    print(f"Verification: {computer.run_program(small_program) == small_program}")

# Verify known solution
known = 117440
computer = Computer(known)
outputs = computer.run_program(small_program)
print(f"\nKnown solution {known} produces: {outputs}")
print(f"Expected: {small_program}")

# Test with the original large program
large_program = [2,4,1,1,7,5,1,5,4,2,5,5,0,3,3,0]
print("\nTesting large program:", large_program)
result = solve_program(large_program)
print(f"Solution: {result}")

if result:
    computer = Computer(result)
    print(f"Verification: {computer.run_program(large_program) == large_program}")