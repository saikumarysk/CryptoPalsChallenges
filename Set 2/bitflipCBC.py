from Crypto.Cipher import AES
from random import randint
import aesInCBC

def keygen() -> str :
	return random_bytes(16)

def random_bytes(n: int) -> str :
	output = b''
	for _ in range(n) :
		output += bytes([randint(0,255)])

	return output

KEY = keygen()
iv = random_bytes(16)

def pad(input: str) -> str :
	rem = len(input)%16
	if rem :
		input += bytes([16 - rem])*(16 - rem)

	return input

def remove_pad(input: str) -> str :
	if input[-input[-1]:] == bytes([input[-1]])*(input[-1]) : input = input[:-input[-1]]
	return input

def encrypt(plaintext: str) -> str :
	cipher = aesInCBC.aesCBC(KEY, iv)

	plaintext = plaintext.replace(b';', b'%3B')
	plaintext = plaintext.replace(b'=', b'%3D')

	plaintext = b'comment1=cooking%20MCs;userdata=' + plaintext +\
	 b';comment2=%20like%20a%20pound%20of%20bacon'

	plaintext = pad(plaintext)

	return cipher.encrypt(plaintext)

def decrypt(ciphertext: str) -> str :
	cipher = aesInCBC.aesCBC(KEY, iv)

	plaintext = cipher.decrypt(ciphertext)
	plaintext = remove_pad(plaintext)
	if b';admin=true;' in plaintext :
		print('You did it')
	else :
		print('Ehh! Try again')

if __name__ == '__main__' :
	plaintext = b'?admin?true?????'
	print(plaintext)
	ciphertext = encrypt(plaintext)
	print(ciphertext)
	ciphertext = ciphertext[:16] + bytes([ciphertext[16]^ord('?')^ord(';')]) +\
	 ciphertext[17:]
	ciphertext = ciphertext[:27] + bytes([ciphertext[27]^ord('?')^ord(';')]) +\
	 ciphertext[28:]
	ciphertext = ciphertext[:22] + bytes([ciphertext[22]^ord('?')^ord('=')]) +\
	 ciphertext[23:]
	decrypt(ciphertext)
