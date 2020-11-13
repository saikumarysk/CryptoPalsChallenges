def validate(input: str) -> bool :
	if not input : return False
	input = input.lower()
	import re
	pattern = re.compile('^[0-9a-f]+$')
	return True if pattern.match(input) else False

def fixedXOR(a: str, b: str) -> str :
	padlength = abs(len(a) - len(b))

	if padlength :
		if len(a) < len(b) :
			a = '0'*padlength + a
		else :
			b = '0'*padlength + b

	output = ''
	for i in range(len(a)) :
		outputNum = hexToNum(a[i]) ^ hexToNum(b[i])
		output += numToHex(outputNum)

	return output

def hexToNum(input: str) -> int :
	if input.isnumeric() : return int(input)
	return ord(input)-97+10

def numToHex(input: int) -> str :
	if 0 <= input <= 9 : return str(input)
	return chr(input - 10 + 97)

if __name__ == '__main__' :
	testString1 = input('Enter first string in lowercase : ')
	testString2 = input('Enter second string in lowercase : ')

	if not validate(testString1) or not validate(testString2) :
		print('Enter valid strings\n')
		from sys import exit
		exit(1)

	testString1 = testString1.lower()
	testString2 = testString2.lower()

	testStringOut = fixedXOR(testString1, testString2)
	print('XOR string -', testStringOut)
