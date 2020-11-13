from rsa import RSA
from random import randint

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

class RSA_server() :
	def __init__(self, keylen) :
		self.rsa = RSA(keylen)
		self.received_texts = set()

	def get_public_key(self) :
		return self.rsa.get_public_key()

	def decrypt(self, text) :
		if text in self.received_texts : return None
		self.received_texts.add(text)

		return self.rsa.decrypt(text)

def attack(e, n, c) :
	s = 0
	while extended_gcd(s, n)[0] != 1 :
		s = randint(2, n-1)
	sen = modexp(s, e, n)

	c = int.from_bytes(ciphertext, 'big')
	c_1 = (sen*c)%n
	p_1 = rsa_server.decrypt(c_1.to_bytes((c_1.bit_length() + 7) // 8, 'big'))
	p_1 = int.from_bytes(p_1, 'big')
	s_1 = modinv(s, n)
	p = ( p_1 * s_1 ) % n
	return p.to_bytes((p.bit_length() + 7) // 8, 'big')

if __name__ == '__main__' :
	rsa_server = RSA_server(180)
	e, n = rsa_server.get_public_key()

	plaintext = b'This is a test'
	print(plaintext)
	ciphertext = modexp(int.from_bytes(plaintext, 'big'), e, n)
	ciphertext = ciphertext.to_bytes((ciphertext.bit_length() + 7) // 8, 'big')
	print(ciphertext)
	# Verify and add to the hashset
	rsa_server.decrypt(ciphertext)

	decrypted_plaintext = attack(e, n, ciphertext)
	print('Plaintext from attack -', decrypted_plaintext)
	print('Are they same -', plaintext == decrypted_plaintext)
