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
	print(clean_input_array)
	reduced_coeff_array = calculate_coefficients_of_reduced_equation(clean_input_array)
	display_reduced_equation(reduced_coeff_array)


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