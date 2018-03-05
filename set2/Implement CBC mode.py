from Crypto.Cipher import AES


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


string = "hatake pham"
plaintext = bytearray(string)
iv = bytearray([chr(0)] * AES.block_size)
print "".join("%02x" % b for b in iv)
iv1  = '0000000000000000000000000000000c'
iv2 = bytearray.fromhex(iv1)
hex = "".join("%02x" % b for b in iv2)
print hex

key = "YELLOW SUNMARINE"

a = aes_128_cbc_enc(plaintext, key, iv2)
print a
b = aes_128_cbc_dec(a, key, iv2)
print b

# kiem tra lai ham

# ciphertext = bytearray("".join(list(open("ch10.txt","r"))).decode("base64"))
# print aes_128_cbc_dec(ciphertext, key, iv)