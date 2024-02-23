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
	print('end of main')



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
	# at this point there are no spaces and stars, and we know there is 1 and only 1 equal
	print("yop")
	check_for_common_errors(input_no_space_no_star)
	
	return True


def	check_for_common_errors(equation_string):
	if re.search("[+\-.^][+\-.^]", equation_string) != None: # any 2 of those signs next to each other : [+-.^]
		print("Problem with equation : 2 or more of those signs are next to each other : [+-.^]")
	if re.search("\^(?![0-2])", equation_string) != None: # exponent sign that is not followed by 0 - 1 - 2
		print("Problem with equation : Each exponent sign --> ^ must be followed by one of those numbers [012]")
	if re.search("[+-](?![0-9])", equation_string) != None: # + - with no digit after it
		print("Problem with equation : Each + or - need to be followed by a number.")
	search_result = re.search("[^xX+\-.^=0-9]", equation_string)
	if search_result != None: #any other sign than {xX+-.^=[0-9]}
		print("Problem with equation : Wrong character --> ", search_result[0])


def	fix_input(raw_input):
	# remove space
	# add 1 when there is no coefficient
	# make sure all coefficients have x^y

	input_no_space_no_star = raw_input.replace(' ', '').replace('*', '')
	input_array = input_no_space_no_star.split('=')

	return input_array



if __name__ == "__main__":
	main()