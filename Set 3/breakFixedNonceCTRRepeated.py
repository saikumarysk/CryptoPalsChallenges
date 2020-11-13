from aesInCTR import aesCTR
from base64 import b64decode

def xor(s1: str, s2: str) -> str :
	output = b''
	for c1, c2 in zip(s1, s2) :
		output += bytes([int(c1)^int(c2)])

	return output

def singleKeyXORBreak(input: str) :
	min_error = float('inf')
	outputs, keys = [], []
	considering=[32, *[i for i in range(65, 91)], *[i for i in range(97, 123)]]
	for c in range(256) :
		key = bytes([c])
		error_seen = 0
		output = b''
		for i in range(len(input)) :
			v = input[i] ^ c
			output += bytes([v])
			if v not in considering :
				error_seen += 1

		if error_seen <= min_error :
			outputs = [output]
			keys = [key*len(input)]
			min_error = error_seen

	return outputs[0]

if __name__ == '__main__' :
	plaintexts = []
	with open('20.txt', 'r') as file :
		plaintexts = [b64decode(x) for x in file.read().splitlines()]
	print(*plaintexts, sep='\n')

	cipher = aesCTR('YELLOW SUBMARINE')
	ciphertexts = [cipher.encrypt(plaintext) for plaintext in plaintexts]
	#print(ciphertexts)

	min_cipher_text_length=min([len(ciphertext) for ciphertext in ciphertexts])

	ciphertexts = [ciphertext[:min_cipher_text_length] for ciphertext in\
	 ciphertexts]
	#print(ciphertexts)

	blocks = [b'' for _ in range(min_cipher_text_length)]
	for i in range(min_cipher_text_length) :
		for ciphertext in ciphertexts :
			blocks[i] += bytes([ciphertext[i]])
	#print(blocks)

	dec_blocks = [singleKeyXORBreak(block) for block in blocks]
	#print(dec_blocks)

	new_plaintexts = [b'' for _ in range(len(blocks[0]))]
	for i in range(len(new_plaintexts)) :
		for dec_block in dec_blocks :
			new_plaintexts[i] += bytes([dec_block[i]])

	print(*new_plaintexts, sep='\n')

	for new_plaintext, plaintext in zip(new_plaintexts, plaintexts) :
		print(new_plaintext in plaintext)
