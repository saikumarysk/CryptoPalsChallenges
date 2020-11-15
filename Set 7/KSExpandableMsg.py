from Crypto.Cipher import AES
from multiCollisionHash import mdhash

def pad(input: str, block_length: int) -> str :
	rem = len(input)%block_length
	if rem :
		input += chr(block_length - rem)*(block_length - rem)

	return input

def random_bytes(n: int) -> str :
	output = b''
	for _ in range(n) :
		output += bytes([randint(0, 255)])

	return output

def keygen() :
	return random_bytes(16)

def generate_messages(k) :
	h = b'\x00\x00'
	start_size = len(h)
	collisions = []

	while k > 0 :
		d = {}
		prefix = b'\x00' * 16 * (1 << (k-1))
		pre_hash = mdhash(prefix, h)

		for _ in range(1<<(start_size*8)) :
			m = random_bytes(start_size)
			d[mdhash(m, h)] = m

		m = random_bytes(start_size)
		hashed = mdhash(m, pre_hash)
		while hashed not in d :
			m = random_bytes(start_size)
			hashed = mdhash(m, pre_hash)

		collisions.append((prefix + m, d[hashed]))

		k -= 1
		h = hashed

	return collisions, hashed

def block_map(M) :
	index = {}
	h = b'\x00\x00'
	M = pad(M)

	for i in range(len(M)//16) :
		block = M[i*16:(i*16 + 16)]
		hashed = mdhash(block, h)
		index[hashed] = i
		h = hashed

	return index

def generate_prefix(l, pairs) :
	l *= 16
	prefix = b''

	for long, short in pairs :
		segment = long if l > len(long) else short
		segment = pad(segment)
		prefix += segment
		l -= len(segment)

		if l == 0 : return prefix

def attack() :
	k = 16
	M = random_bytes(1 << (k+4))
	intermediate_hashes = block_map(M)

	collision_pairs, final_state = generate_messages(k)
	while final_state not in intermediate_hashes :
		collision_pairs, final_state = generate_messages

	bridge_index = intermediate_hashes[final_state] + 1
	bridge_offset = bridge_index*16
	print('Index of bridge block -', bridge_index, ',offset is -', bridge_offset)

	prefix = generate_prefix(bridge_index, collision_pairs)
	print('Length of prefix -', len(prefix))
	print('Length of bridge index -', bridge_index*16)

	preimage = prefix + M[bridge_offset:]
	print('Length of preimage and M -', len(preimage), len(M))
	print('mdhashes are -')
	print('Preimage -', mdhash(preimage, b'\x00\x00'))
	print('M -', mdhash(M, b'\x00\x00'))
