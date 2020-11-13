from Crypto.Cipher import AES
from base64 import b64decode

class aesCBC(object) :

	def __init__(self, key: str, iv: str) :
		self.key = key
		self.block_size = len(self.key)
		self.iv = iv
		self.aes = AES.new(self.key, AES.MODE_ECB)

	def xor(self, s1: str, s2: str) -> str :
		output = b''
		for c1, c2 in zip(s1, s2) :
			output += bytes([int(c1)^int(c2)])

		return output

	def encrypt(self, plaintext: str) -> str :
		blocks = [plaintext[i: i + self.block_size] for i in range(0,\
		 len(plaintext), self.block_size)]
		blocks[-1] = blocks[-1] + bytes([self.block_size - len(blocks[-1])])*\
		 (self.block_size - len(blocks[-1]))

		addendum = self.iv
		output = b''
		for block in blocks :
			curr_block = self.xor(block, addendum)
			curr_encrypted = self.aes.encrypt(curr_block)
			output += curr_encrypted
			addendum = curr_encrypted

		return output

	def decrypt(self, ciphertext: str) -> str :
		blocks = [ciphertext[i:i+self.block_size] for i in range(0,\
		 len(ciphertext), self.block_size)]

		output = b''
		addendum = self.iv
		for block in blocks :
			decrypted_block = self.aes.decrypt(block)
			output += self.xor(decrypted_block, addendum)
			addendum = block

		return output

if __name__ == '__main__' :
	ciphertext = ''
	with open('10.txt','r') as file :
		ciphertext = b64decode(file.read())

	cipher = aesCBC("YELLOW SUBMARINE", bytes(16))
	print('Ciphertext -', ciphertext)
	decrypted_plaintext = cipher.decrypt(ciphertext)
	print('Decrypted stuff -',decrypted_plaintext)

	reencrypted_ciphertext = cipher.encrypt(decrypted_plaintext)
	print('After encryption of decrypted stuff -', reencrypted_ciphertext)
	print('Are ciphertext and reencrypted_ciphertext same?', ciphertext ==\
	 reencrypted_ciphertext)
