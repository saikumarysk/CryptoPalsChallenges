from aesInCBC import aesCBC

def random_bytes(n: int) -> str :
	output = b''
	for _ in range(n) :
		output += bytes([randint(0, 255)])

	return output

def keygen() :
	return random_bytes(16)

def xor(s1, s2) :
	output = b''
	for c1, c2 in zip(s1, s2) :
		output += bytes([int(c1)^int(c2)])

	return output

def pad(input: str, block_length: int) -> str :
	rem = len(input)%block_length
	if rem :
		input += chr(block_length - rem)*(block_length - rem)

	return input

master_key = keygen()

def cbcmac(m, iv, key) :
	ciphertext = aesCBC(key, iv).encrypt(m)
	return ciphertext[-16:]

def validate_message(msg, iv, client_mac) :
	server_mac = cbcmac(msg, iv, master_key)
	return server_mac == client_mac

def forge_mac(valid_mac, new_msg) :
	message_block = xor(valid_mac, pad(new_msg))
	return cbcmac(message_block, b'\x00'*16, master_key)

def attack() :
	my_id = 1
	target_id = 2

	valid_msg = b'from=#1&to=#2&amount=#100000000' # One hundred million dollars
	good_iv = b'\x00'*16
	client_mac = cbcmac(valid_msg, good_iv, master_key)

	bad_msg = b'from=#2&to=#1&amount=#100000000'
	bad_iv = xor(bad_msg[:16], xor(valid_msg[:16], good_iv))
	print(validate_message(bad_msg, bad_iv, client_mac))

	valid_msg = b'from=#2&tx_list=#3:5000;4:7000'
	valid_mac = cbcmac(valid_msg, b'\x00'*16, master_key)

	bad_msg = ';1:100000000'
	forged_mac = forge_mac(valid_mac, bad_msg)
	forged_msg = pad(valid_msg) + pad(bad_msg)

	print('Are the macs same?', forged_mac == cbcmac(forged_msg, b'\x00'*16,\
	 master_key))

if __name__ == '__main__' :
	attack()
