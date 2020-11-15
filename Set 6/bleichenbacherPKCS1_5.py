from rsa import RSA
from random import randint

def ceil(a, b) :
	return (a+b-1)//b

def random_bytes(n: int) -> str :
	output = b''
	for _ in range(n) :
		output += bytes([randint(0, 255)])

	return output

def pkcs1_5Pad(input, length) :
	return b'\x00\x02' + random_bytes(length - 3 - len(input)) + b'\x00' + input

def is_padding_correct(ciphertext, cipher) :
	plaintext = b'\x00' + cipher.decrypt(ciphertext)
	return len(plaintext) == ceil(cipher.n.bit_length(), 8) and \
	 plaintext[:2] == b'\x00\x02'

def appendAndMerge(intervals, l, h) :
	for i, (a, b) in enumerate(intevals) :
		if b >= l and a <= h :
			a_new = min(l, a)
			b_new = max(h, b)
			intervals[i] = (a_new, b_new)
			return

	intervals.append((a_new, b_new))

def attack(c, cipher, keyByteLen) :
	B = 1 << (8*(keyByteLen - 2))
	n, e = cipher.n, cipher.e

	c_0 = c
	M = [(2*B, 3*B - 1)]
	i = 1

	while True :
		if i == 1 :
			s = ceil(cipher.n, 3*B)
			while True :
				c = (c_0*(power(s, e, n))) % n
				if is_padding_correct(c, cipher) : break
				s += 1
		elif len(M) >= 2 :
			while True :
				s += 1
				c = (c_0*(power(s, e, n))) % n
				if is_padding_correct(c, cipher) : break
		elif len(M) == 1 :
			a, b = M[0]
			if a == b : return b'\x00' + \
			 a.to_bytes((a.bit_length() + 7) // 8, 'big')

			r, s = ceil(2*(b*s - 2*B)), n, ceil(2*B+r*n, b)

			while True :
				c = (c_0*(power(s, e, n))) % n
				if is_padding_correct(c, cipher) : break
				s += 1
				if s > (3*B + r*n)//a :
					r += 1
					s = ceil((2*B+r*n), b)

		M_new = []
		for (a, b) in M :
			min_r = ceil(a*s - 3*B + 1, n)
			max_r = (b*s - 2*B)//n

			for r in range(min_r, max_r + 1) :
				l, u = max(a, ceil(2*B + r*n, s)), min(b, (3*B - 1 + r*n)//s)

				if l > u :
					print('Something Wrong')
					return
				appendAndMerge(M_new, l, u)

		if len(M_new) == 0 :
			print('Something Wrong!!')
			return

		M = M_new
		i += 1

if __name__ == '__main__' :
	plaintext = b'howdy!'
	print('Plaintext -', plaintext)
	m = pkcs1_5Pad(plaintext, 32)
	print('m -', m)
	cipher = RSA(256)
	c = cipher.encrypt(m)
	print('c -', c)

	print('Does c have the right padding -', is_padding_correct(c, cipher))

	decrypted_plaintext = attack(c, cipher, 32)
	print('Decrypted Plaintext -', decrypted_plaintext)
	print('Are they same? ', plaintext == decrypted_plaintext)
