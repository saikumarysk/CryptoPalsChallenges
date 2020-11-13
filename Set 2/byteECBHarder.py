from Crypto.Cipher import AES
from random import randint
from base64 import b64decode

def keygen() -> str :
	return random_bytes(16)

def random_bytes(n: input) -> str :
	output = b''
	for _ in range(n) :
		output += bytes([randint(0,255)])

	return output

KEY = keygen()
appendix = ''
with open('12.txt', 'r') as file :
	appendix = b64decode(file.read())

random_prefix = random_bytes(randint(0, 255))

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
	plaintext = random_prefix + plaintext # As only last block matters
	plaintext = pad(plaintext)

	return AES.new(KEY, AES.MODE_ECB).encrypt(plaintext)

def get_prepend_length() -> tuple :
	i = 0
	while repetitions(encryption_oracle(b'\x00'*i + b'\x00'*32)) == 0 :
		i += 1

	ciphertext = encryption_oracle(b'\x00'*i + b'\x00'*32)
	blocks = [ciphertext[j:j+16] for j in range(0, len(ciphertext), 16)]
	j = 0
	while j < len(blocks)-1 and blocks[j] != blocks[j+1] :
		j += 1

	return (i, j*16)

def attack() -> str :
	prepend, pretext_length = get_prepend_length()
	output = b''
	for i in range(138) :
		ciphertext = encryption_oracle(b'\x00'*prepend +\
		 b'A'*(143 - len(output)))
		d = {}
		for j in range(128) :
			v = bytes([j])
			k = encryption_oracle(b'\x00'*prepend + b'A'*(143 - len(output)) +\
			 output + v)[pretext_length:pretext_length+144]
			if k in d : d[k].append(v)
			else : d[k] = [v]

		output += d[ciphertext[pretext_length:pretext_length+144]][0]
		print(output)

	return output

if __name__ == '__main__' :
	decrypted_plaintext = attack()
	print('Decrypted Plaintext -', decrypted_plaintext)
