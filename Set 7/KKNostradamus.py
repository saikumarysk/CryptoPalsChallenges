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

def find_collision(h1, h2) :
	d = {}

	for _ in range(256) :
		m = random_bytes(2)
		hashed = mdhash(m, h1)
		d[hashed] = m

	m = random_bytes(2)
	hashed = mdhash(m, h2)
	while hashed not in d :
		m = random_bytes(2)
		hashed = mdhash(m, h2)

	return d[hashed], m, hashed

def generate_states(k) :
	sieve = []
	initial_states = set()

	while len(initial_states) != (1<<k) :
		initial_states.add(random_bytes(2))

	states = list(initial_states)

	while len(states) != 1 :
		next_states = []

		for i in range(0, len(states), 2) :
			h1, h2 = states[i], states[i+1]
			m1, m2, h = find_collision(h1, h2)

			sieve.append((h1, m1))
			sieve.append((h2, m2))
			next_states.append(h)

		states = next_states[:]
		if len(next_states) == 1 :
			sieve.append((h, None))

	return sieve[::-1]

def generate_suffix(m, sieve) :
	target_states = {h:i for (i, (h, _)) in enumerate(sieve) if i > len(funnel)/2}

	glue = random_bytes(2)
	hashed = mdhash(m+glue, b'\x00\x00')
	while hashed not in target_states :
		glue = random_bytes(2)
		hashed = mdhash(m+glue, b'\x00\x00')

	m = pad(m+glue)
	i = target_states[hashed]
	while i != 0 :
		h, a = sieve[i]
		m += pad(a)
		i = (i-1)//2

	return m

if __name__ == '__main__' :
	sieve = generate_states(8)
	if sieve[0][1] == None :
		prediction = mdhash('', sieve[0][0])
		print('Prediction Hash -', prediction)

		m = b'Prediction message for coming seasons of baseball'
		m = generate_suffix(m, sieve)

		hashed = mdhash(m, b'\x00\x00')
		print('Hashed -', hashed)
		print('Is the attack successful?', hashed == prediction)
