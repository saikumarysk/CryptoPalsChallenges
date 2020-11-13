from Crypto.Cipher import AES
from random import randint

def keygen() -> str :
	return b''.join([bytes([randint(0,255)]) for _ in range(16)])

KEY = keygen()

def parse(ciphertext: str) -> dict :
	input = decrypt(ciphertext)
	entries = input.split(b'&')
	d = {}
	for entry in entries :
		k, v = entry.split(b'=')
		if k == b'role' :
			if v[-v[-1]:] == bytes([int(v[-1])])*int(v[-1]) : v = v[:-v[-1]]
		d[k] = v

	return d

def profile_for(input: str) :
	input = input.replace(b'&', b'%26')
	input = input.replace(b'=', b'%3D')

	plaintext = b'email='+input+b'&uid=10&role=user'

	return encrypt(plaintext)

def pad(input: str) -> str :
	rem = len(input)%16
	if rem :
		input += bytes([16 - rem])*(16-rem)
	return input

def encrypt(plaintext: str) -> str :
	cipher = AES.new(KEY, AES.MODE_ECB)
	plaintext = pad(plaintext)
	return cipher.encrypt(plaintext)

def decrypt(ciphertext: str) -> str :
	cipher = AES.new(KEY, AES.MODE_ECB)
	return cipher.decrypt(ciphertext)

if __name__ == '__main__' :
	ciphertext = profile_for(b'foo@gmail.admin' + b'\x0b'*11)
	print(ciphertext)
	admin_portion = ciphertext[16:32]
	new_ciphertext = profile_for(b'y.saik@gt.edu')
	new_ciphertext = new_ciphertext[:-16] + admin_portion
	plaintext = parse(new_ciphertext)
	print(plaintext)
