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
	clean_input_array = args_check_and_treatment(sys.argv) # will exit the program if input is bad. clean_input_array is an array of two strings. They are both sides of the equation, separated by the =
	coeff_dict = calculate_coefficients_of_reduced_equation(clean_input_array) # coeff_dict is a dictionary : exponents (string) --> coefficients (float)
	display_reduced_equation(coeff_dict)
	verify_that_the_reduced_equation_is_solvable(coeff_dict) # will exit the program if cannot solve
	calculate_solutions(coeff_dict)

def calculate_solutions(coeff_dict):
	if "0" not in coeff_dict:
		coeff_dict["0"] = 0
	if "1" not in coeff_dict:
		coeff_dict["1"] = 0
	if "2" not in coeff_dict:
		coeff_dict["2"] = 0
	if coeff_dict["2"] == 0 and coeff_dict["1"] == 0: # There is no x in the reduced equation.
		if coeff_dict["0"] == 0:
			print("There is no x in the reduced equation. Any number is a solution.")
		else:
			print("The reduced equation is trivially false. There is no solution.")
	elif coeff_dict["2"] == 0:
		display_solution_linear(coeff_dict)
	else:
		display_solutions_quadratic(coeff_dict)


def	display_solution_linear(coeff_dict):
	# There is a single solution. x = -c/b
	sol = -1 * coeff_dict["0"] / coeff_dict["1"]
	print("The equation is linear. There is only one solution : x = -c/b")
	print(f"x = {float_to_string(sol)}")

def	display_solutions_quadratic(coeff_dict):
	print("\nThe discriminant Delta has the formula : Delta = b^2 - 4ac")
	print("Delta can be either strictly positive, zero, or strictly negative, with the following consequences :")
	print("Delta > 0 --> There are two distinct real solutions.")
	print("Delta == 0 --> There is a single real solution, also called a double root.")
	print("Delta < 0 --> There are two distinct complex solutions.")
	delta = calculate_delta(coeff_dict)
	print(f"\nDelta = {float_to_string(delta)}")
	if delta < 0:
		display_complex_solutions(coeff_dict, delta)
	else:
		display_real_solutions(coeff_dict, delta)

def	display_complex_solutions(coeff_dict, delta):
	# Solutions = (-b/2a) +- (i * |delta|^0.5 / 2a)
	# x = real_part +- i * complex_part
	print("\nThe complex solutions have the formula : x = (-b/2a) ± (i * |delta|^0.5 / 2a)")
	real_part = (-1 * coeff_dict["1"] / (2 * coeff_dict["2"]))
	complex_part = my_square_root((my_abs(delta))) / (2 * my_abs(coeff_dict["2"]))
	sol_1 = float_to_string(real_part) + " + " + float_to_string(complex_part) + " i"
	sol_2 = float_to_string(real_part) + " - " + float_to_string(complex_part) + " i"
	print(f"x1 = {sol_1} | x2 = {sol_2}")

def	display_real_solutions(coeff_dict, delta):
	# General case : solutions = (-b +- delta^0.5) / 2a
	print("The real solutions have the formula : x = (-b ± delta^0.5) / 2a")
	sol_1 = (-1 * coeff_dict["1"] + my_square_root(delta)) / (2 * coeff_dict["2"])
	sol_2 = (-1 * coeff_dict["1"] - my_square_root(delta)) / (2 * coeff_dict["2"])
	if delta == 0:
		print("Delta is zero, both solutions are the same, and can be expressed with the formula x = -b/2a")
		print(f"x = {float_to_string(sol_1)}")
	else:
		print(f"x1 = {float_to_string(sol_1)} | x2 = {float_to_string(sol_2)}")

def	calculate_delta(coeff_dict):
	# delta = b^2 - 4ac
	delta = coeff_dict["1"] * coeff_dict["1"] - (4 * coeff_dict["2"] * coeff_dict["0"])
	return delta

def	display_reduced_equation(coeff_dict):
	# making an ordered list of all exponents that have a non zero coefficient in the equation
	exponent_list = []
	for exponent in coeff_dict:
		if coeff_dict[exponent] != 0:
			exponent_list.append(exponent)
	exponent_list.sort(reverse=True) # highest exponent at the beginning
	print("Reduced equation is : ", end="")
	if len(exponent_list) == 0:
		print("0 = 0")
		print("That's an equation of degree 0")
		return
	for exponent in exponent_list:
		# printing the + or - that precedes the coefficient
		if coeff_dict[exponent] > 0 and exponent != exponent_list[0]:
			print(" + ", end="")
		if coeff_dict[exponent] < 0 and exponent != exponent_list[0]:
			print(" - ", end="")
		if coeff_dict[exponent] < 0 and exponent == exponent_list[0]:
			print("-", end="")
		# printing the coefficient
		# si le coeff == 1 on ecrit pas, sauf si exposant = 0
		if my_abs(coeff_dict[exponent]) != 1 or (my_abs(coeff_dict[exponent]) == 1 and exponent == "0"):
			print(f"{float_to_string(my_abs(coeff_dict[exponent]))}", end="")
		# printing the x with its exponent
		if exponent == "1":
			print("x", end="")
		if exponent != "0" and exponent != "1":
			print(f"x^{exponent}", end="")
	print(" = 0")
	print(f"That's an equation of degree {exponent_list[0]}")

