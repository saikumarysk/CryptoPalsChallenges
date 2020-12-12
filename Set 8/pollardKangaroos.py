from random import randint, choice
import hashlib

def modexp(b, e, m) : # Computes (b^e) mod m
	x = 1
	while e > 0 :
		b, e, x = (b*b) % m, e//2, (b*x)%m if e & 1 else x

	return x

def mul_inv(a, b):
	b0 = b
	x0, x1 = 0, 1
	if b == 1: return 1
	while a > 1:
		q = a // b
		a, b = b, a%b
		x0, x1 = x1 - q * x0, x0
	if x1 < 0: x1 += b0
	return x1

def factors(n) :
	result = []

	for i in range(2, (1 << 16) + 1) :
		if n%i == 0 : result.append(i)

	return result

k = 22 # experimental value
con = 4 # experimental value
f = lambda y: 1 << (y%k)
N = (con*((1 << k) - 1))//k # 7.6 million iterations

def pollard_algorithm(p, q, g, y, a, b) :
	xT = 0
	yT = modexp(g, b, p)

	for _ in range(N) :
		f_yT = f(yT)%q # mod q as order of g is q and thus all exponents are in Z_q
		xT = (xT+f_yT)%q # mod q as order of g is q and thus all exponents are in Z_q
		yT = (yT*modexp(g, f_yT, p))%p

	xW = 0
	yW = y
	while xW < b - a + xT :
		f_yW = f(yW)%q
		xW = (xW+f_yW)%q
		yW = (yW*modexp(g, f_yW, p))%p

		if yW == yT :
			return b + xT - xW

if __name__ == '__main__' :
	p = 11470374874925275658116663507232161402086650258453896274534991676898999262641581519101074740642369848233294239851519212341844337347119899874391456329785623
	q = 335062023296420808191071248367701059461
	j = 34233586850807404623475048381328686211071196701374230492615844865929237417097514638999377942356150481334217896204702
	g = 622952335333961296978159266084741085889881358738459939978290179936063635566740258555167783009058567397963466103140082647486611657350811560630587013183357

	a, b = 0, 1<<20
	y = 7760073848032689505395005705677365876654629189298052775754597607446617558600394076764814236081991643094239886772481052254010323780165093955236429914607119

	x = pollard_algorithm(p, q, g, y, a, b)
	print('y -', y)
	print('x is -', x)
	print('g^x mod p -', modexp(g, x, p))
	print('Are they same -', y == modexp(g, x, p))
	print('##################################################################')
	y = 9388897478013399550694114614498790691034187453089355259602614074132918843899833277397448144245883225611726912025846772975325932794909655215329941809013733
	a, b = 0, 1<<40

	x = pollard_algorithm(p, q, g, y, a, b)
	print('y -', y)
	print('x is -', x)
	print('g^x mod p -', modexp(g, x, p))
	print('Are they same -', y == modexp(g, x, p))

	x = randint(1, q-1)
	X = modexp(g, x, p)

	factors_j = factors(j)
	r = choice(factors_j)
	h = 1
	while h == 1 :
		h = modexp(randint(1, p-1), (p-1)//r, p)
	K = modexp(h, x, p)
	m = b'crazy flamboyant for the rap enjoyment'
	t = hashlib.new('md4', K.to_bytes((K.bit_length() + 7)//8, 'big')\
	 + m).hexdigest()
	n = 0
	for i in range(1, r+1) :
		K_1 = modexp(h, i, p)
		t_1 = hashlib.new('md4', K_1.to_bytes((K_1.bit_length() + 7)//8,\
		 'big') + m).hexdigest()
		if t_1 == t :
			n = i
			break

	# This takes a while as upper bound is very large
	a, b = 0, (q-1)//r
	g_1 = modexp(g, r, p)
	g_inverse = mul_inv(g, p)
	y_1 = (X*(modexp(g_inverse, n, p)))%p
	
	m = pollard_algorithm(p, q, g_1, y_1, a, b)
	print('m -', m)
	x_derived = n + m*r
	print('So, derived x -', x_derived)
	print('Are they same -', x_derived == x)
