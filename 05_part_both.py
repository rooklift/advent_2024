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
	return make_rule_dict(rule_lines), make_update_vals(update_lines)

def make_rule_dict(rule_lines):
	rule_dict = dict()
	for line in rule_lines:
		left, right = [int(s) for s in line.split("|")]
		if left in rule_dict:
			rule_dict[left].append(right)
		else:
			rule_dict[left] = [right]
	return rule_dict

def make_update_vals(update_lines):
	ret = []
	for line in update_lines:
		ret.append([int(s) for s in line.split(",")])
	return ret

def update_is_good(rule_dict, vals):
	for i, val in enumerate(vals):
		if val not in rule_dict:
			continue
		for follower in rule_dict[val]:
			if follower in vals[0:i]:
				return False
	return True

def get_fixed_vals(rule_dict, vals):
	ret = []
	fcd = {key: 0 for key in vals}		# Follower count dict - for each value, how many relevant followers does it have?
	for val in vals:
		for v in vals:
			if v in rule_dict[val]:
				fcd[val] += 1
	return sorted(vals, key = lambda x : fcd[x], reverse = True)

def main():
	rule_dict, update_vals = parser("05_input.txt")
	bad_lines = []
	p1_count = 0
	p2_count = 0
	for vals in update_vals:
		if update_is_good(rule_dict, vals):
			p1_count += int(vals[len(vals) // 2])
		else:
			bad_lines.append(vals)
	for vals in bad_lines:
		fixed = get_fixed_vals(rule_dict, vals)
		p2_count += int(fixed[len(fixed) // 2])
	print(p1_count)
	print(p2_count)

main()
