from Crypto.Cipher import AES

obj = AES.new('YELLOW SUBMARINE', AES.MODE_ECB)

ciphertext = "".join(list(open("ch7.txt","r"))).decode("base64")

plaintext = obj.decrypt(ciphertext)
print plaintext
