from Crypto.Cipher import ARC4
from operator import itemgetter
from base64 import b64decode

def random_bytes(n: int) -> str :
	output = b''
	for _ in range(n) :
		output += bytes([randint(0, 255)])

	return output

def keygen() :
	return random_bytes(16)

def oracle(req) :
	cookie = b64decode('QkUgU1VSRSBUTyBEUklOSyBZT1VSIE9WQUxUSU5F')
	key = keygen()

	cipher = ARC4.new(key)
	return cipher.encrypt(req+cookie)

if __name__ == '__main__' :
	cookie_len = len(oracle(b''))
	z16, z32 = 15, 31
	z16_bias, z32_bias = 0xf0, 0xe0
	plaintext = ['?']*cookie_len

	for i in range((cookie_len // 2) + 1) :
		offset = z16 - i
		request = b'A'*offset

		z16_map, z32_map = {}, {}
		check_z32 = z32 < (len(request) + cookie_len)

		for j in range(1<<24) :
			result = oracle(request)

			try :
				z16_map[result[z16]] += 1
			except KeyError :
				z16_map[result[z16]] = 1

			if check_z32 :
				try :
					z32_map[result[z32]] += 1
				except KeyError :
					z32_map[result[z32]] = 1

		z16_char = max(z16_map.items(), key=itemgetter(1))[0]
		plaintext[z16 - offset] = chr(ord(z16_char)^z16_bias)

		if check_z32 :
			z32_char = max(z32_map.items(), key=itemgetter(1))[0]
			plaintext[z32 - offset] = chr(ord(z32_char)^z32_bias)

		#print(''.join(plaintext))

	return ''.join(plaintext)
