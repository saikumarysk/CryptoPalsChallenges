from Crypto.Cipher import AES
from base64 import b64decode

class aesCTR(object) :

	def __init__(self, key, nonce=0) :
		self.key = key
		self.nonce = nonce

	def xor(self, s1: str, s2: str) -> str :
		output = b''
		for c1, c2 in zip(s1, s2) :
			output += bytes([int(c1)^int(c2)])

		return output

	def encrypt(self, plaintext: str) -> str :
		counter = 0
		ciphertext = b''
		cipher = AES.new(self.key, AES.MODE_ECB)
		for i in range(0, len(plaintext), 16) :
			keystream = cipher.encrypt(b'\x00'*8 + bytes([counter]) + b'\x00'*7)
			ciphertext += self.xor(keystream[:len(plaintext[i:i+16])],\
			 plaintext[i:i+16])
			counter += 1

		return ciphertext

	def decrypt(self, ciphertext: str) -> str :
		return self.encrypt(ciphertext)

if __name__ == '__main__' :
	cipher = aesCTR('YELLOW SUBMARINE')
	ciphertext = b''
	with open('18.txt', 'r') as file :
		ciphertext = b64decode(file.read())

	print(ciphertext)
	decrypted_plaintext = cipher.decrypt(ciphertext)
	print(decrypted_plaintext)

	encrypted_plaintext = cipher.encrypt(decrypted_plaintext)
	print(encrypted_plaintext)

	print('Both of the encryptions are correct -', encrypted_plaintext == ciphertext)

	plaintext = cipher.decrypt(encrypted_plaintext)
	print(plaintext)
	print('\n\n')
	plaintext = b'This is a test'
	print(cipher.encrypt(plaintext))
	print(cipher.decrypt(cipher.encrypt(plaintext)))
