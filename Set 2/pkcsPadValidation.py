def remove_padding(input: str) -> str :
	if input[-input[-1]:] == bytes([input[-1]])*input[-1] : input = input[:-input[-1]]
	return input

if __name__ == '__main__' :
	inputs = [b'ICE ICE BABY\x04\x04\x04\x04', b'ICE ICE BABY\x05\x05\x05\x05',\
	 b'ICE ICE BABY\x01\x02\x03\x04']
	print('Inputs are -', inputs)
	print('Outputs are -')
	for input in inputs :
		try :
			output = remove_padding(input)
			if output == input : raise Exception('Bad padding')
			print(output)
		except :
			print('Bad Padding')
