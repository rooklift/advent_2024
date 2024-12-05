def parser(filename):
	with open(filename) as infile:
		lines = [line.strip() for line in infile.readlines() if line.strip() != ""]
	rule_lines = []
	update_lines = []
	for line in lines:
		if "|" in line:
			rule_lines.append(line)
		if "," in line:
			update_lines.append(line)
	return rule_lines, update_lines

def main():
	rule_lines, update_lines = parser("05_input.txt")
	rule_dict = dict()
	for line in rule_lines:
		left, right = [int(s) for s in line.split("|")]
		if left in rule_dict:
			rule_dict[left].append(right)
		else:
			rule_dict[left] = [right]
	result = 0
	for line in update_lines:
		vals = [int(s) for s in line.split(",")]
		ok = True
		for i, val in enumerate(vals):
			if not ok:
				break
			if val not in rule_dict:
				continue
			for follower in rule_dict[val]:
				if follower in vals[0:i]:
					ok = False
					break
		if ok:
			result += vals[len(vals) // 2]
	print(result)

main()
