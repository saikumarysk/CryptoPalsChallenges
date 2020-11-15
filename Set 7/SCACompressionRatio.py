from aesInCBC import aesCBC
from zlib import compress

def random_bytes(n: int) -> str :
	output = b''
	for _ in range(n) :
		output += bytes([randint(0, 255)])

	return output

def keygen() :
	return random_bytes(16)

def detect_compressed_size(plaintext) :
	key, iv = keygen(), keygen()

	request = b'POST / HTTP/1.1\nHost: hapless.com\nCookie: sessionid=TmV2ZXIgcmV2ZWFsIHRoZSBXdS1UYW5nIFNlY3JldCE=\nContent-Length: '+str(len(plaintext))+'\n'+plaintext
	ciphertext = aesCBC(key, iv).encrypt(compress(request))
	return len(ciphertext)

def calculate_padding(content) :
	padding = b'ABCDEFGHIJKLMNOP'
	curr_len = detect_compressed_size(content)

	i = 0
	while detect_compressed_size(content + padding[:i]) == curr_len :
		i += 1

	return padding[:i-1]

def attack() :
	content = b'sessionid='
	shortest = [b'']

	while True :
		min_len = 1000000
		round_shortest = []
		padding = calculate_padding(content + shortest[0])

		for x in range(64) :
			guess = chr(x)
			for cand in shortest :
				text = padding + content + cand + guess
				length = detect_compressed_size(text)

				if length == min_len :
					round_shortest.append(cand + guess)
				elif length < min_len :
					round_shortest = [cand + guess]
					min_len = length

		shortest = round_shortest[:]
		if len(shortest) == 1 and shortest[0][-1] == '\n' :
			print('Session id -', shortest[0][:-1])

if __name__ == '__main__' :
	attack()
