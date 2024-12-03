import re

def main():

	with open("03_input.txt") as infile:
		s = infile.read()

	foo = re.findall(r"mul\(\d{1,3},\d{1,3}\)", s)

	result = 0

	for item in foo:
		first = int(item.split("(")[1].split(",")[0])
		second = int(item.split(",")[1].split(")")[0])
		result += first * second

	print(result)


main()

