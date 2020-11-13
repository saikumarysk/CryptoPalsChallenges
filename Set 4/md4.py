import struct
from binascii import hexlify, unhexlify
from random import randint

def random_bytes(n: int) :
	output = b''
	for _ in range(n) :
		output += bytes([randint(0, 255)])

	return output

KEY = random_bytes(randint(1, 100))

def md_padding(text: str) -> str :
	m1 = len(text)*8

	text += b'\x80'
	text += bytes((56 - len(text)%64) % 64)
	text += struct.pack('<Q', m1)

	return text

class MD4(object) :

	def __init__(self, text, m1=None, A=0x67452301, B=0xefcdab89, C=0x98badcfe,\
	 D=0x10325476) :
		self.A, self.B, self.C, self.D = A, B, C, D
		if not m1 :
			m1 = len(text)*8

		while len(text) > 64 :
			self.handle(text[:64])
			text = text[64:]

		text += b'\x80'
		text += bytes((56 - len(text)%64) % 64)
		text += struct.pack('<Q', m1)

		while len(text) :
			self.handle(text[:64])
			text = text[64:]

	def handle(self, chunk) :
		X = list(struct.unpack('<' + 'I'*16, chunk))
		A, B, C, D = self.A, self.B, self.C, self.D

		for i in range(16) :
			k = i
			if (i % 4) == 0 :
				A = self.leftrotate((A + self.F(B, C, D) + X[k]) & 0xFFFFFFFF,\
				 3)
			elif (i % 4) == 1 :
				D = self.leftrotate((D + self.F(A, B, C) + X[k]) & 0xFFFFFFFF,\
				 7)
			elif (i % 4) == 2 :
				C = self.leftrotate((C + self.F(D, A, B) + X[k]) & 0xFFFFFFFF,\
				 11)
			elif (i % 4) == 3 :
				B = self.leftrotate((B + self.F(C, D, A) + X[k]) & 0xFFFFFFFF,\
				 19)

		for i in range(16) :
			k = (i//4) + (i % 4)*4
			if (i % 4) == 0 :
				A = self.leftrotate((A + self.G(B, C, D) + X[k] + 0x5A827999)\
				 & 0xFFFFFFFF, 3)
			elif (i % 4) == 1 :
				D = self.leftrotate((D + self.G(A, B, C) + X[k] + 0x5A827999)\
				 & 0xFFFFFFFF, 5)
			elif (i % 4) == 2 :
				C = self.leftrotate((C + self.G(D, A, B) + X[k] + 0x5A827999)\
				 & 0xFFFFFFFF, 9)
			elif (i % 4) == 3 :
				B = self.leftrotate((B + self.G(C, D, A) + X[k] + 0x5A827999)\
				 & 0xFFFFFFFF, 13)

		order = [0, 8, 4, 12, 2, 10, 6, 14, 1, 9, 5, 13, 3, 11, 7, 15]
		for i in range(16) :
			k = order[i]
			if (i % 4) == 0 :
				A = self.leftrotate((A + self.H(B, C, D) + X[k] + 0x6ED9EBA1)\
				 & 0xFFFFFFFF, 3)
			elif (i % 4) == 1 :
				D = self.leftrotate((D + self.H(A, B, C) + X[k] + 0x6ED9EBA1)\
				 & 0xFFFFFFFF, 9)
			elif (i % 4) == 2 :
				C = self.leftrotate((C + self.H(D, A, B) + X[k] + 0x6ED9EBA1)\
				 & 0xFFFFFFFF, 11)
			elif (i % 4) == 3 :
				B = self.leftrotate((B + self.H(C, D, A) + X[k] + 0x6ED9EBA1)\
				 & 0xFFFFFFFF, 15)

		self.A = (self.A + A) & 0xFFFFFFFF
		self.B = (self.B + B) & 0xFFFFFFFF
		self.C = (self.C + C) & 0xFFFFFFFF
		self.D = (self.D + D) & 0xFFFFFFFF

	def digest(self) :
		return struct.pack('<4I', self.A, self.B, self.C, self.D)

	def hexdigest(self) :
		return hexlify(self.digest()).decode()

	def leftrotate(self, x: int, v: int) -> int :
		return ( ( (x << v) & 0xFFFFFFFF ) | ( x >> (32 - v) ) )

	def F(self, x: int, y: int, z: int) -> int :
		return ((x & y) | (~x & z))

	def G(self, x: int, y: int, z: int) -> int :
		return ((x & y) | (y & z) | (x & z))

	def H(self, x: int, y: int, z: int) -> int :
		return (x ^ y ^ z)

def validate(text: str, digest: str) -> bool :
	return MD4(KEY+text).hexdigest() == digest

def forge(text: str, digest: str, keylen: int, new_text: str) -> tuple :
	forged_text = md_padding(b'A'*keylen + text) + new_text
	forged_text = forged_text[keylen:]

	a, b, c, d = list(struct.unpack('<4I', unhexlify(digest)))
	forged_digest = MD4(new_text, (keylen + len(forged_text))*8, a, b, c, d)\
	.hexdigest()

	return forged_text, forged_digest

def attack() :
	text = b'comment1=cooking%20MCs;userdata=foo;comment2=%20like%20a%20pound%20of%20bacon'
	digest = MD4(KEY+text).hexdigest()
	print(text, digest)

	i = 1
	while i < 101 :
		forged_text, forged_digest = forge(text, digest, i, b';admin=true')
		if validate(forged_text, forged_digest) :
			print('Done!')
			print('Key length -', i)
			print('Forged text and digest -', forged_text, forged_digest)
			print('Actual key length -', len(KEY))
			break

		i += 1

	if i == 101 :
		print('Could not attack successfully!')
		print('Key length possibly higher than 100')

if __name__ == '__main__' :
	attack()
