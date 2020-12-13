from random import randint, choice
import math
import hashlib

class Point(object) :

	def __init__(self, x, y, p, a, b) :
		self.x = x
		self.y = y
		self.p = p
		self.a = a
		self.b = b

	def extended_gcd(self, a, m) :
		last_r, r = a, m
		x, last_x, y, last_y = 0, 1, 1, 0

		while r :
			last_r, (q, r) = r, divmod(last_r, r)
			x, last_x =  last_x - q*x, x
			y, last_y =  last_y - q*y, y

		return last_r, last_x*(-1 if a < 0 else 1), last_y*(-1 if m < 0 else 1)

	def lcm(self, a, b) :
		g, x, y = self.extended_gcd(a, b)
		return (a*b) // g

	def modinv(self, a, m) : # computes a^-1 mod m
		g, x, y = self.extended_gcd(a, m)
		if g != 1 : raise ValueError
		return x % m

	@classmethod
	def modexp(cls, b, e, m) : # computes b^e mod m
		x = 1
		while e > 0 :
			b, e, x = (b*b) % m, e//2, (b*x)%m if e & 1 else x

		return x

	@classmethod
	def _legendre(cls, n, p) : # Find n^((p-1)//2) mod p
		return cls.modexp(n, (p-1)//2, p)

	@classmethod
	def _tonelli_shanks(cls, n, p) : # Find r such that r^2 = n mod p
		q = p-1
		s = 0
		while q&1 == 0 :
			s += 1
			q >>= 1

		if s == 1 : return cls.modexp(n, (p+1)//4, p)

		z = 0
		for i in range(2, p) :
			if cls._legendre(i, p) == p-1 :
				z = i
				break

		c = cls.modexp(z, q, p)
		r = cls.modexp(n, (q+1)//2, p)
		t = cls.modexp(n, q, p)
		m = s
		t2 = 0

		while (t-1)%p != 0 :
			t2 = (t*t)%p
			for i in range(1, m) :
				if (t2-1)%p == 1 : break
				t2 = (t2*t2)%p
			b = cls.modexp(c, 1 << (m-i-1), p)
			r = (r*b)%p
			c = (b*b)%p
			t = (t*c)%p
			m = i

		return r

	@classmethod
	def get_random(cls, p, a, b) : # Find random point on EC(GF(p), a, b)
		l = p-1
		x = 0
		y_power_2 = 0
		while l != 1 :
			x = randint(1, p-1)
			y_power_2 = (x**3 + a*x + b)%p
			l = cls._legendre(y_power_2, p)

		y = cls._tonelli_shanks(y_power_2, p)
		return Point(x, y, p, a, b)

	def copy(self) :
		return Point(self.x, self.y, self.p, self.a, self.b)

	def is_identity(self) :
		return (self.x == float('inf') or self.x == float('-inf')) and\
		 (self.y == float('inf') or self.y == float('-inf'))

	def is_valid(self) :
		lhs = (self.y*self.y)%self.p
		rhs = (self.modexp(self.x, 3, self.p) + self.a*self.x + self.b)%self.p
		return lhs == rhs

	def inverse(self) :
		return Point(self.x, self.p-self.y, self.p, self.a, self.b)

	def double(self) :
		if self.is_identity() : return self.copy()
		if self.y == 0 : return Point(float('inf'), float('inf'), self.p,\
		 self.a, self.b)

		m = ((3*self.x*self.x + self.a)*self.modinv(2*self.y, self.p))%self.p
		x1 = (m*m - 2*self.x)%self.p
		y1 = (m*(self.x - x1) - self.y)%self.p
		return Point(x1, y1, self.p, self.a, self.b)

	def add(self, q) :
		if self.is_identity() :
			return q.copy()

		if q.is_identity() :
			return self.copy()

		if q == self.inverse() :
			return Point(float('inf'), float('inf'),\
			 self.p, self.a, self.b)

		x1, y1 = self.x, self.y
		x2, y2 = q.x, q.y

		if x1 == x2 and y1 == y2 :
			return self.double()
		elif self.x == q.x : return Point(float('inf'), float('inf'), self.p,\
			 self.a, self.b)

		m = ((y2 - y1)*self.modinv((x2 - x1)%self.p, self.p))%self.p
		x3 = (m*m - x1 - x2)%self.p
		y3 = (m*((x1 - x3)%self.p) - y1)%self.p

		return Point(x3, y3, self.p, self.a, self.b)

	def scale(self, k) :
		p = self.copy()
		result = Point(float('inf'), float('inf'), self.p, self.a, self.b)
		i = 1
		while k > 0 :
			if k & 1 : result = result.add(p)
			p = p.add(p)
			k >>= 1

		return result

	def __eq__(self, q) :
		return self.x == q.x and self.y == q.y and self.p == q.p and\
		 self.a == q.a and self.b == q.b

	def __ne__(self, q) :
		return not self.__eq__(q)

	def __repr__(self) :
		return '( {x}, {y} ). Field - GF({p}). Curve - y^2 = x^3 + ({a})x + ({b})'.\
		format(x = self.x, y = self.y, p = self.p, a = self.a, b = self.b)

	def __str__(self) :
		return self.__repr__()

m = b'crazy flamboyant for the rap enjoyment'

def generate_keypair(baseorder, base) :
	secret = randint(1, baseorder-1)
	public = base.scale(secret)
	return secret, public

def factors(n) :
	result = []

	for i in range(2, (1<<20) + 1) : # Increasing the limit will increase time but increase the chances of finding the correct result
		if n%i == 0 : result.append(i)

	return result

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

def attack(p, baseorder, base) :
	a, A = generate_keypair(baseorder, base)

	print('secret is -', a)
	print('public is -', A)

	b1, b2, b3 = 210, 504, 727
	q1, q2, q3 = 233970423115425145550826547352470124412,\
	 233970423115425145544350131142039591210,\
	 233970423115425145545378039958152057148

	factors_q1, factors_q2, factors_q3 = factors(q1), factors(q2), factors(q3)
	b_s, r_s, r_set = [[]], [[]], [set()]
	print('First q')
	subgroupC(factors_q1, r_s, r_set, q1, b1, b_s, int(baseorder**(1/3))+1, p, base.a, a)
	print('Second q')
	subgroupC(factors_q2, r_s, r_set, q2, b2, b_s, int(baseorder**(1/3)), p, base.a, a)
	print('Third q')
	subgroupC(factors_q3, r_s, r_set, q3, b3, b_s, int(baseorder**(1/3))+1, p, base.a, a)

	a_derived = chinese_remainder_theorem(r_s, b_s)
	print('a derived -', a_derived)
	print('Are they same -', a == a_derived)

def subgroupC(factor_list, r_s, r_set, q, b, b_s, limit, p, a, secret) :
	r_prod = 1
	while r_prod <= limit :
		r = choice(factor_list)
		if r in r_set[0] : continue
		flag = False
		for r_i in r_s[0] :
			if gcd(r_i, r) != 1 :
				flag = True
				break
		if flag: continue

		h = Point(float('inf'), float('inf'), p, a, b)
		while h.is_identity() :
			h = Point.get_random(p, a, b).scale(q//r)

		K = h.scale(secret)
		print('K -', K)
		t = hashlib.new('md4', bytes(str(K), 'utf-8')+m).hexdigest()
		print('t -', t)

		for i in range(1, r+1) :
			K_1 = h.scale(i)
			t_1 = hashlib.new('md4', bytes(str(K_1), 'utf-8')+m).hexdigest()
			if t_1 == t :
				print('Match found')
				b_s[0].append(i)
				r_s[0].append(r)
				r_set[0].add(r)
				r_prod *= r
				break

if __name__ == '__main__' :
	G = Point(182, 85518893674295321206118380980485522083,\
	 233970423115425145524320034830162017933, -95051, 11279326)
	'''print(G)
	print(G.inverse())
	print(G.double())
	print(G.add(G.inverse()))
	print(G.scale(29246302889428143187362802287225875743))
	print(G.scale(233970423115425145498902418297807005944))

	baseorder = 29246302889428143187362802287225875743 # Other one also works
	base = G
	a, A = generate_keypair(baseorder, base)
	b, B = generate_keypair(baseorder, base)

	print(A.scale(b))
	print(B.scale(a))
	print('Are they same -', A.scale(b) == B.scale(a))'''

	p = 233970423115425145524320034830162017933
	baseorder = 29246302889428143187362802287225875743
	base = G

	attack(p, baseorder, base)
