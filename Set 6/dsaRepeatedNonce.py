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
A = int('2d026f4bf30195ede3a088da85e398ef869611d0f68f0713d51c9c1a3a26c95105d915e2d8cdf26d056b86b8a7b85519b1c23cc3ecdc6062650462e3063bd179c2a6581519f674a61f1d89a1fff27171ebc1b93d4dc57bceb7ae2430f98a6a4d83d8279ee65d71c1203d2c96d65ebbf7cce9d32971c3de5084cce04a2e147821', 16)

def get_k_from_sigs(sig1, sig2) :
	return ((sig1[3] - sig2[3]) * modinv(sig1[1] - sig2[1], q)) % q

def attack(sigs) :
	d = {}
	k = []
	signature = []
	for sig in sigs :
		if sig[2] not in d :
			d[sig[2]] = sig
		else :
			k.append(get_k_from_sigs(sig, d[sig[2]]))
			signature.append(sig)

	a = 0
	for i in range(len(k)) :
		a1 = ((((k[i]*signature[i][1])%q) - signature[i][3]) * modinv(signature[i][2], q)) % q
		if modexp(g, a1, p) == A : a = a1

	return a

if __name__ == '__main__' :
	lines = []
	with open('44.txt', 'r') as file :
		lines = file.read().splitlines()

	inputs = [lines[i: i+4] for i in range(0, len(lines), 4)]
	sigs = []
	for M, s, r, h in inputs :
		M += ''
		M = M[5:]
		s = int(s[3:])
		r = int(r[3:])
		h = int(h[3:], 16)
		sigs.append((M+' ', s, r, h))

	a = attack(sigs)
	print('Retrieved a -', a)
	print("Original a's sha1 fingerprint - ca8f6f7c66fa362d40760d135b763eb8527d3d52")
	hash = sha1(hex(a)[2:].encode())
	print("Retrieved a's sha1 fingerprint -", hash)
	print('Are they same -', hash == 'ca8f6f7c66fa362d40760d135b763eb8527d3d52')
