from base64 import b64decode
import aesInCBC
from random import randint, choice

def keygen() -> str :
	return random_bytes(16)

def random_bytes(n: int) -> str :
	output = b''
	for _ in range(n) :
		output += bytes([randint(0, 255)])

	return output

KEY = keygen()

plaintexts = []
with open('17.txt', 'r') as file :
	plaintexts = [b64decode(x) for x in file.read().splitlines()]

def pad(input: str) -> str :
	rem = len(input)%16
	if rem :
		input += bytes([16 - rem])*(16 - rem)

	return input

def valid_padding(input: str) -> bool :
	return input[-input[-1]:] == bytes([input[-1]])*(input[-1])

def remove_padding(input: str) -> str :
	if valid_padding(input) :
		input = input[:-input[-1]]

	return input

def encrypt() -> str :
	plaintext = plaintexts[randint(0, len(plaintexts)-1)]
	plaintext = pad(plaintext)

	iv = random_bytes(16)

	cipher = aesInCBC.aesCBC(KEY, iv)
	return cipher.encrypt(plaintext), iv

def decrypt(ciphertext: str, iv: str) -> bool :
	plaintext = aesInCBC.aesCBC(KEY, iv).decrypt(ciphertext)
	return valid_padding(plaintext)

def get_forced_iv(block: str, guess: int, padding_length: int, plaintext: str)\
 -> str :
	forced = int(block[-padding_length]) ^ guess ^ padding_length

	output = block[:-padding_length] + bytes([forced])

	j = 0
	for i in range(16 - padding_length + 1, 16) :
		forced = int(block[i]) ^ int(plaintext[j]) ^ padding_length
		output += bytes([forced])
		j += 1

	return output

def attack(ciphertext: str, iv: str) -> str :
	plaintext = b''
	blocks = [iv] + [ciphertext[i:i+16] for i in range(0, len(ciphertext), 16)]

	for i in range(1, len(blocks)) :
		plaintext_block = b''
		prev_ciphertext_block = blocks[i-1]
		for j in range(15, -1, -1) :
			padding_length = len(plaintext_block) + 1
			possible = []
			for k in range(256) :
				forced_iv = get_forced_iv(prev_ciphertext_block, k,\
				 padding_length, plaintext_block)
				if decrypt(blocks[i], forced_iv) :
					possible.append(bytes([k]))

			if len(possible) > 1:
				for b in possible :
					for k in range(256) :
						forced_iv = get_forced_iv(prev_ciphertext_block, k,\
						 padding_length + 1, b + plaintext)

						if decrypt(blocks[i], forced_iv) :
							possible = [b]
							break

			plaintext_block = possible[0] + plaintext_block

		plaintext += plaintext_block

	return remove_padding(plaintext)

if __name__ == '__main__' :
	ciphertext, iv = encrypt()
	print(ciphertext, iv)
	plaintext = attack(ciphertext, iv)
	print('Plaintext -', plaintext)
