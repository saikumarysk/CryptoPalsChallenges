import singleXORCipher

if __name__ == '__main__' :
	cipher_texts = ''
	with open('4.txt','r') as file :
		cipher_texts = file.read()

	cipher_texts = cipher_texts.splitlines()

	min_error = float('inf')
	results, keys, messages = [], [], []
	for cipher_text in cipher_texts :
		key, message, err = singleXORCipher.singleXORCipher(cipher_text)
		if err < min_error :
			min_error = err
			results = [cipher_text]
			keys = key
			messages = message
		elif err == min_error :
			results.append(cipher_text)
			keys.append(key)
			messages.append(message)

	print('Possible Encrypted Message -', results)
	print('Possible Keys -', keys)
	print('Possible plain texts -', messages)

	for i, cipher_text in enumerate(cipher_texts) :
		if cipher_text == results[0] : print('Line number',i+1,'in the file')
