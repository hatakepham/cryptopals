def xor(a1,a2):
	a = bytearray(len(a1))
	for i in range(len(a1)):
		a[i] = a1[i] ^ a2[i]
	return a	

lines = ["Burning 'em, if you ain't quick and nimble\n", "I go crazy when I hear a cymbal"]

text = "".join(lines)
print text

key = bytearray("ICE" * len(text))

plaintext = bytes(xor(bytearray(text),key))

print plaintext.encode("hex")