def	verify_that_the_reduced_equation_is_solvable(coeff_dict):
	for exponent in coeff_dict:
		if (exponent != "0" and exponent != "1" and exponent != "2" and coeff_dict[exponent] != 0):
			print("This program only solves equation of degree up to 2 with exponents that are positive integers. Only possible exponents are : 0 | 1 | 2")
			print("Why not try this equation instead : x^2 + 11x = -24")
			exit()

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

	coeff_dict = dict()

# finding all exponents in both sides of the equation
# using a set to avoid duplicates
# summing all coefficient that correspond to that exponent
	exponent_set_left = set(re.findall("(?<=\^)-?[.0-9]+", input_array[0]))
	for exponent in exponent_set_left:
		regex_coeff_this_exponent = "\+?-?[0-9.]+(?=x\^" + exponent + ")"
		if exponent not in coeff_dict: # this is probably not needed for the left part
			coeff_dict[exponent] = sum(map(float, re.findall(regex_coeff_this_exponent, input_array[0])))

	exponent_set_right = set(re.findall("(?<=\^)-?[.0-9]+", input_array[1]))
	for exponent in exponent_set_right:
		regex_coeff_this_exponent = "\+?-?[0-9.]+(?=x\^" + exponent + ")"
		if exponent in coeff_dict:
			coeff_dict[exponent] -= sum(map(float, re.findall(regex_coeff_this_exponent, input_array[1])))
		else:
			coeff_dict[exponent] = 0 - sum(map(float, re.findall(regex_coeff_this_exponent, input_array[1])))

	# # deleting all exponents that have a coefficient equal to zero
	# key_list = list(coeff_dict.keys()) # iterating over a copy of the keys to not invalidate iterators when deleting
	# for exponent in key_list:
	# 	if coeff_dict[exponent] == 0:
	# 		del coeff_dict[exponent] # maybe no need for that, can just used the ordered list and check for value each time

	return coeff_dict

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
	treated_equation = re.sub("[*\s]+", "", argv[1]).lower() # Removing stars, whitespaces, and making all X lower case
	# if check_for_common_errors(treated_equation) == False:
	# 	exit()
	if check_for_common_errors(argv[1]) == False:
		exit()
	treated_equation = normalize_coeff_and_exponents(treated_equation)
	treated_equation = treated_equation.split("=")
	return treated_equation

def	check_for_common_errors(equation_string):
	result = True
	equation_string = re.sub("[\s]+", "", equation_string).lower() # Removing whitespaces and making all X lower case
	if re.search("(?<![0-9])\*|\*(?!x)", equation_string) != None: # a * that is at the wrong place. Something like "3x * = 6"
		print("ERROR : * is at the wrong place")
		result = False
	equation_string = equation_string.replace("*", "") # Removing all stars
	split_result = equation_string.split("=")
	if len(split_result[0]) == 0 or len(split_result[1]) == 0: # something like " = 4x" or "3x^2 + 7 = "
		print("ERROR : There must be something on both sides of the equal sign")
		result = False
	if re.search("[+\-.][+\-.]", equation_string) != None: # any 2 of those signs next to each other : [+-.^] --> the ^ was removed to allow negative exponent at this point
		print("ERROR : 2 or more of those signs are next to each other : [+-.]")
		result = False
	if re.search("xx", equation_string) != None:
		print("ERROR : Two x cannot be next to each other")
		result = False
	if re.search("(?<!x)\^", equation_string) != None: # exponent sign that is not preceded by x
		print("ERROR : Each exponent sign --> ^ must be preceded by x")
		result = False
	if re.search("\^(?![0-9-+])", equation_string) != None: # exponent sign that is followed by something else than a minus sign, a plus sign or a number
		print("ERROR : Each exponent sign --> ^ must be followed by a number")
		result = False
	exponent_regex = "(?<=\^)-?\+?[.0-9]+x?" # Used to detect an empty exponent. Something like "8x^ + 9x = 0"
	exponent_list = re.findall(exponent_regex, equation_string)
	for exponent in exponent_list:
		if exponent.count('x') != 0: # an empty exponent will take the next term of the equation as the exponent, that will include an x
			print("ERROR : Issue with exponent")
			result = False
	if re.search("[+-](?![0-9x])", equation_string) != None: # + - with no digit after it
		print("ERROR : Each + or - need to be followed by a number or x")
		result = False
	if re.search("(?<![0-9])\.|\.(?![0-9])", equation_string) != None: # decimal dot that doesn't have numbers on both sides
		print("ERROR : Decimal numbers need to have numbers on both side of the decimal dot")
		result = False
	if re.search("[0-9]+\.[0-9]+\.[0-9]", equation_string) != None: # testing for things like 2.3.5
		print("ERROR : A number cannot have more than one dot")
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
	exponent_regex = "(?<=\^)-?\+?[.0-9]+"
	exponent = re.search(exponent_regex, result) # get the exponent value
	while (exponent != None):
		result = re.sub(exponent_regex, "!" + float_to_string(float(exponent[0])), result, count=1) # converting exponents to float then back to str using the custom function, to avoid -0 or 02 or .0 etc
		exponent = re.search(exponent_regex, result) # get the exponent value
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
	maximum_gap = 0.00000001
	# as a first guess, I arbitraly divide the number by 8.
	square_root = nbr / 8
	while (my_abs((square_root * square_root) - nbr) > maximum_gap):
		square_root = 0.5 * (square_root + (nbr / square_root)) # Heron's method
	return square_root

if __name__ == "__main__":
	main()
