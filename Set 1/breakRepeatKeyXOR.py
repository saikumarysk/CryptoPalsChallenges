import heapq
from base64 import b64decode

def num_of_ones(x: int) -> int :
	res = 0
	while x :
		res += 1
		x = x & (x-1)

	return res

def hamming(s1: str, s2: str) -> str :
	res = 0
	for c1, c2 in zip(s1, s2) :
		res += num_of_ones(int(c1)^int(c2))
	return res

def singleXORCipher(input: str) -> str :
	key, message = '', ''
	current_error, min_error = 0, float('inf')
	for c in range(128) :
		output = ''
		current_error = 0
		for i in range(len(input)) :
			deciphered_char = int(input[i])^c
			if not ((deciphered_char >= 48 and deciphered_char <= 57) or \
			 (deciphered_char >= 65 and deciphered_char <= 90) or \
			 (deciphered_char >= 97 and deciphered_char <= 122) or \
			 (deciphered_char == 32)) : current_error += 1
			output += chr(deciphered_char)

		if current_error < min_error :
			min_error = current_error
			key = chr(c)
			message = output

	return (key, message, min_error)

def decrypt(input: str) -> str :
	minNormSizes = []
	for KEYSIZE in range(2, 41) :
		chunks = [input[i:i+KEYSIZE] for i in range(0, len(input), KEYSIZE)]
		sum_hamming = 0
		for i in range(0, len(chunks), 2) :
			if i < len(chunks)-1 : sum_hamming += hamming(chunks[i], chunks[i+1])
		avg_hamming_distance = sum_hamming/(len(chunks)//2)
		minNormSizes.append((avg_hamming_distance/KEYSIZE, KEYSIZE))

	KEYSIZE = min(minNormSizes)[1]
	blocks = [b'' for _ in range(KEYSIZE)]
	for i in range(len(input)) :
		blocks[i%KEYSIZE] += bytes([input[i]])

	key = ''
	messages = []
	for block in blocks :
		output = singleXORCipher(block)
		key += output[0]
		messages.append(output[1])

	output = ''
	i = 0
	while True :
		if messages[i] :
			output += messages[i][0]
			messages[i] = messages[i][1:]
		else :
			del messages[i]
		if not messages : break
		i = (i+1)%len(messages)

	return (key, output)

if __name__ == '__main__' :
	ciphertext = ''
	with open('6.txt', 'r') as file :
		ciphertext = file.read()

	ciphertext = b64decode(ciphertext)
	key, plaintext = decrypt(ciphertext)
	print('Key is -', key)
	print('Message is -', plaintext)
