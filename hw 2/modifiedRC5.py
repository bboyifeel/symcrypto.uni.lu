import numpy as np
from breakingLFSR import *

def cyclic_rotation_left(block, rotations):
	rotations %= len(block)
	l = block[:rotations]
	r = block[rotations:]
	return np.concatenate([r,l])


def cyclic_rotation_right(block, rotations):
	rotations %= len(block)
	l = block[:len(block) - rotations]
	r = block[len(block) - rotations:]
	return np.concatenate([r,l])


def mrc5_encrypt(block, key, rounds):
	assert len(block) == len(key)
	# x1 - x left, x1 - x right
	x0 = block[:len(block)//2]
	x1 = block[len(block)//2:]
	k0 = key[:len(key)//2]
	k1 = key[len(key)//2:]

	for i in range(rounds):
		x0 = np.bitwise_xor(x0, x1)
		x0 = cyclic_rotation_left(x0, 7)
		x0 = np.bitwise_xor(x0, k0)
		x1 = np.bitwise_xor(x0, x1)
		x1 = cyclic_rotation_left(x1, 7)
		x1 = np.bitwise_xor(x1, k1)

	return np.concatenate([x0, x1])


def mrc5_decrypt(block, key, rounds):
	assert len(block) == len(key)
	# x1 - x left, x1 - x right
	x0 = block[:len(block)//2]
	x1 = block[len(block)//2:]
	k0 = key[:len(key)//2]
	k1 = key[len(key)//2:]

	for i in range(rounds):
		x1 = np.bitwise_xor(x1, k1)
		x1 = cyclic_rotation_right(x1, 7)
		x1 = np.bitwise_xor(x0, x1)
		
		x0 = np.bitwise_xor(x0, k0)
		x0 = cyclic_rotation_right(x0, 7)
		x0 = np.bitwise_xor(x0, x1)
		
	return np.concatenate([x0, x1])


def testEncryption():
	block = "1110000001110001000001000001100011111101001001001110011101101110"
	key   = "1101001111110101101000111111000101001110110010100100111100010101"
	block = binaryStringToArray(block)
	key	  = binaryStringToArray(key)

	print("Plaintext " + str(block))

	result = mrc5_encrypt(block, key, 12)
	print("Ciphertext " + str(result))
	
	result = mrc5_decrypt(result, key, 12)
	print("Decoded " + str(result))


def breaking_mrc5_demonstration():

	"""https://crypto.stackexchange.com/questions/29804/given-a-linear-block-cipher-how-can-an-attacker-decrypt-any-plaintext-value-encr"""
	
	key   = "1101001111110101101000111111000101001110110010100100111100010101"
	key	  = binaryStringToArray(key)
	
	M     = np.empty([64,0], int)
	toEncrypt = np.zeros(64, int)
	toEncrypt[63] = 1
	
	for i in range(64):
		toEncrypt = cyclic_rotation_right(toEncrypt, 1)
		column = mrc5_decrypt(toEncrypt, key, 12)
		M = np.column_stack((M, column))
	print M

	block = "1110000001110001000001000001100011111101001001001110011101101110"
	block = binaryStringToArray(block)

	ciphertext = mrc5_encrypt(block, key, 12)

	encrypted  = np.dot(M, block)
	encrypted  = np.mod(encrypted, 2)

	print("ciphertext " + str(ciphertext))
	print("encrypted  " + str(encrypted))


def breaking_mrc5():

	"""https://crypto.stackexchange.com/questions/29804/given-a-linear-block-cipher-how-can-an-attacker-decrypt-any-plaintext-value-encr"""
	
	key   = "1101001111110101101000111111000101001110110010100100111100010101"
	key	  = binaryStringToArray(key)

	block = "1110000001110001000001000001100011111101001001001110011101101110"
	block = binaryStringToArray(block)

	ciphertext = mrc5_encrypt(block, key, 12)

	B_k = mrc5_encrypt(np.zeros(64, int), key, 12)
	A_k = mrc5_encrypt(block, np.zeros(64, int), 12)

	cracked = np.bitwise_xor(A_k, B_k)

	print("ciphertext " + str(ciphertext))
	print("cracked " + str(cracked))


breaking_mrc5()