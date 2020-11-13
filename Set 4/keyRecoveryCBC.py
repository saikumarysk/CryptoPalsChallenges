from aesInCBC import aesCBC
from random import randint

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
		output += bytes([int(c1) ^ int(c2)])

	return output

KEY = keygen()

def encrypt(plaintext: str) -> str :
	cipher = aesCBC(KEY, KEY)
	plaintext = plaintext.replace(b';', b'%3B')
	plaintext = plaintext.replace(b'=', b'%3D')

	plaintext = b'comment1=cooking%20MCs;userdata=' + plaintext +\
	 b';comment2=%20like%20a%20pound%20of%20bacon'

	return cipher.encrypt(plaintext)

def decrypt(ciphertext: str) -> str :
	cipher = aesCBC(KEY, KEY)

	plaintext = cipher.decrypt(ciphertext)
	for c in plaintext :
		if c > 127 : raise Exception('Invalid plaintext - '+(plaintext.hex()))

	return plaintext

if __name__ == '__main__' :
	ciphertext = encrypt(b'AA')
	ciphertext = ciphertext[:16] + bytes([0])*16 + ciphertext[:16] +\
	 ciphertext[48:]

	try :
		plaintext = decrypt(ciphertext)
		print('Plaintext is -', plaintext)
	except Exception as e :
		print('Plaintext decryption faced error.')
		plaintext = bytes.fromhex(str(e)[20:])
		print('Plaintext obtained -', plaintext)
		key = xor(plaintext[:16], plaintext[32:48])
		print('Got key -', key)
		print('Are keys same -', key == KEY)
