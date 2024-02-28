#!/usr/bin/python3

# All regex formulas here were crafted with the help of https://regexr.com/.
# Please visit the website for formulas explanation

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
	print(clean_input_array)
	reduced_coeff_array = calculate_coefficients_of_reduced_equation(clean_input_array)
	display_reduced_equation(reduced_coeff_array)
	delta = calculate_delta(reduced_coeff_array)
	solutions = calculate_solutions(reduced_coeff_array, delta)
	if solutions == None:
		print("Any number is a solution.")
		return
	elif reduced_coeff_array[2] == 0:
		print("That is a linear equation. There is only one solution.")
		print("x = ", solutions[0])
	elif solutions[0] == solutions[1]:
		print("For this equation, Delta is zero. We have a double root.")
		print("x_1 = x_2 = ", solutions[0])
	else:
		print("Delta = ", delta)
		print("x_1 = ", solutions[0])
		print("x_2 = ", solutions[1])
	# TO DO : Calculate Delta
	# Depending of the value of Delta, solutions can be real or complex

def	calculate_solutions(coeff_array, delta):
	# General case : solutions = (-b +- delta^0.5) / 2a

	if coeff_array[2] == 0 and coeff_array[1] == 0: # There is no x in the reduced equation.
		return None # Any number is a solution to the equation
	elif coeff_array[2] == 0: # That is a linear equation. There is a single solution. x = -c/b
		sol_1 = -1 * coeff_array[0] / coeff_array[1]
		sol_2 = sol_1
	elif delta >= 0:
		sol_1 = (-1 * coeff_array[1] + delta ** 0.5) / (2 * coeff_array[2])
		sol_2 = (-1 * coeff_array[1] - delta ** 0.5) / (2 * coeff_array[2])
	else:
		# Delta is negative, that means the solutions are complex
		# Solutions = (-b/2a) +- (i * |delta|^0.5 / 2a)
		# We will return an array of string instead of float
		sol_1 = (-1 * coeff_array[1] / (2 * coeff_array[2])) + (((abs(delta)) ** 0.5) / (2 * coeff_array[2]))
		sol_2 = (-1 * coeff_array[1] / (2 * coeff_array[2])) - (((abs(delta)) ** 0.5) / (2 * coeff_array[2]))
		return []
		# Better to have a separate function for complex solutions. 
	return [sol_1, sol_2]

def	calculate_delta(coeff_array):
	# delta = b^2 - 4ac
	delta = coeff_array[1] * coeff_array[1] - (4 * coeff_array[2] * coeff_array[0])
	return delta

def	display_reduced_equation(reduced_coeff_array):
	# Negative coefficient will be automatically displayed with the minus sign but not positive ones
	# We add a plus sign before positive coefficient only if they are not at the beginning of the string
	str_to_display = ""
	str_to_display += "Reduced equation is : "
	if reduced_coeff_array[2] != 0:
		str_to_display += floatToString(reduced_coeff_array[2])
		str_to_display += "x^2"
	if reduced_coeff_array[1] != 0:
		if reduced_coeff_array[1] > 0 and reduced_coeff_array[2] != 0:
			str_to_display += "+"
		str_to_display += floatToString(reduced_coeff_array[1])
		str_to_display += "x"
	if reduced_coeff_array[0] != 0:
		if reduced_coeff_array[0] > 0 and (reduced_coeff_array[2] != 0 or reduced_coeff_array[1] != 0):
			str_to_display += "+"
		str_to_display += floatToString(reduced_coeff_array[0])
	str_to_display += " = 0"
	for x in range(2): # We add a space before and after plus and minus signs that are not at the beginning of the string (They can be maximum 2)
		search_result = re.search("(?<=[^ ])[+-](?=[^ ])", str_to_display)
		if search_result != None:
			str_to_display = re.sub("(?<=[^ ])[+-](?=[^ ])", " "  + search_result[0] + " ", str_to_display, count=1)
	str_to_display = re.sub("\.0(?![0-9])", "", str_to_display) # getting rid of .0 when the coefficient is an integer
	print(str_to_display)


