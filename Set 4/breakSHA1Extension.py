import struct
import sha1MAC
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

	while ((len(text)*8) % 512) != 448 :
		text += b'\x00'

	text += struct.pack('>Q', m1)
	return text

def split_five_words(digest: str) -> tuple :
	digest = int(digest, 16)
	a = digest >> 128
	b = ( digest >> 96 ) & 0xFFFFFFFF
	c = ( digest >> 64 ) & 0xFFFFFFFF
	d = ( digest >> 32 ) & 0xFFFFFFFF
	e = digest & 0xFFFFFFFF

	return a, b, c, d, e

def validate(text: str, digest: str) -> bool :
	return sha1MAC.sha1_mac(KEY, text) == digest

def forge(text: str, digest: str, keylen: int, new_text: str) -> tuple :
	forged_text = md_padding(b'A'*keylen + text) + new_text
	forged_text = forged_text[keylen:]

	a, b, c, d, e = split_five_words(digest)
	forged_digest = sha1MAC.sha1(new_text, (keylen + len(forged_text))*8,\
	 a, b, c, d, e)

	return forged_text, forged_digest

def attack() :
	text = b'comment1=cooking%20MCs;userdata=foo;comment2=%20like%20a%20pound%20of%20bacon'
	digest = sha1MAC.sha1_mac(KEY, text)
	print(text, digest)

	i = 0
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
