import hashlib
import hmac
from random import randint

def modexp(b: int, e: int, m: int) : # Computes (b^e) mod m
	x = 1
	while e > 0 :
		b, e, x = (b*b) % m, e//2, (b*x)%m if e & 1 else x

	return x

N = int('ffffffffffffffffc90fdaa22168c234c4c6628b80dc1cd129024e088a67cc74020bbea63b139b22514a08798e3404ddef9519b3cd3a431b302b0a6df25f14374fe1356d6d51c245e485b576625e7ec6f44c42e9a637ed6b0bff5cb6f406b7edee386bfb5a899fa5ae9f24117c4b1fe649286651ece45b3dc2007cb8a163bf0598da48361c55d39a69163fa8fd24cf5f83655d23dca3ad961c62f356208552bb9ed529077096966d670c354e4abc9804f1746c08ca237327ffffffffffffffff', 16)
g, k = 2, 3
I, P = 'set8.cryptopals@gmail.com', b'Kt8ph%We?TCYa4E`'
dC, dS = {}, {}
stateC, stateS = 0, 0
queue = []

def preprocess_server() :
	salt = randint(1, (1 << 16) - 1)
	xH = hashlib.sha256(salt.to_bytes((salt.bit_length() + 7)//8, 'big') + P).\
	hexdigest()
	x = int(xH, 16)
	v = modexp(g, x, N)
	dS['v'] = v
	dS['salt'] = salt

def processC() :
	global stateC, dC
	if stateC == 0 :
		a = randint(1, N-1)
		A = modexp(g, a, N)
		dC['a'] = a
		dC['A'] = A
		queue.append((I, A))
		stateC = (stateC + 1)%2
	elif stateC == 1 :
		salt, B = queue.pop()
		dC['salt'] = salt
		dC['B'] = B
		uH = hashlib.sha256(dC['A'].to_bytes((dC['A'].bit_length() + 7)//8,\
		 'big') + dC['B'].to_bytes((dC['B'].bit_length() + 7)//8, 'big')).\
		 hexdigest()
		u = int(uH, 16)
		xH = hashlib.sha256(salt.to_bytes((salt.bit_length() + 7)//8, 'big') +\
		 P).hexdigest()
		x = int(xH, 16)
		gx = modexp(g, x, N)
		kgx = (k*gx)%N
		S = modexp(B - kgx, dC['a'] + u*x, N)
		K = hashlib.sha256(S.to_bytes((S.bit_length() + 7) // 8, 'big')).digest()
		mac_digest = hmac.new(K, salt.to_bytes((salt.bit_length() + 7)//8,\
		 'big'), digestmod=hashlib.sha256).hexdigest()
		queue.append(mac_digest)
		stateC = (stateC + 1)%2

def processS() :
	global stateS, dS
	if stateS == 0 :
		I, A = queue.pop()
		dS['I'] = I
		dS['A'] = A
		b = randint(1, N-1)
		B = k*dS['v'] + modexp(g, b, N)
		dS['b'] = b
		dS['B'] = B
		queue.append((dS['salt'], B))
		uH = hashlib.sha256(dS['A'].to_bytes((dS['A'].bit_length() + 7)//8,\
		 'big') + dS['B'].to_bytes((dS['B'].bit_length() + 7)//8, 'big')).\
		 hexdigest()
		u = int(uH, 16)
		vu = modexp(dS['v'], u, N)
		Avu = (A * vu) % N
		S = modexp(Avu, dS['b'], N)
		K = hashlib.sha256(S.to_bytes((S.bit_length() + 7) // 8, 'big')).\
		digest()
		dS['K'] = K
		stateS = (stateS + 1)%2
	elif stateS == 1 :
		mac_digest = queue.pop()
		my_digest = hmac.new(dS['K'], dS['salt'].to_bytes((dS['salt'].\
		bit_length() + 7) // 8, 'big'), digestmod=hashlib.sha256).hexdigest()
		print('OK' if my_digest == mac_digest else 'Something Wrong')
		stateS = (stateS + 1)%2

def protocol() :
	preprocess_server()
	processC()
	processS()
	processC()
	processS()

if __name__ == '__main__' :
	protocol()
