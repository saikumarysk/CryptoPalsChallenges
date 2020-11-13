import requests

def attack(file_name) -> str :
	sig = ''
	for _ in range(20) :
		times = []
		for i in range(256) :
			temp_sig = sig + hex(i)[2:] + '00'*(40 - len(sig))
			sum_times = 0
			for j in range(10) : # For next challenge, incerease rounds to get more precise
				response = requests.get('http://127.0.0.1:8080/test?file='+\
				 file_name+'&signature='+temp_sig)

				if response.status_code == 200 : return temp_sig
				sum_times += response.elapsed.total_seconds()

			avg_time = sum_times / 10
			times.append(avg_time)

		best = max(range(256), key = lambda x: times[x])
		print(times)
		sig += '0'*(2 - len(hex(best)[2:])) + hex(best)[2:]
		print(sig)

	return sig


if __name__ == '__main__' :
	signature = attack("Lorem.txt")
	print('Signature found from attack -', signature)
	verify_signature = '' # Change it
	print('Actual signature -', verify_signature)
	print('Are both same -', verify_signature == signature)
