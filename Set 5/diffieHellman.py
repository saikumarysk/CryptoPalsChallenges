from random import randint
import hashlib

def modexp(b: int, e: int, m: int) : # Computes (b^e) mod m
	x = 1
	while e > 0 :
		b, e, x = (b*b) % m, e//2, (b*x)%m if e & 1 else x

	return x

def diffie_hellman(p: int, g: int) :
	a = randint(1, p-1)
	print('a -', a)
	A = modexp(g, a, p)
	print('A -', A)
	b = randint(0, p-1)
	print('b -', b)
	B = modexp(g, b, p)
	print('B -', B)
	s1 = modexp(B, a, p)
	print('s1 -', s1)
	s2 = modexp(A, b, p)
	print('s2 -', s2)
	print('Are they same -', s1 == s2)
	hex_value = hex(s1)[2:]
	if len(hex_value) & 1 : hex_value = '0' + hex_value
	hash = hashlib.new('md4', bytes.fromhex(hex_value)).hexdigest()
	print('128 bit key -', hash)
	print('###################################################################')

if __name__ == '__main__' :
	diffie_hellman(37, 5)
	p = int('ffffffffffffffffc90fdaa22168c234c4c6628b80dc1cd129024e088a67cc74020bbea63b139b22514a08798e3404ddef9519b3cd3a431b302b0a6df25f14374fe1356d6d51c245e485b576625e7ec6f44c42e9a637ed6b0bff5cb6f406b7edee386bfb5a899fa5ae9f24117c4b1fe649286651ece45b3dc2007cb8a163bf0598da48361c55d39a69163fa8fd24cf5f83655d23dca3ad961c62f356208552bb9ed529077096966d670c354e4abc9804f1746c08ca237327ffffffffffffffff', 16)
	diffie_hellman(p, 2)
