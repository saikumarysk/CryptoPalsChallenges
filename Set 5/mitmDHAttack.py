from aesInCBC import aesCBC
from sha1MAC import sha1
from random import randint

def random_bytes(n: int) -> str :
	output = b''
	for _ in range(n) :
		output += bytes([randint(0, 255)])

	return output

def modexp(b: int, e: int, m: int) : # Computes (b^e) mod m
	x = 1
	while e > 0 :
		b, e, x = (b*b) % m, e//2, (b*x)%m if e & 1 else x

	return x

def remove_padding(text: str) -> str :
	if text[-text[-1]:] == bytes([text[-1]])*text[-1] : text = text[:-text[-1]]
	return text

def get_diffie_hellman(p=None, g=None) -> tuple :
	if not p : p = int('ffffffffffffffffc90fdaa22168c234c4c6628b80dc1cd129024e088a67cc74020bbea63b139b22514a08798e3404ddef9519b3cd3a431b302b0a6df25f14374fe1356d6d51c245e485b576625e7ec6f44c42e9a637ed6b0bff5cb6f406b7edee386bfb5a899fa5ae9f24117c4b1fe649286651ece45b3dc2007cb8a163bf0598da48361c55d39a69163fa8fd24cf5f83655d23dca3ad961c62f356208552bb9ed529077096966d670c354e4abc9804f1746c08ca237327ffffffffffffffff', 16)
	if not g : g = 2
	a = randint(1, p-1)
	A = modexp(g, a, p)

	return (p, g, a, A)

def get_key_diffie_hellman(capital: int, small: int, prime: int) :
	s = modexp(capital, small, prime)
	key = sha1(s.to_bytes((s.bit_length() + 7) // 8, 'big'))[:32]

	key = bytes.fromhex(key)
	return key

stateA, stateB = 0, 0
state_attack = 0
dA, dB = {}, {}
d_attack = {}
queue = []

def processA() :
	global stateA, dA
	if stateA == 0 :
		p, g, a, A = get_diffie_hellman()
		dA['p'] = p
		dA['g'] = g
		dA['a'] = a
		dA['A'] = A
		queue.append((p, g, A))
		stateA = (stateA + 1)%3
	elif stateA == 1 :
		B = queue.pop()
		dA['B'] = B
		dA['key'] = get_key_diffie_hellman(dA['B'], dA['a'], dA['p'])
		dA['iv'] = random_bytes(16)
		cipher = aesCBC(dA['key'], dA['iv'])
		print('Sending A - Hello There!')
		queue.append(cipher.encrypt(b'Hello There!') + dA['iv'])
		stateA = (stateA + 1)%3
	elif stateA == 2 :
		ciphertext = queue.pop()
		iv = ciphertext[-16:]
		ciphertext = ciphertext[:-16]
		cipher = aesCBC(dA['key'], iv)
		decrypted_plaintext = cipher.decrypt(ciphertext)
		decrypted_plaintext = remove_padding(decrypted_plaintext)
		print('Received A -', decrypted_plaintext)
		stateA = (stateA + 1)%3

def processB() :
	global stateB, dB
	if stateB == 0 :
		p, g, A = queue.pop()
		p, g, b, B = get_diffie_hellman(p, g)
		dB['p'] = p
		dB['g'] = g
		dB['b'] = b
		dB['B'] = B
		dB['A'] = A
		dB['key'] = get_key_diffie_hellman(dB['A'], dB['b'], dB['p'])
		queue.append(B)
		stateB = (stateB + 1)%2
	elif stateB == 1 :
		ciphertext = queue.pop()
		iv = ciphertext[-16:]
		ciphertext = ciphertext[:-16]
		cipher = aesCBC(dB['key'], iv)
		decrypted_plaintext = cipher.decrypt(ciphertext)
		decrypted_plaintext = remove_padding(decrypted_plaintext)
		print('Received B -', decrypted_plaintext)
		print('Sending B - General Kenobi!')
		dB['iv'] = random_bytes(16)
		cipher = aesCBC(dB['key'], dB['iv'])
		queue.append(cipher.encrypt(b'General Kenobi!') + dB['iv'])
		stateB = (stateB + 1)%2

def attacker() :
	global state_attack, d_attack
	if state_attack == 0 :
		p, g, A = queue.pop()
		d_attack['p'] = p
		print('[*] Got p, g, A -', p, g, A)
		print('[*] Replacing A with p')
		queue.append((p, g, p))
		state_attack = (state_attack + 1) % 4
	elif state_attack == 1 :
		B = queue.pop()
		print('[*] Got B -', B)
		print('[*] Replacing B with p')
		queue.append(d_attack['p'])
		state_attack = (state_attack + 1) % 4
	elif state_attack == 2 :
		ciphertext = queue[0]
		iv = ciphertext[-16:]
		ciphertext = ciphertext[:-16]
		print('[*] Got ciphertext and iv -', ciphertext, iv)
		key = sha1(b'')[:32]
		d_attack['key'] = bytes.fromhex(key)
		print('[*] From Diffie-Hellman, actual key -', d_attack['key'])
		cipher = aesCBC(d_attack['key'], iv)
		print('[*] Actual plaintext -', remove_padding(cipher.decrypt(\
		ciphertext)))
		state_attack = (state_attack + 1) % 4
	elif state_attack == 3 :
		ciphertext = queue[0]
		iv = ciphertext[-16:]
		ciphertext = ciphertext[:-16]
		print('[*] Got ciphertext and iv -', ciphertext, iv)
		cipher = aesCBC(d_attack['key'], iv)
		print('[*] Actual plaintext -', remove_padding(cipher.decrypt(\
		ciphertext)))
		state_attack = (state_attack + 1) % 4

def normal_functionality() :
	processA()
	processB()
	processA()
	processB()
	processA()

def mitm_attack() :
	processA()
	attacker()
	processB()
	attacker()
	processA()
	attacker()
	processB()
	attacker()
	processA()

if __name__ == '__main__' :
	print('Normal functionality :-')
	print('-----------------------\n')
	normal_functionality()

	print('\nAttacker involved :-')
	print('--------------------\n')
	print('[*] - denotes attacker\n')
	mitm_attack()