def	floatToString(inputValue):
	return(str(inputValue))

def	calculate_coefficients_of_reduced_equation(input_array):
	# Finding numbers with 1 or more digit, with or without dot, with or without a plus or minus sign before it, and followed by x^0, x^1 or x^2, converting them to a float, then summing them
	coeff_x_0_left_side = sum(map(float, re.findall("\+?-?[0-9.]+(?=x\^0)", input_array[0])))
	coeff_x_0_right_side = sum(map(float, re.findall("\+?-?[0-9.]+(?=x\^0)", input_array[1])))
	coeff_x_1_left_side = sum(map(float, re.findall("\+?-?[0-9.]+(?=x\^1)", input_array[0])))
	coeff_x_1_right_side = sum(map(float, re.findall("\+?-?[0-9.]+(?=x\^1)", input_array[1])))
	coeff_x_2_left_side = sum(map(float, re.findall("\+?-?[0-9.]+(?=x\^2)", input_array[0])))
	coeff_x_2_right_side = sum(map(float, re.findall("\+?-?[0-9.]+(?=x\^2)", input_array[1])))
	reduced_coeff_array = [coeff_x_0_left_side - coeff_x_0_right_side, coeff_x_1_left_side - coeff_x_1_right_side, coeff_x_2_left_side - coeff_x_2_right_side]
	return reduced_coeff_array




def	args_check_and_treatment(argv):
	# look for errors in equation, remove unneeded chars, normalize coefficients and exponents and split both side of the equal sign
	if len(argv) != 2:
		print("We allow strictly 1 argument. It has to be the equation in a single string (Between quotes).")
		print('Usage : ./computor "YOUR QUADRATIC EQUATION"')
		exit()
	if argv[1].count('=') != 1:
		print("Your equation must have one and only one equal sign --> =")
		print('An example of a valid equation is : "x^2 + 4x + 6 = 2x + 8 - 3x^2"')
		exit()
	#treated_equation = argv[1].replace(' ', '').replace('*', '').lower()
	treated_equation = re.sub("[*\s]+", "", argv[1]).lower() # Removing stars, whitespaces, and making all X lower case

	if check_for_common_errors(treated_equation) == False:
		exit()
	treated_equation = normalize_coeff_and_exponents(treated_equation)

	treated_equation = treated_equation.split("=")

	return treated_equation


def	check_for_common_errors(equation_string):
	result = True
	if re.search("[+\-.^][+\-.^]", equation_string) != None: # any 2 of those signs next to each other : [+-.^]
		print("Problem with equation : 2 or more of those signs are next to each other : [+-.^]")
		result = False
	if re.search("\^(?![0-2])", equation_string) != None: # exponent sign that is not followed by 0 - 1 - 2
		print("Problem with equation : Each exponent sign --> ^ must be followed by one of those numbers [012]")
		result = False
	if re.search("[+-](?![0-9x])", equation_string) != None: # + - with no digit after it
		print("Problem with equation : Each + or - need to be followed by a number.")
		print(equation_string)
		result = False
	search_result = re.search("[^x+\-.^=0-9]", equation_string)
	if search_result != None: #any other sign than {x+-.^=[0-9]}
		print("Problem with equation : Wrong character --> ", search_result[0])
		result = False
	return result



def	normalize_coeff_and_exponents(equation):
	
	result = re.sub("(?<![0-9])x", "1x", equation) # Adding coefficient 1 when x doesn't have a coefficient
	
	result = re.sub("x(?!\^)", "x^1", result) # Adding power of 1, where there is no exponent

	#print("Equation before normalization : ", result)
	search_result = re.search("(?<!\^)[0-9](?![x.0-9])", result)
	while (search_result != None):
		result = re.sub("(?<!\^)[0-9](?![x.0-9])", search_result[0] + "x^0", result, count=1) # Adding x^0 to numbers that are not an exponent, and that are not followed by x (or . or another number)
		search_result = re.search("(?<!\^)[0-9](?![x.0-9])", result)
	#print("Equation after : ", result)
	return result





if __name__ == "__main__":
	main()