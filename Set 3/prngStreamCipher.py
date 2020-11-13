from mt19937RNG import mt19937
from random import randint

def random_bytes(n: int) -> str :
	output = b''
	for _ in range(n) :
		output += bytes([randint(0, 255)])

	return output

class prngStreamCipher(object) :

	def __init__(self, seed) :
		self.seed = seed

	def encrypt(self, plaintext: str) -> str :
		self.rng = mt19937(self.seed)
		ciphertext = b''
		key_stream = []
		for c in plaintext :
			if not key_stream :
				rand_num = self.rng.extract_number()
				for _ in range(4) :
					key_stream.append(rand_num & 255)
					rand_num >>= 8

			ciphertext += bytes([c ^ key_stream.pop()])

		return ciphertext

	def decrypt(self, ciphertext: str) -> str :
		return self.encrypt(ciphertext)

if __name__ == '__main__' :
	plaintext = b'A'*14
	plaintext_prepend = random_bytes(randint(0, 100))

	seed = randint(0, ( 1 << 16 ) - 1)
	cipher = prngStreamCipher(seed)
	ciphertext = cipher.encrypt(plaintext_prepend + plaintext)

	possible_seeds = []
	for i in range(1<<16) :
		cipher = prngStreamCipher(i)
		if cipher.decrypt(ciphertext) == plaintext_prepend + plaintext :
			possible_seeds.append(i)

	print('Possible Seeds -', possible_seeds)
	print('Seed is -', seed)
	print('Is the assertion correct -', seed in possible_seeds)
