from rsa import RSA

def extended_gcd(a, m) :
	last_r, r = a, m
	x, last_x, y, last_y = 0, 1, 1, 0

	while r :
		last_r, (q, r) = r, divmod(last_r, r)
		x, last_x =  last_x - q*x, x
		y, last_y =  last_y - q*y, y

	return last_r, last_x*(-1 if a < 0 else 1), last_y*(-1 if m < 0 else 1)

def modinv(a, m) :
	g, x, y = extended_gcd(a, m)
	if g != 1 : raise ValueError
	return x % m

plaintext = b'text Jun3 bug!'
ciphertexts = []

for _ in range(3) :
	cipher = RSA(150)
	ciphertexts.append([cipher.encrypt(plaintext), cipher.n])

(c_0, n_0), (c_1, n_1), (c_2, n_2) = ciphertexts
c_0, c_1, c_2 = int.from_bytes(c_0, 'big'), int.from_bytes(c_1, 'big'),\
 int.from_bytes(c_2, 'big')
ms_0, ms_1, ms_2 = n_1*n_2, n_0*n_2, n_0*n_1

result = ((c_0 * ms_0 * modinv(ms_0, n_0)) + (c_1 * ms_1 * modinv(ms_1, n_1)) +\
 (c_2 * ms_2 * modinv(ms_2, n_2)))
result = result % (n_0 * n_1 * n_2)

lo, hi = 0, result
while lo < hi :
	mid = (lo + hi) // 2
	if mid ** 3 <  result:
		lo = mid + 1
	else :
		hi = mid

result = lo

print(result.to_bytes((result.bit_length() + 7) // 8, 'big'))
