from sha1MAC import sha1
from random import randint

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

def modexp(b, e, m) :
	x = 1
	while e > 0 :
		b, e, x = (b*b) % m, e//2, (b*x)%m if e & 1 else x

	return x


p = int('800000000000000089e1855218a0e7dac38136ffafa72eda7859f2171e25e65eac698c1702578b07dc2a1076da241c76c62d374d8389ea5aeffd3226a0530cc565f3bf6b50929139ebeac04f48c3c84afb796d61e5a4f9a8fda812ab59494232c7d2b4deb50aa18ee9e132bfa85ac4374d7f9091abc3d015efc871a584471bb1', 16)
q = int('f4f47f05794b256174bba6e9b396a7707e563c5b', 16)
g = int('5958c9d3898b224b12672c0b98e06c60df923cb8bc999d119458fef538b8fa4046c8db53039db620c094c9fa077ef389b5322a559946a71903f990f1f7e0e025e2d7f7cf494aff1a0470f5b64c36b625a097f1651fe775323556fe00b3608c887892878480e99041be601a62166ca6894bdd41a7054ec89f756ba9fc95302291', 16)

def dsa_sign(p, q, g, a, M) :
	r, s = 0, 0
	while s == 0 :
		r, k = 0, randint(1, q-1)
		while r == 0 :
			X = modexp(g, k, p)
			r = X % q

		k_inverse = modinv(k, q)
		h = sha1(M)
		h = int(h, 16) % q
		s = (k_inverse * ((h + a*r) % q)) % q
	return r, s

def dsa_verify(p, q, g, A, M, r, s) :
	if r not in range(1, q) or s not in range(1, q) : return 'Reject'

	w = modinv(s, q)
	h = sha1(M)
	h = int(h, 16) % q
	u1, u2 = (h*w) % q, (r*w) % q
	X = (modexp(g, u1, p) * modexp(A, u2, p)) % p
	v = X % q
	if v == r : return 'Accept'
	return 'Reject'

def diffie_hellman(p, g) :
	a = randint(1, p-1)
	A = modexp(g, a, p)
	return (a, A)

def find_a(p, q, g, A, M, r, s) :
	print(sha1(M))
	h = int(sha1(M), 16) % q
	r_inverse = modinv(r, q)
	s = s%q
	for k in range((1 << 16) + 1) :
		a = (((k*s) - h) * r_inverse) % q
		if A == modexp(g, a, p) :
			return a

if __name__ == '__main__' :
	'''a, A = diffie_hellman(p, g)
	M = b'Trap Nation'
	r, s = dsa_sign(p, q, g, a, M)

	print(dsa_verify(p, q, g, A, M, r, s))'''

	A = int('84ad4719d044495496a3201c8ff484feb45b962e7302e56a392aee4abab3e4bdebf2955b4736012f21a08084056b19bcd7fee56048e004e44984e2f411788efdc837a0d2e5abb7b555039fd243ac01f0fb2ed1dec568280ce678e931868d23eb095fde9d3779191b8c0299d6e07bbb283e6633451e535c45513b2d33c99ea17', 16)
	M = b'For those that envy a MC it can be hazardous to your health\nSo be friendly, a matter of life and death, just like a etch-a-sketch\n'
	r, s = 548099063082341131477253921760299949438196259240, 857042759984254168557880549501802188789837994940
	a = find_a(p, q, g, A, M, r, s)
	print('a is -', a)
	print('For the real a, the sha1 fingerprint is - 0954edd5e0afe5542a4adf012611a91912a3ec16')
	h = sha1(hex(a)[2:].encode())
	print('Sha1 for this a -', h)
	print('Is sha1 fingerprint the same -', h == '0954edd5e0afe5542a4adf012611a91912a3ec16')
