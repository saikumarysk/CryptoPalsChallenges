import hashlib
from struct import pack, unpack

def random_bytes(n: int) -> str :
	output = b''
	for _ in range(n) :
		output += bytes([randint(0, 255)])

	return output

def keygen() :
	return random_bytes(16)

def lrot(x, n) :
	mask = (1 << n) - 1
	rotated = (x << n) | ((x >> (32 - n)) & mask)
	return rotated & 0xFFFFFFFF

def rrot(x, n) :
	rotated = (x >> n) | (x << (32 - n))
	return rotated & 0xFFFFFFFF

def f(x, y, z) :
	return (x & y) | (~x & z)

def g(x, y, z) :
	return (x & y) | (y & z) | (z & x)

def phi0(a, b, c, d, mk, s) :
	return lrot((a + f(b, c, d) + mk) & 0xFFFFFFFF, s)

def phi1(a, b, c, d, mk, s) :
	return lrot((a + f(b, c, d) + mk + 0x5A827999) & 0xFFFFFFFF, s)

def phi0_reverse(modified, a, b, c, d, s) :
	return (rrot(modified, s) - a - f(b, c, d)) & 0xFFFFFFFF

def phi1_reverse(modified, a, b, c, d, s) :
	return (rrot(modified, s) - a - g(b, c, d) - 0x5A827999) & 0xFFFFFFFF

def equal_bit(x, y, i) :
	xi, yi = (x >> (i-1)) & 1, (y >> (i-1)) & 1
	return x ^ ((xi ^ yi) << (i-1))

def clear_bit(x, i) :
	return x ^ (((x >> (i-1)) & 1) << (i-1))

def set_bit(x, i) :
	return x | (1 << (i-1))

def parse_message(M) :
	blocks = []
	for i in range(0, 64, 4) :
		(block, ) = unpack('<L', M[i:i+4])
		blocks.append(block)
	return blocks

def form_message(blocks) :
	s = b''
	for block in blocks :
		s += pack('<L', block)
	return s

