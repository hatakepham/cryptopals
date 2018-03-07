from Crypto.Cipher import AES
from random import randint
from collections import defaultdict

def xor(b1, b2):
	b = bytearray(len(b1))
	for i in range(len(b1)):
		b[i] = b1[i] ^ b2[i]
	return b

def aes_128_ecb_enc(buffer, key):
	obj = AES.new(key, AES.MODE_ECB)
	ciphertext = bytearray(obj.encrypt(bytes(buffer)))
	return ciphertext

def  aes_128_ecb_dec(buffer,key):
	obj = AES.new(key, AES.MODE_ECB)
	plaintext = bytearray(obj.decrypt(bytes(buffer)))
	return plaintext

def pad_pkcs7(buffer, block_size):
	if len(buffer) % block_size:
		padding = (len(buffer)/block_size + 1 ) * block_size - len(buffer)
	else:
		padding = 0

	assert 0<= padding <= 255
	new_buffer = bytearray()
	new_buffer[:] = buffer
	new_buffer += bytearray([chr(padding)] * padding)
	return new_buffer

def  unpad_pkcs7(buffer):
	padding = buffer[-1]
	for i in range(len(buffer)- 1, len(buffer) - padding, -1):
		if buffer[i] != buffer[-1]:
			return buffer
	new_buffer = bytearray()
	new_buffer[:] = buffer[:-padding]
	return new_buffer

def aes_128_cbc_enc(buffer, key, iv):
	plaintext = pad_pkcs7(buffer, AES.block_size)
	ciphertext = bytearray(len(plaintext))
	prev_block = iv

	for i in range(0, len(plaintext), AES.block_size):
		ciphertext[i: i+ AES.block_size] = aes_128_ecb_enc(xor(plaintext[i: i + AES.block_size], prev_block),key)
		prev_block = ciphertext[i: i + AES.block_size]

	return ciphertext

def aes_128_cbc_dec(ciphertext, key, iv):
	plaintext = bytearray(len(ciphertext))
	prev_block = iv
	for i in range(0, len(ciphertext), AES.block_size):
		plaintext[i: i + AES.block_size] = xor(aes_128_ecb_dec(bytes(ciphertext[i: i+ AES.block_size]), key), prev_block)
		prev_block = ciphertext[i : i + AES.block_size]

	return unpad_pkcs7(plaintext)

def random_key(length):
	key = bytearray(length)
	for i in range(length):
		key[i] = chr(randint(0,255))
	return key

def encryption_oracle(buffer):
	bytes_to_add = randint(5, 10)
	plaintext = pad_pkcs7(random_key(bytes_to_add) + buffer +random_key(bytes_to_add), AES.block_size)

	key = bytes(random_key(16))

	if randint(0, 1):
		return aes_128_ecb_enc(plaintext,key)
	else:
		iv = random_key(16)
		return aes_128_cbc_enc(plaintext,key,iv)

# print encryption_oracle(bytearray("hatake pham"))
# test encryption_oracle


def  repeated_blocks(buffer, block_length=16):
	reps = defaultdict(lambda: -1)
	for i in range(0, len(buffer), block_length):
		block = bytes(buffer[i:i+block_length])
		reps[block] += 1
	return sum(reps.values())

def is_ecb_mode(buffer,block_size):
	return repeated_blocks(buffer, block_size) > 0


plaintext = bytearray("".join(list(open("ch11.txt","r"))))
for i in range(1000):

	ciphertext = encryption_oracle(plaintext)
	print is_ecb_mode(ciphertext, AES.block_size)
	if is_ecb_mode(ciphertext, AES.block_size):
		print "Detection work"
		exit()

print "Detection not work"
# kiem tra ham check ecb bang vong lap 1000 lan, sau 1000 lan ko ra thi la sai

