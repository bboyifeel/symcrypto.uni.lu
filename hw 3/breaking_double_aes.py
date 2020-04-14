from Crypto.Cipher import AES

def toHexString(string):
	return ''.join(x.encode('hex') for x in string)

plaintext = "cb7488bac2092786d915c713a05c5bcf".decode("hex")
ciphertext = "9246351a1af86adc5be32acdd45be2e4".decode("hex")

dictionary = dict()

keyRange = 1<<24

print "[start] build forward dictionary"

for x in range(keyRange):
	key = "{0:06x}".format(x) + "00" * 13
	aes = AES.new(key.decode("hex"), AES.MODE_ECB)
	intermidiate = toHexString(aes.encrypt(plaintext))
	dictionary[intermidiate] = key

print "[done] build forward dictionary"

print "[start] bruteforce"

for x in range(keyRange):
	key = "{0:06x}".format(x) + "00" * 13
	aes = AES.new(key.decode("hex"), AES.MODE_ECB)

	intermidiate = toHexString(aes.decrypt(ciphertext))

	if intermidiate in dictionary:
		print "key 1: {} \nkey 2: {}".format(dictionary[intermidiate], key)
		break

print "[done] bruteforce"

# plaintext = "cb7488bac2092786d915c713a05c5bcf".decode("hex")

# key_1 = "fe355a00000000000000000000000000".decode("hex") 
# key_2 = "e5d97f00000000000000000000000000".decode("hex")

# aes = AES.new(key_1, AES.MODE_ECB)
# intermidiate = aes.encrypt(plaintext)
# aes = AES.new(key_2, AES.MODE_ECB)
# ciphertext = toHexString(aes.encrypt(intermidiate))

# print ciphertext
