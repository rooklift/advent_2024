import re

def main():
	with open("03_input.txt") as infile:
		s = infile.read()
	print(calculate_result(modify_string(s)))

def modify_string(s):
	enable = True
	dos = find_indices(s, "do()")
	donts = find_indices(s, "don't()")
	newchars = []
	for i, c in enumerate(s):
		if i in dos:
			enable = True
		if i in donts:
			enable = False
		if enable:
			newchars.append(c)
	return "".join(newchars)

def find_indices(s, srch):
	ret = []
	i = -1
	while True:
		try:
			i = s.index(srch, i + 1)
			ret.append(i)
		except:
			return ret

def calculate_result(s):
	foo = re.findall(r"mul\(\d{1,3},\d{1,3}\)", s)
	result = 0
	for item in foo:
		first = int(item.split("(")[1].split(",")[0])
		second = int(item.split(",")[1].split(")")[0])
		result += first * second
	return result

main()
