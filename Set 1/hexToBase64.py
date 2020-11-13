def validate(input: str) -> bool :
	if not input : return False
	input = input.lower()
	import re
	pattern = re.compile('^[0-9a-f]+$')
	return True if pattern.match(input) else False

def hexToBase64(input: str) -> str :
	numbits = 4*len(input) - (4 - hexToNum(input[0]).bit_length())
	padlength = 0
	if numbits%6 :
		padlength = 6 - ( numbits%6 )
	bitstring = ''
	i = 0
	for c in input :
		binstring = bin(hexToNum(c))[2:]
		binstring = (('0'*(4 - len(binstring))) if i else '') + binstring
		if not i : i += 1
		bitstring += binstring

	bitstring = '0'*padlength + bitstring
	output = ''
	for i in range(0,len(bitstring),6) :
		output += numToBase64(int(bitstring[i:i+6], 2))

	return output

def hexToNum(input: str) -> int :
	if input.isnumeric() : return int(input)
	return ord(input)-97+10

def numToBase64(input: int) -> str :
	if 0 <= input <= 25 :
		return chr(input + 65)
	if 26 <= input <= 51 :
		return chr(input - 26 + 97)
	if 52 <= input <= 61 :
		return str(input - 52)
	return '+' if input == 62 else '/'

if __name__=='__main__' :
	testStringInp = input('Enter test string(Lower case is preferred. I will convert anyway) : ')

	if not validate(testStringInp) :
		print('Enter valid input string.\n')
		from sys import exit
		exit(1)
	
	testStringInp = testStringInp.lower()
	testStringOut = hexToBase64(testStringInp)
	print("Coverted string -",testStringOut)
