from Crypto.Cipher import AES

def repeatedBlocks(input: list) -> list :
	possible = []
	for line in input :
		hs = set()
		for i in range(0, len(line), 16) :
			if line[i:i+16] in hs :
				possible.append(line)
				break
			hs.add(line[i:i+16])

	return possible


if __name__ == '__main__' :
	ciphertexts = []
	with open('8.txt', 'r') as file :
		lines = file.read().splitlines()
		for line in lines :
			ciphertexts.append(bytes.fromhex(line))

	possible = repeatedBlocks(ciphertexts)
	print(len(possible),'\n',possible)
	for i, ciphertext in enumerate(ciphertexts) :
		if ciphertext == possible[0] :
			print('Line '+str(i+1)+' in file')
			break
