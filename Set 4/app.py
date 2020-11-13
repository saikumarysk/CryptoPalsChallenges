import web
import hmacSHA1
from random import randint
from time import sleep

urls = (
	'/test', 'test'
)
app = web.application(urls, globals())

def keygen() :
	output = b''
	for _ in range(16) :
		output += bytes([randint(0, 255)])

	return output

KEY = keygen()

class test:
	def GET(self):
		print('Key is -', KEY)
		data = web.input()
		file_name = data.file
		signature = data.signature
		file = open(file_name, 'r')
		contents = bytes(file.read(), 'utf-8')
		file.close()
		hmac_sha1_signature = hmacSHA1.hmac_sha1(KEY, contents)

		if self.insecure_compare(hmac_sha1_signature, signature) :
			return 'Everything is fine, baby doll and the key is'+str(KEY)
		else :
			web.application.internalerror('BAD')

	def insecure_compare(self, s1, s2) :
		if len(s1) != len(s2) : return False

		for i in range(0, len(s1), 2) :
			if s1[i:i+2] != s2[i:i+2] : return False
			sleep(0.05)

		return True

if __name__ == "__main__":
	app.run()
