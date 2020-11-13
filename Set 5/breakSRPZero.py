'''

If we send A to be 0 or N or 2*N ..., basically any multiple of N, at the server
side, S = (A*(v**u))**b % N will become 0. So, no matter the password, S will be
0. So, determining K without S is possible as it is only K value. So, you can
login without password using K = sha256('0')

I am too lazy to write web.py code for this.

'''
