
import codecs
Hex_String="49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d"

# encoded = Hex_String.decode("hex").encode("base64")
# python 2

encoded = codecs.encode(codecs.decode(Hex_String, 'hex'), 'base64').decode()

print (encoded)