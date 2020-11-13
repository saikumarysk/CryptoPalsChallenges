from Crypto.Cipher import AES
from random import randint
from base64 import b64decode

def keygen() -> str :
	key = b''
	for _ in range(16) :
		key += bytes([randint(0,255)])

	return key

KEY = keygen()
appendix = ''
with open('12.txt', 'r') as file :
	appendix = b64decode(file.read())

def repetitions(input: str) -> int :
	blocks = [input[i:i+16] for i in range(0, len(input), 16)]
	return len(blocks) - len(set(blocks))

def pad(input: str) -> str :
	rem = len(input)%16
	if rem :
		input += bytes([16 - rem])*(16-rem)
	return input

def encryption_oracle(plaintext: str) -> str :
	plaintext += appendix
	plaintext = pad(plaintext)

	return AES.new(KEY, AES.MODE_ECB).encrypt(plaintext)

def detect_block_size() -> int :
	guess = 0
	for i in range(256) :
		ciphertext = encryption_oracle(b'A'*i)
		if repetitions(ciphertext) != 0 :
			guess = i//2 #As first repetition occurs at twice the size
			if repetitions(encryption_oracle(b'A'*(3*guess))) != 0 and\
			 repetitions(encryption_oracle(b'A'*(4*guess))) != 0 :
				break

	return guess

def detect_ecb() -> bool :
	input = bytes(64)
	for _ in range(1000) :
		ciphertext = encryption_oracle(input)
		if repetitions(ciphertext) == 0 : return False

	return True

def attack() -> str :
	output = b''
	for i in range(138) :
		dict = {}
		for j in range(128) :
			v = bytes([j])
			k = encryption_oracle(b'A'*(143 - len(output))+output+v)[:144]
			if k in dict :
				dict[k].append(v)
			else :
				dict[k] = [v]

		output += dict[encryption_oracle(b'A'*(143 - len(output)))[:144]][0]

	return output

if __name__ == '__main__' :
	block_size = detect_block_size()
	print('Block size is -', block_size)

	is_ecb = detect_ecb()
	print('Is the oracle using ECB?', is_ecb)

	first_byte = attack()
	print(first_byte)
