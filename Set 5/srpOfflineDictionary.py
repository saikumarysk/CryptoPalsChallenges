'''

This is a brute force attack where after getting the hmac-sha256(K, salt) from
client, we try all possible words and guess K and sub-sequently the hmac of it
and match with the provided one. I can use a couple of words to do it. But the
code I have to write for it is not worth it.

'''
