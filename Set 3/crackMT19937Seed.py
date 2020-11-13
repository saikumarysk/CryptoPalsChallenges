import time
from random import randint
from mt19937RNG import mt19937

curr_time = 0

def routine() -> int :
	global curr_time
	curr_time = int(time.time())
	curr_time += randint(40, 1000)
	seed = curr_time
	rng = mt19937(seed)
	curr_time += randint(40, 500)
	return rng.extract_number(), seed

def attack(num: int) -> int :
	global curr_time
	curr_time += randint(5, 10)
	possible_seeds = []
	for i in range(1600) :
		seed = curr_time - i
		rng = mt19937(seed)
		if rng.extract_number() == num : possible_seeds.append(seed)

	return possible_seeds

if __name__ == '__main__' :
	random_num = routine()
	possible_seeds = attack(random_num[0])
	print('Possible seeds -', possible_seeds)
	print('Is guess correct -', random_num[1] in possible_seeds)
