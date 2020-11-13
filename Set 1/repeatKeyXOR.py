key = "ICE"

def repeatKeyXOR(input: str) -> str :
	i = 0
	output = ''
	for c in input :
		hexstring = hex(ord(c)^ord(key[i]))[2:]
		output += '0'*(2-len(hexstring)) + hexstring
		i = (i+1)%3

	return output

if __name__ == '__main__' :
	no_of_lines = 0
	try :
		no_of_lines = int(input('Enter number of lines in input - '))
	except :
		print('Enter a valid number!!\n')
		from sys import exit
		exit(1)

	testString = ''
	for _ in range(no_of_lines) :
		testString += input() + "\n"

	testString = testString[:-1]

	if not testString :
		print('Enter valid input\n')
		from sys import exit
		exit(1)

	testStringOut = repeatKeyXOR(testString)
	print('Encrypted message -', testStringOut)
