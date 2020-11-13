from Crypto.Cipher import AES
import aesInCBC
from random import randint

def keygen() -> str :
	return randbytestring(16)

def randbytestring(n: int) -> str :
	output = b''
	for _ in range(n) :
		output += bytes([randint(0,255)])

	return output

def pad(input: str) -> str :
	rem = len(input)%16
	if rem :
		input += bytes([16 - rem])*(16 - rem)

	return input

def repetitions(input: str) -> int :
	blocks = [input[i:i+16] for i in range(0, len(input), 16)]
	return len(blocks) - len(set(blocks))

def encryption_oracle(plaintext: str) -> str :
	plaintext = randbytestring(randint(5,10)) + plaintext +\
	 randbytestring(randint(5,10))
	plaintext = pad(plaintext)
	if randint(0,1) :
		return aesECB(plaintext), 'ECB'
	return aesCBC(plaintext), 'CBC'

def aesECB(plaintext: str) -> str :
	cipher = AES.new(keygen(), AES.MODE_ECB)
	return cipher.encrypt(plaintext)

def aesCBC(plaintext: str) -> str :
	cipher = aesInCBC.aesCBC(keygen(), randbytestring(16))
	return cipher.encrypt(plaintext)


if __name__ == '__main__' :
	plaintext = bytes(64)
	for _ in range(1000) :
		ciphertext = encryption_oracle(plaintext)
		mode_used = 'ECB' if repetitions(ciphertext[0]) != 0 else 'CBC'
		assert mode_used == ciphertext[1]

	print('Oracle prediction correct')
