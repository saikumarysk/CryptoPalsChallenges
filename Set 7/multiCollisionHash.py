from Crypto.Cipher import AES

def pad(input: str, block_length: int) -> str :
	rem = len(input)%block_length
	if rem :
		input += chr(block_length - rem)*(block_length - rem)

	return input

def mdhash(m, h) :
	state_size = len(h)
	m = pad(m)

	for block in range(len(m)//16) :
		cipher = AES.new(pad(h), AES.MODE_ECB)
		h = cipher.encrypt(m[block*16 : block*16 + 16])[:state_size]

	return h

def find_collision(m, h) :
	d = {}
	hashed = mdhash(m, h)
	while hashed not in d :
		d[hashed] = m
		m += 1
		hashed = mdhash(m, h)

	return m.to_bytes((m.bit_length() + 7)//8, 'big'),\
	 d[hashed].to_bytes((d[hashed].bit_length() + 7)//8, 'big'), hashed

def generate_collision(n, start) :
	h = b'\x00\x00'
	collisions = []

	for i in range(n) :
		prev_collisions = collisions[:]
		s1, s2, hashed = find_collision(start, h)

		if not collisions :
			collisions = [s1, s2]
		else :
			collisions = [pad(p)+s1 for p in prev_collisions]
			collisions += [pad(p)+s2 for p in prev_collisions]

		h = hashed

	return collisions

def attack() :
	expensive_size = 4
	expensive_state = b'\x00'*expensive_size
	start = 0

	while True:
		d = {}
		collisions = generate_collision(expensive_size*4, start)

		for m in collisions :
			h = mdhash(m, expensive_state)

			if h in d :
				collision = d[h]
				if mdhash(m, b'\x00\x00') == mdhash(collision, b'\x00\x00') :
					print('Found one m -', m, 'h -', h, 'collision -', collision)
			else :
				d[h] = m

		start += 100000

	return 'Nothing found'

if __name__ == '__main__' :
	attack()
