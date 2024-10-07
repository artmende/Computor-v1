#!/usr/bin/python3

# All regex formulas here were crafted with the help of https://regexr.com/.
# Please visit the website for formulas explanation

# https://wolfreealpha.gitlab.io to compare results quickly

import sys
import re

# save both sides of the equation
# sum all coefficient of each power of x, using regex, for both sides of equal
# Display the reduced form
# apply the math formula to get the discriminant, and to get the roots

# Examples of equations
# 8 * x^2 + 7 * x^1 - 9.4 * X = 8x + 2 - 7x^2 + 3.3*x^0 ---> real roots
# x + 7x^2 - 6 = 4 * x^0 + 8 * x^1 - 8.1 + 43*x^2 ---> complex roots

#########################################
# THINGS TO DO !
# Calculate reduced form of equation before looking at exponent. So we can get the degree anyway, and some higher degree might simplify themselves

def	main():
	clean_input_array = args_check_and_treatment(sys.argv) # will exit the program if input is bad
	reduced_coeff_array = calculate_coefficients_of_reduced_equation(clean_input_array)
	
	display_reduced_equation(reduced_coeff_array)

	##### HERE calculate and display at the same time
	if reduced_coeff_array[2] == 0 and reduced_coeff_array[1] == 0 : # There is no x in the reduced equation.
		print("Equation of degree 0")
		if reduced_coeff_array[0] == 0:
			print("There is no x in the reduced equation. Any number is a solution.")
		else:
			print("The reduced equation is trivially false. There is no solution.")
	elif reduced_coeff_array[2] == 0:
		display_solution_linear(reduced_coeff_array)
	else:
		display_solutions_quadratic(reduced_coeff_array)

def	display_solution_linear(coeff_array):
	# There is a single solution. x = -c/b
	sol = -1 * coeff_array[0] / coeff_array[1]
	print("Equation of degree 1")
	print("The equation is linear. There is only one solution : x = -c/b")
	print(f"x = {float_to_string(sol)}")

def	display_solutions_quadratic(coeff_array):
	print("Equation of degree 2")
	print("\nThe discriminant Delta has the formula : Delta = b^2 - 4ac")
	print("Delta can be either strictly positive, zero, or strictly negative, with the following consequences :")
	print("Delta > 0 --> There are two distinct real solutions.")
	print("Delta == 0 --> There is a single real solution, also called a double root.")
	print("Delta < 0 --> There are two distinct complex solutions.")
	delta = calculate_delta(coeff_array)
	print(f"\nDelta = {float_to_string(delta)}")
	if delta < 0:
		display_complex_solutions(coeff_array, delta)
	else:
		display_real_solutions(coeff_array, delta)

def	display_complex_solutions(coeff_array, delta):
	# Solutions = (-b/2a) +- (i * |delta|^0.5 / 2a)
	# x = real_part +- i * complex_part
	print("\nThe complex solutions have the formula : x = (-b/2a) ± (i * |delta|^0.5 / 2a)")
	real_part = (-1 * coeff_array[1] / (2 * coeff_array[2]))
	#complex_part = ((abs(delta)) ** 0.5) / (2 * coeff_array[2])
	complex_part = my_square_root((my_abs(delta))) / (2 * my_abs(coeff_array[2]))
	sol_1 = float_to_string(real_part) + " + " + float_to_string(complex_part) + " i"
	sol_2 = float_to_string(real_part) + " - " + float_to_string(complex_part) + " i"
	print(f"x1 = {sol_1} | x2 = {sol_2}")

def	display_real_solutions(coeff_array, delta):
	# General case : solutions = (-b +- delta^0.5) / 2a
	print("The real solutions have the formula : x = (-b ± delta^0.5) / 2a")
	sol_1 = (-1 * coeff_array[1] + my_square_root(delta)) / (2 * coeff_array[2])
	sol_2 = (-1 * coeff_array[1] - my_square_root(delta)) / (2 * coeff_array[2])
	if delta == 0:
		print("Delta is zero, both solutions are the same, and can be expressed with the formula x = -b/2a")
		print(f"x = {float_to_string(sol_1)}")
	else:
		print(f"x1 = {float_to_string(sol_1)} | x2 = {float_to_string(sol_2)}")

def	calculate_delta(coeff_array):
	# delta = b^2 - 4ac
	delta = coeff_array[1] * coeff_array[1] - (4 * coeff_array[2] * coeff_array[0])
	return delta

def	display_reduced_equation(reduced_coeff_array):
	# Negative coefficient will be automatically displayed with the minus sign but not positive ones
	# We add a plus sign before positive coefficient only if they are not at the beginning of the string
	print("\nThe reduced equation is the standard form 'ax^2 + bx + c = 0' with 3 coefficients (a, b, c).")
	print(f"Here we have a = {float_to_string(reduced_coeff_array[2])} | b = {float_to_string(reduced_coeff_array[1])} | c = {float_to_string(reduced_coeff_array[0])}")
	str_to_display = "Reduced equation is : "
	if reduced_coeff_array[2] != 0:
		str_to_display += float_to_string(reduced_coeff_array[2])
		str_to_display += "x^2"
	if reduced_coeff_array[1] != 0:
		if reduced_coeff_array[1] > 0 and reduced_coeff_array[2] != 0:
			str_to_display += "+"
		str_to_display += float_to_string(reduced_coeff_array[1])
		str_to_display += "x"
	if reduced_coeff_array[0] != 0 or (reduced_coeff_array[1] == 0 and reduced_coeff_array[2] == 0):
		if reduced_coeff_array[0] > 0 and (reduced_coeff_array[2] != 0 or reduced_coeff_array[1] != 0):
			str_to_display += "+"
		str_to_display += float_to_string(reduced_coeff_array[0])
	str_to_display += " = 0"
	for x in range(2): # We add a space before and after plus and minus signs that are not at the beginning of the string (They can be maximum 2)
		search_result = re.search("(?<=[^ ])[+-](?=[^ ])", str_to_display)
		if search_result != None:
			str_to_display = re.sub("(?<=[^ ])[+-](?=[^ ])", " "  + search_result[0] + " ", str_to_display, count=1)
	str_to_display = re.sub("\.0(?![0-9])", "", str_to_display) # getting rid of .0 when the coefficient is an integer
	str_to_display = re.sub("(?<![0-9])1(?=x)", "", str_to_display) # getting rid of coefficient 1 for x and x^2 --> Find 1 that doesnt have another digit before it and that is followed by x, and delete it
	print(str_to_display)

