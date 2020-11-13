from aesInCTR import aesCTR
from random import randint
from base64 import b64decode

def keygen() -> str :
	return random_bytes(16)

def random_bytes(n: int) -> str :
	output = b''
	for _ in range(n) :
		output += bytes([randint(0, 255)])

	return output

def xor(s1: str, s2: str) -> str :
	output = b''
	for c1, c2 in zip(s1, s2) :
		output += bytes([c1 ^ c2])

	return output

KEY = keygen()

def edit(ciphertext: str, offset: int, newtext: str) -> str :
	cipher = aesCTR(KEY)

	ciphertext = ciphertext[:offset] + newtext + ciphertext[offset + 1:]
	return cipher.encrypt(ciphertext)

if __name__ == '__main__' :
	plaintext = b''
	with open('25.txt', 'r') as file :
		plaintext = b64decode(file.read())

	print(plaintext)
	cipher = aesCTR(KEY)
	ciphertext = cipher.encrypt(plaintext)

	key = b''
	for i in range(len(ciphertext)) :
		modified_ciphertext = edit(ciphertext, i, b'\x00')
		key += bytes([modified_ciphertext[i]])
	decrypted_plaintext = xor(ciphertext, key)
	print(decrypted_plaintext)
	print('Are they same -', plaintext == decrypted_plaintext)
