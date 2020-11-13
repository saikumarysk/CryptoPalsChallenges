from base64 import b64decode
from rsa import RSA
import sys

def modexp(b, e, m) :
	x = 1
	while e > 0 :
		b, e, x = (b*b) % m, e//2, (b*x)%m if e & 1 else x

	return x

def extended_gcd(a, m) :
	last_r, r = a, m
	x, last_x, y, last_y = 0, 1, 1, 0

	while r :
		last_r, (q, r) = r, divmod(last_r, r)
		x, last_x =  last_x - q*x, x
		y, last_y =  last_y - q*y, y

	return last_r, last_x*(-1 if a < 0 else 1), last_y*(-1 if m < 0 else 1)

def modinv(a, m) :
	g, x, y = extended_gcd(a, m)
	if g != 1 : raise ValueError
	return x % m

class rsaOracle(object) :
	def __init__(self) :
		self.rsa = RSA(1024)

	def get_public_key(self) :
		return self.rsa.get_public_key()

	def get_parity(self, ciphertext) :
		return self.rsa.decrypt(ciphertext)[-1] & 1

if __name__ == '__main__' :
	plaintext = b''
	with open('46.txt', 'r') as file :
		plaintext = b64decode(file.read())

	int_plain = int.from_bytes(plaintext, 'big')
	oracle = rsaOracle()
	e, n = oracle.get_public_key()
	ciphertext = modexp(int.from_bytes(plaintext, 'big'), e, n)

	lo, hi = 0, n
	while lo < hi :
		mid = (lo + hi) // 2
		ciphertext = (modexp(2, e, n)*ciphertext)%n
		bytes_ciphertext = ciphertext.to_bytes((ciphertext.bit_length() + 7)\
		//8, 'big')
		if oracle.get_parity(bytes_ciphertext) :
			lo = mid + 1
		else :
			hi = mid

	print(lo.to_bytes((lo.bit_length() + 7)//8, 'big'))
	print(plaintext)