def	float_to_string(inputValue):
	result = round(inputValue, 6)
	result = str(result)
	result = re.sub("\.0(?![0-9])", "", result) # getting rid of .0 when the there is no other digit after the 0
	if inputValue == 0:
		result = result.replace("-", "") # avoiding -0
	return result

def	calculate_coefficients_of_reduced_equation(input_array):
	# for every different exponent, sum all of their respective coefficient
	# the highest exponent for which the final coefficient is not zero is the degree of the equation
	# if there are non zero coefficient for any other exponent than 0 - 1 - 2 , the equation is not supported

	# do a findall to select all exponents, and browse through the result, adding them one by one in a dictionary (creating new entry for new exponent, adding to the existing for repeated exponent)

	print("Input array left : ", input_array[0])
	print("Input array right : ", input_array[1])
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
	split_result = equation_string.split("=")
	if len(split_result[0]) == 0 or len(split_result[1]) == 0: # something like " = 4x" or "3x^2 + 7 = "
		print("ERROR : There must be something on both sides of the equal sign")
		result = False
	if re.search("[+\-.][+\-.]", equation_string) != None: # any 2 of those signs next to each other : [+-.^] --> the - was removed to allow negative exponent at this point
		print("ERROR : 2 or more of those signs are next to each other : [+-.]")
		result = False
	#exponents_array = re.findall("(?<=\^)-?[.0-9]+", equation_string) # get the exponent value
	#for i in range(len(exponents_array)):
	#	if exponents_array[i].count('.') != 0:# or int(exponents_array[i]) > 2 or int(exponents_array[i]) < 0:
	#		#print("ERROR : Exponents cannot be lower than 0 or higher than 2 and need to be integer. Only possible exponents are : 0 | 1 | 2")
	#		print(f"ERROR: Exponents \'{exponents_array[i]}\' is not an integer")
	#		result = False
	#if re.search("\^(?![0-2])", equation_string) != None: # exponent sign that is not followed by 0 - 1 - 2
	#	print("ERROR : Each exponent sign --> ^ must be followed by one of those numbers [012]")
	#	result = False
	if re.search("(?<!x)\^", equation_string) != None: # exponent sign that is not preceded by x
		print("ERROR : Each exponent sign --> ^ must be preceded by x")
		result = False
	if re.search("[+-](?![0-9x])", equation_string) != None: # + - with no digit after it
		print("ERROR : Each + or - need to be followed by a number or x")
		result = False
	if re.search("(?<![0-9])\.|\.(?![0-9])", equation_string) != None: # decimal dot that doesn't have numbers on both sides
		print("ERROR : Decimal numbers need to have numbers on both side of the decimal dot")
		result = False
	wrong_char_array = re.findall("[^x+\-.^=0-9]", equation_string)
	if len(wrong_char_array) > 0: #any other sign than {x+-.^=[0-9]}
		for i in range(len(wrong_char_array)):
			print("ERROR : Wrong character --> ", wrong_char_array[i])
		result = False
	return result

def	normalize_coeff_and_exponents(equation):
	result = re.sub("(?<![0-9])x", "1x", equation) # Adding coefficient 1 when x doesn't have a coefficient
	result = re.sub("x(?!\^)", "x^1", result) # Adding power of 1, where there is no exponent
	exponent = re.search("(?<=\^)-?[.0-9]+", result) # get the exponent value
	while (exponent != None):
		result = re.sub("(?<=\^)-?[.0-9]+", "!" + float_to_string(float(exponent[0])), result, count=1) # converting exponents to float then back to str using the custom function, to avoid -0 or 02 or .0 etc
		exponent = re.search("(?<=\^)-?[.0-9]+", result) # get the exponent value
	result = re.sub("!", "", result) # We added a ! to prevent infinite loop, now we remove it
	# finding coefficients that don't have x, and adding x^0 (3x^2+2 will become 3x^2+2x^0)
	lonely_coeff_regex = "((?<=([+=]))|(?<=^)|(?<=[0-9=]-)|(?<=^-))([0-9]+)\.?([0-9]+)?(?=([-+=])|$)"
	lonely_coeff = re.search(lonely_coeff_regex, result)
	while (lonely_coeff != None):
		result = re.sub(lonely_coeff_regex, lonely_coeff[0] + "x^0", result, count=1) # Adding x^0 to those numbers
		lonely_coeff = re.search(lonely_coeff_regex, result)
	return result

def	my_abs(nbr): # the subject doesn't allow to use any math function other than addition, subraction, multiplication, division
	if nbr > 0:
		return nbr
	else:
		return -nbr

def	my_square_root(nbr): # the subject doesn't allow to use any math function other than addition, subraction, multiplication, division
	maximum_gap = 0.0000000000001
	# as a first guess, I arbitraly divide the number by 8.
	square_root = nbr / 8
	while (my_abs((square_root * square_root) - nbr) > maximum_gap):
		square_root = 0.5 * (square_root + (nbr / square_root)) # Heron's method
	return square_root

if __name__ == "__main__":
	main()
