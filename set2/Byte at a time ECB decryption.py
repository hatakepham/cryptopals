from Crypto.Cipher import AES
from random import randint
from collections import defaultdict

def repeated_blocks(buffer, block_length=16):
    reps = defaultdict(lambda: -1)
    for i in range(0, len(buffer), block_length):
        block = bytes(buffer[i:i + block_length])
        reps[block] += 1
    return sum(reps.values())

    # ham tinh cac khoi giong nhau, ham tre ve sum khoi de xac dinh ecb

def pad_pkcs7(buffer, block_size):
    if len(buffer) % block_size:
        padding = (len(buffer) / block_size + 1) * block_size - len(buffer)
    else:
        padding = 0 
    assert 0 <= padding <= 255
    new_buffer = bytearray()
    new_buffer[:] = buffer
    new_buffer += bytearray([chr(padding)] * padding)
    return new_buffer

    # ham padding

def random_key(length):
    key = bytearray(length)
    for i in range(length):
        key[i] = chr(randint(0, 255)) 
    return key

# tao key random
key = bytes(random_key(16))

def aes_128_ecb_enc(buffer, key):
    obj = AES.new(key, AES.MODE_ECB)
    return bytearray(obj.encrypt(bytes(buffer)))

# ham encryp ecb

def encryption_oracle(data):
    unknown_string = bytearray((
        "Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkg\n" +
        "aGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBq\n" +
        "dXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUg\n" +
        "YnkK"
    ).decode("base64"))
    plaintext = pad_pkcs7(
        data + unknown_string,
        AES.block_size,
    )
    return aes_128_ecb_enc(plaintext, key)

def get_block_size(encryption_oracle):
    ciphertext_length = len(encryption_oracle(bytearray()))
    i = 1
    while True:
        data = bytearray("A" * i)
        new_ciphertext_length = len(encryption_oracle(data))
        if ciphertext_length != new_ciphertext_length:
            return new_ciphertext_length - ciphertext_length
        i += 1

# xac dinh do dai block

def is_ecb_mode(buffer, block_size):
    return repeated_blocks(buffer, block_size) > 0

def get_unknown_string_size(encryption_oracle):
    ciphertext_length = len(encryption_oracle(bytearray()))
    i = 1
    while True:
        data = bytearray("A" * i)
        new_ciphertext_length = len(encryption_oracle(data))
        if ciphertext_length != new_ciphertext_length:
            return (new_ciphertext_length - i - (new_ciphertext_length - ciphertext_length))
        i += 1
#xac dinh do dai unknow string 

def get_unknown_string(encryption_oracle):
    block_size = get_block_size(encryption_oracle)
    is_ecb = is_ecb_mode(
        encryption_oracle(bytearray("YELLOW SUBMARINE" * 2)),
        block_size,
    )
    assert is_ecb
    unknown_string_size = get_unknown_string_size(encryption_oracle)

    unknown_string = bytearray()
    unknown_string_size_rounded = ((unknown_string_size / block_size) + 1) * block_size
    for i in range(unknown_string_size_rounded - 1, 0, -1):
        d1 = bytearray("A" * i)
        c1 = encryption_oracle(d1)[:unknown_string_size_rounded]
        for c in range(256):
            d2 = d1[:] + unknown_string + chr(c)
            c2 = encryption_oracle(d2)[:unknown_string_size_rounded]
            if c1 == c2:
                unknown_string += chr(c)
                break
    return unknown_string

print get_unknown_string(encryption_oracle)
