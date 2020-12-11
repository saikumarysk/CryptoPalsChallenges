from random import randint, choice
from functools import reduce
from math import sqrt
import hashlib

def modexp(b, e, m) : # Computes (b^e) mod m
	x = 1
	while e > 0 :
		b, e, x = (b*b) % m, e//2, (b*x)%m if e & 1 else x

	return x

def chinese_remainder_theorem(n, a) :
	result = 0
	prod = reduce(lambda a, b: a*b, n)
	for n_i, a_i in zip(n, a) :
		p = prod//n_i
		result += a_i * mul_inv(p, n_i) * p

	return result % prod

def gcd(a, b):
	if (b == 0): return a
	return gcd(b, a%b)

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

p = 7199773997391911030609999317773941274322764333428698921736339643928346453700085358802973900485592910475480089726140708102474957429903531369589969318716771
g = 4565356397095740655436854503483826832136106141639563487732438195343690437606117828318042418238184896212352329118608100083187535033402010599512641674644143
q = 236234353446506858198510045061214171961
j = 30477252323177606811760882179058908038824640750610513771646768011063128035873508507547741559514324673960576895059570
m = b'crazy flamboyant for the rap enjoyment'
a = 0
b = 0
while a == b :
	a = randint(1, q-1)
	b = randint(1, q-1)

b_s, r_s, r_set = [], [], set()
r_prod = 1
factors_j = factors(j)
#print(factors_j)
while r_prod <= q :
	r = choice(factors_j)
	if r in r_set : continue
	flag = False
	for r_i in r_s :
		if gcd(r_i, r) != 1 :
			flag = True
			break

	if flag : continue
	h = 1
	while h == 1 :
		h = modexp(randint(1, p-1), (p-1)//r, p)
	K = modexp(h, b, p) # Bob does this and sends m and t to us
	t = hashlib.new('md4', K.to_bytes((K.bit_length() + 7)//8, 'big')\
	 + m).hexdigest()

	for i in range(1, r+1) :
		K_1 = modexp(h, i, p)
		t_1 = hashlib.new('md4', K_1.to_bytes((K_1.bit_length() + 7)//8,\
		 'big') + m).hexdigest()
		if t_1 == t :
			b_s.append(i)
			r_s.append(r)
			r_set.add(r)
			r_prod *= r
			break

b_derived = chinese_remainder_theorem(r_s, b_s)
print('Derived b -', b_derived)
print('Actual b -', b)
print('Are they same -', b == b_derived)
