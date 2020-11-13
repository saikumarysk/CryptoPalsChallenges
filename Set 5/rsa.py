from Crypto.Util.number import getPrime

class RSA(object) :

	def __init__(self, keylen) :
		self.e = 3
		phi = 0
		while self.extended_gcd(self.e, phi)[0] != 1 :
			p, q = getPrime(keylen//2), getPrime(keylen//2)
			self.n = p*q
			phi = self.lcm(p-1, q-1)

		self.d = self.modinv(self.e, phi)

		self.public = (self.e, self.n)
		self.private = (self.d, self.n)

	def get_public_key(self) :
		return self.public

	def encrypt(self, text, public=None) :
		if not public : public = self.public
		m = int.from_bytes(text, 'big')
		c = self.modexp(m, public[0], public[1])
		return c.to_bytes((c.bit_length() + 7) // 8, 'big')

	def decrypt(self, text) :
		c = int.from_bytes(text, 'big')
		m = self.modexp(c, self.private[0], self.private[1])
		return m.to_bytes((m.bit_length() + 7) // 8, 'big')

	def extended_gcd(self, a, m) :
		last_r, r = a, m
		x, last_x, y, last_y = 0, 1, 1, 0

		while r :
			last_r, (q, r) = r, divmod(last_r, r)
			x, last_x =  last_x - q*x, x
			y, last_y =  last_y - q*y, y

		return last_r, last_x*(-1 if a < 0 else 1), last_y*(-1 if m < 0 else 1)

	def lcm(self, a, b) :
		g, x, y = self.extended_gcd(a, b)
		return (a*b) // g

	def modinv(self, a, m) :
		g, x, y = self.extended_gcd(a, m)
		if g != 1 : raise ValueError
		return x % m

	def modexp(self, b, e, m) :
		x = 1
		while e > 0 :
			b, e, x = (b*b) % m, e//2, (b*x)%m if e & 1 else x

		return x

if __name__ == '__main__' :
	rsa = RSA(108)
	print(rsa.get_public_key())
	print(rsa.private)
	plaintext = b'test'
	print('Plaintext -', plaintext)
	ciphertext = rsa.encrypt(plaintext, rsa.get_public_key())
	print('Ciphertext -', ciphertext)
	decrypted_plaintext = rsa.decrypt(ciphertext)
	print('Decrypted Plaintext -', decrypted_plaintext)
