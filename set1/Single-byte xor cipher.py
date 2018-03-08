def xor(a1, a2):
	a = bytearray(len(a1))
	for i in range(len(a1)):
		a[i] = a1[i] ^ a2[i]
	return a


def score(s):
	freq = {}
	freq[' '] = 700000000
	freq['e'] = 390395169
	freq['t'] = 282039486
	freq['a'] = 248362256
	freq['o'] = 235661502
	freq['i'] = 214822972
	freq['n'] = 214319386
	freq['s'] = 196844692
	freq['h'] = 193607737
	freq['r'] = 184990759
	freq['d'] = 134044565
	freq['l'] = 125951672
	freq['u'] = 88219598
	freq['c'] = 79962026
	freq['m'] = 79502870
	freq['f'] = 72967175
	freq['w'] = 69069021
	freq['g'] = 61549736
	freq['y'] = 59010696
	freq['p'] = 55746578
	freq['b'] = 47673928
	freq['v'] = 30476191
	freq['k'] = 22969448
	freq['x'] = 5574077
	freq['j'] = 4507165
	freq['q'] = 3649838
	freq['z'] = 2456495
	
	score = 0
	for c in s.lower():
		if c in freq:
			score += freq[c]
	return score
	
def break_single_key_xor(a1):
	max_score= None
	english_plaintext = None
	key = None

	for i in range(256):
		a2 = [i] * len(a1)
		plaintext = bytes(xor(a1,a2))
		temp_score = score(plaintext)

		if temp_score > max_score or not max_score:
			max_score = temp_score
			english_plaintext = plaintext
			key = chr(i)

	return key, english_plaintext
		
a1 = bytearray.fromhex("1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736")


print break_single_key_xor(a1)	
