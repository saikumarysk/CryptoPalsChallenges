import bleichenbacherPKCS1_5

if __name__ == '__main__' :
	plaintext = b'howdy!'
	print('Plaintext -', plaintext)
	m = pkcs1_5Pad(plaintext, 96s)
	print('m -', m)
	cipher = RSA(768)
	c = cipher.encrypt(m)
	print('c -', c)

	print('Does c have the right padding -', is_padding_correct(c, cipher))

	decrypted_plaintext = attack(c, cipher, 32)
	print('Decrypted Plaintext -', decrypted_plaintext)
	print('Are they same? ', plaintext == decrypted_plaintext)
