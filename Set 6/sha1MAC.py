import hashlib
import struct

def leftrotate(x: int, v: int) -> str :
	return ( ( (x << v) & 0xFFFFFFFF ) | ( x >> (32 - v) ) )

def sha1(text, m1=None, h0=0x67452301, h1=0xEFCDAB89, h2=0x98BADCFE, h3=0x10325476,\
 h4=0xC3D2E1F0) -> str :
	if not m1 : m1 = len(text)*8
	#Pre-processing
	text += b'\x80'

	while ( (len(text)*8) % 512 ) != 448 :
		text += b'\x00'

	text += struct.pack('>Q', m1)

	chunks = [text[i:i+64] for i in range(0, len(text), 64)]
	for chunk in chunks :
		words = [chunk[i:i+4] for i in range(0, len(chunk), 4)]
		words = [int(word.hex(), 16) for word in words]
		for i in range(16, 80) :
			words.append(leftrotate(words[i-3] ^ words[i-8] ^ words[i-14] ^\
			 words[i-16], 1))

		a, b, c, d, e = h0, h1, h2, h3, h4

		for i in range(80) :
			if i in range(20) :
				f, k = d ^ (b & (c ^ d)), 0x5A827999
			elif i in range(20, 40) :
				f, k = b ^ c ^ d, 0x6ED9EBA1
			elif i in range(40, 60) :
				f, k = (b & c) | (b & d) | (c & d), 0x8F1BBCDC
			elif i in range(60, 80) :
				f, k = b ^ c ^ d, 0xCA62C1D6

			temp = (leftrotate(a, 5) + f + e + k + words[i]) & 0xFFFFFFFF
			e = d
			d = c
			c = leftrotate(b, 30)
			b = a
			a = temp

		h0, h1, h2, h3, h4 = (h0 + a) & 0xFFFFFFFF, (h1 + b) & 0xFFFFFFFF,\
		 (h2 + c) & 0xFFFFFFFF, (h3 + d) & 0xFFFFFFFF, (h4 + e) & 0xFFFFFFFF

	return '%08x%08x%08x%08x%08x' % (h0, h1, h2, h3, h4)

def sha1_mac(key: str, text: str) :
	return sha1(key + text)

if __name__ == '__main__' :
	text = b'Listen for me, you better listen for me now. '
	hash = sha1(text)
	print('My implementation -', hash)
	h = hashlib.sha1(text).hexdigest()
	print('HashLib -', h)
	print('Are they same -', hash == h)
