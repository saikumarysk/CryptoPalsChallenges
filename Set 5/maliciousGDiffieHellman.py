'''

As you can see the code will be a lot bigger. I can explain what happens in each
case and you can write the code yourself.

If we replace g = 1 then for any random a or b, A and B will be 1
So, the s will be 1 and the AES key will be sha1(b'\x01')[:32]. Thus, you can
intercept the messages the same way we have done in the previous exercise

If we replace g = p then for any random a or b, A and B will be 0
Exactly same as previous exercise

If we replace g = p-1, situation is a little bit complicated. You can refer to
the table to see what happens

a			b			A			B			keyA		keyB
----		----		----		----		----		----
odd 		odd 		p-1 		p-1 		p-1 		p-1
odd 		even		p-1 		1    		1    		1
even		odd 		1    		p-1 		1    		1
even		even		1    		1    		1    		1

So, you can predict the key and still intercept the messages

So, moral is that A->B ACK snhould not happen without checking if someone is
tampering with the keys

'''
