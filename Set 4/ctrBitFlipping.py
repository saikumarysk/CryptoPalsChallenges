from aesInCTR import aesCTR
from random import randint

def keygen() -> str :
	return random_bytes(16)

def random_bytes(n: int) -> str :
	output = b''
	for _ in range(n) :
		output += bytes([randint(0, 255)])

	return output

KEY = keygen()

def encrypt(plaintext: str) -> str :
	plaintext = plaintext.replace(b';', b'%3B')
	plaintext = plaintext.replace(b'=', b'%3D')
	plaintext = b'comment1=cooking%20MCs;userdata=' + plaintext +\
	 b';comment2=%20like%20a%20pound%20of%20bacon'

	cipher = aesCTR(KEY)
	return cipher.encrypt(plaintext)

def decrypt(ciphertext: str) -> str :
	cipher = aesCTR(KEY)
	print(plaintext)

	if b';admin=true;' in plaintext :
		print('You did it!')
	else :
		print('Nope. Try again!')

if __name__ == '__main__' :
	plaintext = b'?admin?true?????'

	ciphertext = encrypt(plaintext)
	ciphertext = ciphertext[:32] + bytes([ciphertext[32] ^ ord('?') ^ ord(';')]\
	 ) + ciphertext[33:]
	ciphertext = ciphertext[:38] + bytes([ciphertext[38] ^ ord('?') ^ ord('=')]\
	 ) + ciphertext[39:]
	ciphertext = ciphertext[:43] + bytes([ciphertext[43] ^ ord('?') ^ ord(';')]\
	 ) + ciphertext[44:]

	decrypt(ciphertext)