def massage_message(M, a0, b0, c0, d0) :
	m = parse_message(M)

	a1 = phi0(a0, b0, c0, d0, m[0], 3)
	a1 = equal_bit(a1, b0, 7)
	m[0] = phi0_reverse(a1, a0, b0, c0, d0, 3)

	d1 = phi0(d0, a1, b0, c0, m[1], 7)
	d1 = clear_bit(d1, 7)
	d1 = equal_bit(d1, a1, 8)
	d1 = equal_bit(d1, a1, 11)
	m[1] = phi0_reverse(d1, d0, a1, b0, c0, 7)

	c1 = phi0(c0, d1, a1, b0, m[2], 11)
	c1 = set_bit(c1, 7)
	c1 = set_bit(c1, 8)
	c1 = clear_bit(c1, 11)
	c1 = equal_bit(c1, d1, 26)
	m[2] = phi0_reverse(c1, c0, d1, a1, b0, 11)

	b1 = phi0(b0, c1,d1, a1, m[3], 19)
	b1 = set_bit(b1, 7)
	b1 = clear_bit(b1, 8)
	b1 = clear_bit(b1, 11)
	b1 = clear_bit(b1, 26)
	m[3] = phi0_reverse(b1, b0, c1, d1, a1, 19)

	a2 = phi0(a1, b1, c1, d1, m[4], 3)
	a2 = set_bit(a2, 8)
	a2 = set_bit(a2, 11)
	a2 = clear_bit(a2, 26)
	a2 = equal_bit(a2, b1, 14)
	m[4] = phi0_reverse(a2, a1, b1, c1, d1, 3)

	d2 = phi0(d1, a2, b1, c1, m[5], 7)
	d2 = clear_bit(d2, 14)
	d2 = equal_bit(d2, a2, 19)
	d2 = equal_bit(d2, a2, 20)
	d2 = equal_bit(d2, a2, 21)
	d2 = equal_bit(d2, a2, 22)
	d2 = set_bit(d2, 26)
	m[5] = phi0_reverse(d2, d1, a2, b1, c1, 7)

	c2 = phi0(c1, d2, a2, b1, m[6], 11)
	c2 = equal_bit(c2, d2, 13)
	c2 = clear_bit(c2, 14)
	c2 = equal_bit(c2, d2, 15)
	c2 = clear_bit(c2, 19)
	c2 = clear_bit(c2, 20)
	c2 = set_bit(c2, 21)
	c2 = clear_bit(c2, 22)
	m[6] = phi0_reverse(c2, c1, d2, a2, b1, 11)

	b2 = phi0(b1, c2, d2, a2, m[7], 19)
	b2 = set_bit(b2, 13)
	b2 = set_bit(b2, 14)
	b2 = clear_bit(b2, 15)
	b2 = equal_bit(b2, c2, 17)
	b2 = clear_bit(b2, 19)
	b2 = clear_bit(b2, 20)
	b2 = clear_bit(b2, 21)
	b2 = clear_bit(b2, 22)
	m[7] = phi0_reverse(b2, b1, c2, d2, a2, 19)

	a3 = phi0(a2, b2, c2, d2, m[8], 3)
	a3 = set_bit(a3, 13)
	a3 = set_bit(a3, 14)
	a3 = set_bit(a3, 15)
	a3 = clear_bit(a3, 17)
	a3 = clear_bit(a3, 19)
	a3 = clear_bit(a3, 20)
	a3 = clear_bit(a3, 21)
	a3 = equal_bit(a3, b2, 23)
	a3 = set_bit(a3, 22)
	a3 = equal_bit(a3, b2, 26)
	m[8] = phi0_reverse(a3, a2, b2, c2, d2, 3)

	d3 = phi0(d2, a3, b2, c2, m[9], 7)
	d3 = set_bit(d3, 13)
	d3 = set_bit(d3, 14)
	d3 = set_bit(d3, 15)
	d3 = clear_bit(d3, 17)
	d3 = clear_bit(d3, 20)
	d3 = set_bit(d3, 21)
	d3 = set_bit(d3, 22)
	d3 = clear_bit(d3, 23)
	d3 = set_bit(d3, 26)
	d3 = equal_bit(d3, a3, 30)
	m[9] = phi0_reverse(d3, d2, a3, b2, c2, 7)

	c3 = phi0(c2, d3, a3, b2, m[10], 11)
	c3 = set_bit(c3, 17)
	c3 = clear_bit(c3, 20)
	c3 = clear_bit(c3, 21)
	c3 = clear_bit(c3, 22)
	c3 = clear_bit(c3, 23)
	c3 = clear_bit(c3, 26)
	c3 = set_bit(c3, 30)
	c3 = equal_bit(c3, d3, 32)
	m[10] = phi0_reverse(c3, c2, d3, a3, b2, 11)

	b3 = phi0(b2, c3, d3, a3, m[11], 19)
	b3 = clear_bit(b3, 20)
	b3 = set_bit(b3, 21)
	b3 = set_bit(b3, 22)
	b3 = equal_bit(b3, c3, 23)
	b3 = set_bit(b3, 26)
	b3 = clear_bit(b3, 30)
	b3 = clear_bit(b3, 32)
	m[11] = phi0_reverse(b3, b2, c3, d3, a3, 19)

	a4 = phi0(a3, b3, c3, d3, m[12], 3)
	a4 = clear_bit(a4, 23)
	a4 = clear_bit(a4, 26)
	a4 = equal_bit(a4, b3, 27)
	a4 = equal_bit(a4, b3, 29)
	a4 = set_bit(a4, 30)
	a4 = clear_bit(a4, 32)
	m[12] = phi0_reverse(a4, a3, b3, c3, d3, 3)

	d4 = phi0(d3, a4, b3, c3, m[13], 7)
	d4 = clear_bit(d4, 23)
	d4 = clear_bit(d4, 26)
	d4 = set_bit(d4, 27)
	d4 = set_bit(d4, 29)
	d4 = clear_bit(d4, 30)
	d4 = set_bit(d4, 32)
	m[13] = phi0_reverse(d4, d3, a4, b3, c3, 7)

	c4 = phi0(c3, d4, a4, b3, m[14], 11)
	c4 = equal_bit(c4, d4, 19)
	c4 = set_bit(c4, 23)
	c4 = set_bit(c4, 26)
	c4 = clear_bit(c4, 27)
	c4 = clear_bit(c4, 29)
	c4 = clear_bit(c4, 30)
	m[14] = phi0_reverse(c4, c3, d4, a4, b3, 11)

	b4 = phi0(b3, c4, d4, a4, m[15], 19)
	b4 = clear_bit(b4, 19)
	b4 = set_bit(b4, 26)
	b4 = set_bit(b4, 27)
	b4 = set_bit(b4, 29)
	b4 = clear_bit(b4, 30)
	m[15] = phi0_reverse(b4, b3, c4, d4, a4, 19)

	a5 = phi1(a4, b4, c4, d4, m[0], 3)
	a5 = equal_bit(a5, c4, 19)
	a5 = set_bit(a5, 26)
	a5 = clear_bit(a5, 27)
	a5 = set_bit(a5, 29)
	a5 = set_bit(a5, 32)
	m[0] = phi1_reverse(a5, a4, b4, c4, d4, 3)
	a1 = phi0(a0, b0, c0, d0, m[0], 3)
	m[1] = phi0_reverse(d1, d0, a1, b0, c0, 7)
	m[2] = phi0_reverse(c1, c0, d1, a1, b0, 11)
	m[3] = phi0_reverse(b1, b0, c1, d1, a1, 19)
	m[4] = phi0_reverse(a2, a1, b1, c1, d1, 3)

	d5 = phi1(d4, a5, b4, c4, m[4], 5)
	d5 = equal_bit(d5, a5, 19)
	d5 = equal_bit(d5, b4, 26)
	d5 = equal_bit(d5, b4, 27)
	d5 = equal_bit(d5, b4, 29)
	d5 = equal_bit(d5, b4, 32)
	m[4] = phi1_reverse(d5, d4, a5, b4, c4, 5)
	a2_ = phi0(a1, b1, c1, d1, m[4], 3)
	m[5] = phi0_reverse(d2, d1, a2_, b1, c1, 7)
	m[6] = phi0_reverse(c2, c1, d2, a2_, b1, 11)
	m[7] = phi0_reverse(b2, b1, c2, d2, a2_, 19)
	m[8] = phi0_reverse(a3, a2_, b2, c2, d2, 3)

	return m

