#!/usr/bin/python3

import sys
import re

# save both sides of the equation
# sum all coefficient of each power of x, using regex, for both sides of equal
# Display the reduced form
# apply the math formula to get the discriminant, and to get the roots

#coefficient can be followed by * or not
#if no coefficient, it's 1

def	main():
	if len(sys.argv) != 2:
		print("We allow strictly 1 argument. It has to be the equation in a single string (Between quotes).")
		print('Usage : ./computor "YOUR QUADRATIC EQUATION"')
		exit()
	if sys.argv[1].__contains__("=") == False:
		print("Your equation must have an equal sign --> =")
		print('An example of a valid equation is : "x^2 + 4x + 6 = 2x + 8 - 3x^2"')
		exit()

	input_with_no_space = sys.argv[1].replace(' ', '')

	clean_input = fix_input(sys.argv[1])


def	fix_input(raw_input):
	# remove space
	# add 1 when there is no coefficient
	# make sure all coefficients have x^y
	pass



if __name__ == "__main__":
	main()