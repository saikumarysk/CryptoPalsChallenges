from base64 import b64decode
from aesInCTR import aesCTR
from random import randint

def xor(s1: str, s2: str) -> str :
	output = b''
	for c1, c2 in zip(s1, s2) :
		output += bytes([int(c1)^int(c2)])

	return output

def keygen() -> str :
	return random_bytes(16)

def random_bytes(n: int) -> str :
	output = b''
	for _ in range(n) :
		output += bytes([randint(0,255)])

	return output

plaintexts = []
with open('19.txt', 'r') as file :
	plaintexts = [b64decode(x) for x in file.read().splitlines()]

KEY = keygen()
cipher = aesCTR(KEY)

ciphertexts = [cipher.encrypt(plaintext) for plaintext in plaintexts]

#Too lazy to do manual analysis. Leave it
