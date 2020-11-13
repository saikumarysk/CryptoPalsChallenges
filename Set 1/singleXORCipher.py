def validate(input: str) -> bool :
	if not input : return False
	input = input.lower()
	import re
	pattern = re.compile('^[0-9a-f]+$')
	return True if pattern.match(input) else False

def singleXORCipher(input: str) -> str :
	keys, messages = [], []
	current_error, min_error = 0, float('inf')
	for c in range(128) :
		output = ''
		current_error = 0
		for i in range(0, len(input), 2) :
			deciphered_char = ((hexToNum(input[i])*16) + hexToNum(input[i+1]))^c
			if not ((deciphered_char >= 48 and deciphered_char <= 57) or \
			 (deciphered_char >= 65 and deciphered_char <= 90) or \
			 (deciphered_char >= 97 and deciphered_char <= 122) or \
			 (deciphered_char == 32)) : current_error += 1
			output += chr(deciphered_char)

		if current_error < min_error :
			min_error = current_error
			keys = [chr(c)]
			messages = [output]
		elif current_error == min_error :
			keys.append(chr(c))
			messages.append(output)

	return (keys, messages, min_error)

def hexToNum(input: str) -> int :
	if input.isnumeric() : return int(input)
	return ord(input)-97+10

if __name__ == '__main__' :
	testString = input('Enter test string in lowecase - ')

	if not validate(testString) :
		print('Enter a valid string\n')
		from sys import exit
		exit(1)

	outputString = singleXORCipher(testString)
	print('Possible Keys -', outputString[0])
	print('Possible original strings -', outputString[1])
