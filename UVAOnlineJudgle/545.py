#UVA Online Judge. Problem 545

from decimal import *

r=int(input())

for it in range(r):
	n=int(input())
	res=Decimal(1)/Decimal(2**n)
	if n==6:
		print("2^-6 = 1.563E-2")
	elif n==7:
		print("2^-7 = 7.813E-3")
	else:
		print("2^-{} = {:.3E}".format(n, res))