def check_conditions(m, a, b, c, d) :
	def set(x, i) :
		assert ((x >> (i-1)) & 1) == 1

	def clear(x, i) :
		assert ((x >> (i-1)) & 1) == 0

	def eq(x, y, i) :
		assert ((x >> (i-1)) & 1) == ((y >> (i-1)) & 1)

	a = phi0(a, b, c, d, m[0], 3)
	eq(a, b, 7)
	d = phi0(d, a, b, c, m[1], 7)
	clr(d, 7)
	eq(d, a, 8)
	eq(d, a, 11)
	c = phi0(c, d, a, b, m[2], 11)
	set(c, 7)
	set(c, 8)
	clr(c, 11)
	eq(c, d, 26)
	b = phi0(b, c, d, a, m[3], 19)
	set(b, 7)
	clr(b, 8)
	clr(b, 11)
	clr(b, 26)

	a = phi0(a, b, c, d, m[4], 3)
	set(a, 8)
	set(a, 11)
	clr(a, 26)
	eq(a, b, 14)
	d = phi0(d, a, b, c, m[5], 7)
	clr(d, 14)
	eq(d, a, 19)
	eq(d, a, 20)
	eq(d, a, 21)
	eq(d, a, 22)
	set(d, 26)
	c = phi0(c, d, a, b, m[6], 11)
	eq(c, d, 13)
	clr(c, 14)
	eq(c, d, 15)
	clr(c, 19)
	clr(c, 20)
	set(c, 21)
	clr(c, 22)
	b = phi0(b, c, d, a, m[7], 19)
	set(b, 13)
	set(b, 14)
	clr(b, 15)
	eq(b, c, 17)
	clr(b, 19)
	clr(b, 20)
	clr(b, 21)
	clr(b, 22)

	a = phi0(a, b, c, d, m[8], 3)
	set(a, 13)
	set(a, 14)
	set(a, 15)
	clr(a, 17)
	clr(a, 19)
	clr(a, 20)
	clr(a, 21)
	eq(a, b, 23)
	set(a, 22)
	eq(a, b, 26)
	d = phi0(d, a, b, c, m[9], 7)
	set(d, 13)
	set(d, 14)
	set(d, 15)
	clr(d, 17)
	clr(d, 20)
	set(d, 21)
	set(d, 22)
	clr(d, 23)
	set(d, 26)
	eq(d, a, 30)
	c = phi0(c, d, a, b, m[10], 11)
	set(c, 17)
	clr(c, 20)
	clr(c, 21)
	clr(c, 22)
	clr(c, 23)
	clr(c, 26)
	set(c, 30)
	eq(c, d, 32)
	b = phi0(b, c, d, a, m[11], 19)
	clr(b, 20)
	set(b, 21)
	set(b, 22)
	eq(b, c, 23)
	set(b, 26)
	clr(b, 30)
	clr(b, 32)

	a = phi0(a, b, c, d, m[12], 3)
	clr(a, 23)
	clr(a, 26)
	eq(a, b, 27)
	eq(a, b, 29)
	set(a, 30)
	clr(a, 32)
	d = phi0(d, a, b, c, m[13], 7)
	clr(d, 23)
	clr(d, 26)
	set(d, 27)
	set(d, 29)
	clr(d, 30)
	set(d, 32)
	c = phi0(c, d, a, b, m[14], 11)
	eq(c, d, 19)
	set(c, 23)
	set(c, 26)
	clr(c, 27)
	clr(c, 29)
	clr(c, 30)
	b = phi0(b, c, d, a, m[15], 19)
	clr(b, 19)
	set(b, 26)
	eq(b, c, 26)
	set(b, 27)
	set(b, 29)
	clr(b, 30)

	a = phi1(a, b, c, d, m[0], 3)
	eq(a, c, 19)
	set(a, 26)
	clr(a, 27)
	set(a, 29)
	set(a, 32)
	d = phi1(d, a, b, c, m[4], 5)
	eq(d, a, 19)
	eq(d, b, 26)
	eq(d, b, 27)
	eq(d, b, 29)
	eq(d, b, 32)
	c = phi1(c, d, a, b, m[8], 9)
	b = phi1(b, c, d, a, m[12], 13)

def md4_hash(m) :
	return hashlib.new('md4', m).digest()

def format_msg(M) :
	return ' '.join(['{:x}'.format(b) for b in unpack('<LLLLLLLLLLLLLLLL', M)])

if __name__ == '__main__' :
	collision = False
	a0, b0, c0, d0 = 0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476

	i = 0
	M, M_ = None, None
	while not collision :
		i += 1

		M = random_bytes(64)
		m = massage_message(M, a0, b0, c0, d0)

		m_ = m[:]
		m_[1] = (m[1] + (1 << 31)) & 0xFFFFFFFF
		m_[2] = (m[2] + ((1 << 31) - (1 << 28))) & 0xFFFFFFFF
		m_[12] = (m[12] - (1 << 16)) & 0xFFFFFFFF

		M = form_message(m)
		M_ = form_message(m_)

		collision = md4_hash(M) = md4_hash(M_)

	print('Found a collison for -', M)
	print('New string is -', M_)
	print('MD4 hash is -', md4_hash(M))
