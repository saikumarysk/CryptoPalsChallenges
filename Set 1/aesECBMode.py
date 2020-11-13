from Crypto.Cipher import AES
from base64 import b64decode

if __name__ == '__main__' :
	cipher_text = ''
	with open('7.txt', 'r') as file :
		cipher_text = file.read()

	cipher_text = b64decode(cipher_text)
	cipher = AES.new('YELLOW SUBMARINE', AES.MODE_ECB)
	plain_text = cipher.decrypt(cipher_text)
	print(plain_text)
