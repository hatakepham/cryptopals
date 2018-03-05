def pad_pksc7(buffer, block_size):
	if len(buffer) % block_size:
		padding = (len(buffer) / block_size + 1) * block_size - len(buffer)
	else:
		padding = 0
		# tinh padding

	assert 0 <= padding <= 255
	new_buffer = bytearray()
	new_buffer[:] = buffer
	new_buffer += bytearray([chr(padding)] * padding)
	#add padding
	return new_buffer

def  unpad_pkcs7(buffer):
	padding = buffer[-1]
	for i in range(len(buffer)- 1, len(buffer) - padding, -1):
		if buffer[i] != buffer[-1]:
			return buffer
	new_buffer = bytearray()
	new_buffer[:] = buffer[:-padding]
	return new_buffer
	#ham unpad

buffer = bytearray("YELLOW SUBMARINE")
a = pad_pksc7(buffer, 20)

hex = "".join("%02x" % b for b in a)
print hex
print unpad_pkcs7(a)