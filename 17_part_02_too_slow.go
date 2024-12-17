package main

import "fmt"
import "strconv"

/*
		Program: 2,4,1,1,7,5,1,5,4,2,5,5,0,3,3,0

		2,4		B = A & 7				// Chop off all but 3 bits of A (but saving in B)
		1,1		B = B ^ 1				// Flip smallest bit
		7,5		C = A / (2 ** B)
		1,5     B = B ^ 5				// Flip 1st and 3rd bits (from right)
		4,2		B = B ^ C
		5,5		output B & 7			// Output final 3 bits of B
		0,3		A = A / 8
		3,0		terminate if A == 0
*/

// PART 1

func full_output(a uint64) string {

	var b uint64
	var c uint64

	s := ""

	for {
		b = a & 7
		b = b ^ 1
		c = a / (1 << b)
		b = b ^ 5
		b = b ^ c
		if len(s) > 0 {
			s += ","
		}
		s += strconv.Itoa(int(b & 7))
		a = a >> 3
		if a == 0 {
			return s
		}
	}
}

// PART 2

var desired_output = [16]uint64{2,4,1,1,7,5,1,5,4,2,5,5,0,3,3,0}

func check(a uint64) bool {		// should be 16 digits in octal

	var b uint64
	var c uint64

	for i := 0; i < 16; i++ {
		b = a & 7
		b = b ^ 1
		c = a / (1 << b)
		b = b ^ 5
		b = b ^ c
		if b & 7 != desired_output[i] {
			return false
		}
		a = a >> 3
	}

	return true
}


func main() {

	var n uint64

	fmt.Printf("PART 1: %s\n", full_output(28422061))				// Part 1

	for n = 0o1000000000000000; n <= 0o7777777777777777; n++ {		// Part 2 - would take some weeks...
		if check(n) {
			fmt.Printf("-------------------")
			fmt.Printf("\n%d\n", n)
			break
		}
		if n % 1000000000 == 0 {
			fmt.Printf("%O...\n", n)
		}
	}
}

