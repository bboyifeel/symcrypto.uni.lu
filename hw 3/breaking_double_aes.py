from Crypto.Cipher import AES

def encrypt (key, ptext):
	return AES.new(key, AES.MODE_ECB).encrypt(ptext)

def decrypt(key, ctext):
	return AES.new(key, AES.MODE_ECB).decrypt(ctext)

def check(plaintext, ciphertext, key1, key2):
	if encrypt(key2, encrypt(key1, plaintext)) == ciphertext:
		print('Keys are correct!')

def crack():
	plaintext = 0xcb7488bac2092786d915c713a05c5bcf.to_bytes(16, byteorder='big')
	ciphertext = 0x9246351a1af86adc5be32acdd45be2e4.to_bytes(16, byteorder='big')

	dictionary = dict()

	keyRange = 1<<24

	print ("[start] build forward dictionary")
	for x in range(keyRange):
		x <<= 104
		key = x.to_bytes(16, byteorder='big')
		intermediate = int.from_bytes(encrypt(key, plaintext), byteorder='big')
		dictionary[intermediate] = key
	
	print ("[done] build forward dictionary")

	print ("[start] bruteforce")

	for x in range(keyRange):
		x <<= 104
		key = x.to_bytes(16, byteorder='big')
		intermediate = int.from_bytes(AES.new(key, AES.MODE_ECB).decrypt(ciphertext), byteorder='big')

		if intermediate in dictionary:
			key1 = dictionary[intermediate]
			key2 = key
	
			check(plaintext, ciphertext, key1, key2)
			
			key1 = int.from_bytes(key1, byteorder='big')
			key2 = int.from_bytes(key2, byteorder='big')
			print ("key 1: {}\nkey 2: {}".format(key1, key2))
			print ("IN HEX:")
			print ("key 1: {}\nkey 2: {}".format(hex(key1), hex(key2)))
			break

	print ("[done] bruteforce")


if __name__ == "__main__":
	crack()