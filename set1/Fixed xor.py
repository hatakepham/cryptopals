def xor(a1, a2):
	a = bytearray(len(a1))
	for i in range(len(a1)):
		a[i] = a1[i] ^ a2[i]
	return a

a1 = bytearray.fromhex("1c0111001f010100061a024b53535009181c")
a2 = bytearray.fromhex("686974207468652062756c6c277320657965")

a= bytes(xor(a1,a2))

print a.encode('hex')