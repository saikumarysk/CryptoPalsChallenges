from cbcMac import cbcmac, xor

def attack() :
	key = b'YELLOW SUBMARINE'
	s1 = b"alert('MZA who was that?');\n"
	target_hash = cbcmac(s1, b'\x00'*16, key)

	s2 = b"alert('Ayo, the Wu is back!');//"
	intermediate_hash = cbcmac(s2, b'\x00'*16, key)

	block0 = b'\x10'*16
	block1 = xor(intermediate_hash, s1[:16])
	block2 = s1[16:]
	valid_snippet = s2 + block0 + block1 + block2
	collision_hash = cbcmac(valid_snippet, b'\x00'*16, key)

	print('Are they same?', collision_hash == target_hash)

if __name__ == '__main__' :
	attack()
