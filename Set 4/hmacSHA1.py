import sha1MAC

def xor(s1: str, s2: str) :
	output = b''
	for c1, c2 in zip(s1, s2) :
		output += bytes([c1 ^ c2])

	return output

def hmac_sha1(key, text) :
	block_size = 64
	output_size = 20

	if len(key) > block_size :
		key = sha1MAC.sha1(key)

	while len(key) < block_size :
		key += b'\x00'

	outer_key_pad = xor(key, b'\x5c'*64)
	inner_key_pad = xor(key, b'\x36'*64)

	return sha1MAC.sha1(outer_key_pad + bytes.fromhex(sha1MAC.sha1(inner_key_pad + text)))

if __name__ == '__main__' :
	key = b'\xc8\x82I\xde}3\xf7\x13\xaf#\xc4\x80\x90\xfb\xf0\xb6'
	text = b''
	with open('Lorem.txt', 'r') as file :
		text = bytes(file.read(), 'utf-8')

	from hashlib import sha1
	import hmac
	hmack = hmac_sha1(key, text)
	print('My implementation -', hmack)
	official = hmac.new(key, text, sha1)
	print('Official -', official.digest().hex())
	print('Are they same -', hmack == official.digest().hex())
