'''

If g = 0, then A = 0. This also means for any arbitrary k, X = 0 and hence r = 0
On the verifier side, v is generated from g and A which are both 0. So, all the
signatures are valid.

If g = p+1 then A = 1. X = 1 and r = 1. Similarly on client's side v = 1
So, all the signatures are valid. So, for any s, this will work. So, the generation
of signatures is non-relevant now.

'''
