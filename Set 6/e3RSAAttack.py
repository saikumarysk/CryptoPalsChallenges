from rsa import RSA
from sha1MAC import sha1
import re

ASN1_SHA1 = b'\x30\x21\x30\x09\x06\x05\x2b\x0e\x03\x02\x1a\x05\x00\x04\x14'

def int_cube_root(n: int) -> int :
	lo, hi = 0, n
	while lo < hi :
		mid = (lo + hi)//2
		if mid**3 < n :
			lo = mid + 1
		else :
			hi = mid

	return lo

class RSA_Verifier() :
	def __init__(self, keylen) :
		self.rsa = RSA(keylen)

	def verify(self, signature, message) :
		signature = b'\x00' + self.rsa.encrypt(signature)

		r = re.compile(b'\x00\x01\xff+?\x00.{15}(.{20})', re.DOTALL)
		m = r.match(signature)
		if not m :
			print('Signature format wrong')
			return

		hash = m.group(1)
		if hash == bytes.fromhex(sha1(message)) :
			print('Signatures matched')
		else :
			print('Signatures did not match')

def attack(message, keylen) :
	block = b'\x00\x01\xff\x00' + ASN1_SHA1 + bytes.fromhex(sha1(message))
	block += b'\x00' * (((keylen + 7) // 8) - len(block))

	sig = int.from_bytes(block, 'big')
	forged_sig = int_cube_root(sig)
	forged_sig = forged_sig.to_bytes((forged_sig.bit_length() + 7) // 8, 'big')
	print('Forged signature -', forged_sig)
	RSA_Verifier(keylen).verify(forged_sig, message)


if __name__ == '__main__' :
	message = b'hi mom'
	attack(message, 1024) # Higher value is better as the message length is also high
