def pad(input: str, block_length: int) -> str :
	rem = len(input)%block_length
	if rem :
		input += chr(block_length - rem)*(block_length - rem)

	return input

if __name__ == '__main__' :
	no_of_lines = 0
	try :
		no_of_lines = int(input('Enter number of lines in input - '))
	except :
		print('Enter a valid number!!\n')
		from sys import exit
		exit(1)

	if no_of_lines <= 0 :
		print('Done')
		from sys import exit
		exit(0)

	testString = ''
	for _ in range(no_of_lines) :
		testString += input() + "\n"

	testString = testString[:-1]

	block_length = 0
	try :
		block_length = int(input('Enter block length in bytes - '))
	except :
		print('Enter a valid number!!\n')
		from sys import exit
		exit(1)

	if block_length <= 0 :
		print('Done')
		from sys import exit
		exit(0)

	outputString = pad(testString, block_length)

	print('Padded String -', bytes(outputString, 'utf-8'))
