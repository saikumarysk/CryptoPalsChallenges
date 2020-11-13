from mt19937RNG import mt19937
from random import randint

def clone() -> tuple :
	seed = randint(0, (1<<16)-1)
	rng = mt19937(seed)
	mt = []
	for _ in range(624) :
		rand_num = rng.extract_number()
		#print(rand_num)
		untempered_rand_num = untemper(rand_num)
		mt.append(untempered_rand_num)
		#print(mt)

	new_rng = mt19937(1)
	new_rng.MT = mt
	new_rng.index = new_rng.n

	return (new_rng, rng)

def untemper(num: int) -> int :
	#print('Here2 -', num)
	num = first_untemper(num)
	#print('Here2 -', num)
	num = second_untemper(num)
	#print('Here2 -', num)
	num = third_untemper(num)
	#print('Here2 -', num)
	num = fourth_untemper(num)
	#print('Here2 -', num)
	return num

def first_untemper(num: int) -> int :
	if num == 0 : return 0
	b = bin(num)[2:]
	b = '0'*(32 - len(b)) + b
	output = b[:18]
	block = bin(int(b[-14:], 2)^int(b[:14], 2))[2:]
	block = '0'*(14 - len(block)) + block
	output += block
	return int(output, 2) & 0xFFFFFFFF

def second_untemper(num: int) -> int :
	b = bin(num)[2:]
	b = '0'*(32 - len(b)) + b
	choice_0 = '0' + b[-16:] + '0'*15
	choice_1 = '1' + b[-16:] + '0'*15

	output_choice_0 = num ^ (int(choice_0, 2) & 0xEFC60000)
	output_choice_1 = num ^ (int(choice_1, 2) & 0xEFC60000)

	if (((output_choice_0&(1<<31)) >> 31)^((output_choice_0 & (1<<16)) >> 16))\
	 == ((num & (1 << 31)) >> 31) :
		return output_choice_0 & 0xFFFFFFFF
	return output_choice_1 & 0xFFFFFFFF

def third_untemper(num: int) -> int :
	b = bin(num)[2:]
	b = '0'*(32 - len(b)) + b
	output = b[-7:]
	mask = bin(0x9D2C5680)[2:]
	b = [b[:4], b[4:11], b[11:18], b[18:25]]
	mask = [mask[:4], mask[4:11], mask[11:18], mask[18:25]]
	for _ in range(4) :
		block = ''
		if _ == 3 :
			block = bin((int(mask.pop(), 2)&int(output[:7][-4:], 2)) ^ int(b.pop(), 2))[2:]
			block = '0'*(4 - len(block)) + block
		else :
			block = bin((int(mask.pop(), 2)&int(output[:7], 2)) ^ int(b.pop(), 2))[2:]
			block = '0'*(7 - len(block)) + block
		output = block + output

	return int(output, 2) & 0xFFFFFFFF

def fourth_untemper(num: int) -> int :
	b = bin(num)[2:]
	b = '0'*(32 - len(b)) + b

	output = b[:11]

	block = bin(int(output[-11:], 2) ^ int(b[11:22], 2))[2:]
	block = '0'*(11 - len(block)) + block
	output += block

	block = bin(int(output[-11:][:10], 2) ^ int(b[22:], 2))[2:]
	block = '0'*(10 - len(block)) + block
	output += block

	return int(output, 2) & 0xFFFFFFFF

if __name__ == '__main__' :
	new_rng, rng = clone()

	print('New\t\told\t\tSame')
	for _ in range(20) :
		new_num = new_rng.extract_number()
		old_num = rng.extract_number()
		print(new_num, old_num, '\t\t', old_num == new_num)
