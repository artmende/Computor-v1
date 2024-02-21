#!/usr/bin/python3

import sys
import re

# save both sides of the equation
# sum all coefficient of each power of x, using regex, for both sides of equal
# Display the reduced form
# apply the math formula to get the discriminant, and to get the roots

#coefficient can be followed by * or not
#if no coefficient, it's 1

# 8 * x^2 + 7 * x^1 - 9.4 * X = 8x + 2 - 7x^2 + 3.3*x^0
# x + 7x^2 - 6 = 4 * x^0 + 8 * x^1 - 8.1 + 43*x^2

def	main():
	clean_input_array = args_check_and_treatment(sys.argv) # will exit the program if input is bad

	if check_input_is_correct(sys.argv) == False:
		exit()

	input_with_no_space = sys.argv[1].replace(' ', '')

	clean_input_array = fix_input(sys.argv[1]) # will exit the program if input is bad
	print(clean_input_array)

def	args_check_and_treatment(argv):
	if len(argv) != 2:
		print("We allow strictly 1 argument. It has to be the equation in a single string (Between quotes).")
		print('Usage : ./computor "YOUR QUADRATIC EQUATION"')
		exit()
	if argv[1].count('=') != 1:
		print("Your equation must have one and only one equal sign --> =")
		print('An example of a valid equation is : "x^2 + 4x + 6 = 2x + 8 - 3x^2"')
		exit()
	input_no_space_no_star = argv[1].replace(' ', '').replace('*', '')


def	check_input_is_correct(argv_array):

	# possible errors (after spaces and asterisks are removed and separated by equal) :
	# any 2 of those signs next to each other : [+-.^]
	# + - ^ with no digit after it
	# no equal sign, or more than one -- taken care of
	# exponent more than 2
	# any other sign than {xX+-.^=[0-9]}

	if len(argv_array) != 2:
		print("We allow strictly 1 argument. It has to be the equation in a single string (Between quotes).")
		print('Usage : ./computor "YOUR QUADRATIC EQUATION"')
		return False
	if argv_array[1].__contains__("=") == False:
		print("Your equation must have an equal sign --> =")
		print('An example of a valid equation is : "x^2 + 4x + 6 = 2x + 8 - 3x^2"')
		return False
	return True

def	fix_input(raw_input):
	# remove space
	# add 1 when there is no coefficient
	# make sure all coefficients have x^y

	input_no_space_no_star = raw_input.replace(' ', '').replace('*', '')
	input_array = input_no_space_no_star.split('=')

	return input_array



if __name__ == "__main__":
	main()