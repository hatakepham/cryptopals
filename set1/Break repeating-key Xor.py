def xor(b1, b2):
    b = bytearray(len(b1))
    for i in range(len(b1)):
        b[i] = b1[i] ^ b2[i]
    return b
# xor 2 chuoi

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
# ham tinh diem cua planintext    

def  hamming_distance(b1, b2):
    differing_bits = 0
    for byte in xor(b1, b2):
        differing_bits += bin(byte).count("1")
    return differing_bits
# tinh khoang cach hamming

def hamming_distance(b1, b2):
    differing_bits = 0
    for byte in xor(b1, b2):
        differing_bits += bin(byte).count("1")
    return differing_bits

def  break_single_key_xor(b1):
    max_score = None
    english_plaintext = None
    key = None

    for i in range(256):
        b2 = [i]* len(b1)
        plaintext = bytes(xor(b1,b2))
        pscore = score(plaintext)

        if pscore > max_score or not max_score:
            max_score = pscore
            english_plaintext = plaintext
            key = chr(i)

    return key, english_plaintext

# ham tim single key 

b = bytearray("".join(list(open("ch6.txt", "r"))).decode("base64"))

normalized_distances = []

for KEYSIZE in range(2, 40):
    b1 = b[:KEYSIZE]
    b2 = b[KEYSIZE:KEYSIZE*2]
    b3 = b[KEYSIZE*2:KEYSIZE*3]
    b4 = b[KEYSIZE*3:KEYSIZE*4]

    normalized_distance = float(hamming_distance(b1,b2) + hamming_distance(b2,b3) + hamming_distance(b3,b4))/(KEYSIZE*3)

    normalized_distances.append((KEYSIZE, normalized_distance)) 

normalized_distances = sorted(normalized_distances, key=lambda (_, y): y)
#sort ket qua hamming


for KEYSIZE, _ in normalized_distances[:4]:
    block_types = [[] for _ in range(KEYSIZE)]
    for i,byte in enumerate(b):
        block_types[i % KEYSIZE].append(byte)

    keys = ""
    for bbytes in block_types:
        keys += break_single_key_xor(bbytes)[0]

    key = bytearray(keys * len(b))
    plaintext = bytes(xor(b,key))

    print keys
    print KEYSIZE
    print plaintext