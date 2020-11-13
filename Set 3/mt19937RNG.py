class mt19937(object) :

	def __init__(self, seed: int) -> None:
		self.seed = seed

		self.w, self.n, self.m, self.r = 32, 624, 397, 31
		self.MT = [0]*(self.n)
		self.index = self.n + 1
		self.a = 0x9908B0DF
		self.u, self.d = 11, 0xFFFFFFFF
		self.s, self.b = 7, 0x9D2C5680
		self.t, self.c = 15, 0xEFC60000
		self.l, self.f = 18, 1812433253

		self.lower_mask = (1 << self.r) - 1
		self.upper_mask = (not self.lower_mask) & ((1 << self.w) - 1)

		self.seed_mt()

	def seed_mt(self) -> None:
		self.index = self.n
		self.MT[0] = self.seed
		for i in range(1, self.n) :
			self.MT[i] = (self.f * (self.MT[i-1] ^ (self.MT[i-1] >>\
			 (self.w - 2))) + i) & ((1 << self.w) - 1)

	def extract_number(self) -> int :
		if self.index > self.n : self.seed_mt(5489)
		if self.index == self.n : self.twist()

		y = self.MT[self.index]
		#print('Here1 -', y)
		y ^= (y >> self.u) & self.d
		#print('Here1 -', y)
		y ^= (y << self.s) & self.b
		#print('Here1 -', y)
		y ^= (y << self.t) & self.c
		#print('Here1 -', y)
		y ^= (y >> self.l)
		#print('Here1 -', y)

		self.index += 1
		return y & ((1 << self.w) - 1)

	def twist(self) -> None:
		for i in range(self.n) :
			x = (self.MT[i] & self.upper_mask) + (self.MT[(i + 1) % (self.n)] &\
			 self.lower_mask)
			xA = x >> 1
			if x&1 : xA = xA^x
			self.MT[i] = self.MT[(i + self.m) % (self.n)] ^ xA

		self.index = 0

if __name__ == '__main__' :
	rng = mt19937(1599248270)
	for _ in range(10) :
		print(rng.extract_number())
