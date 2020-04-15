from aes import *
import numpy as np

class AESnShifrRow:
	"""
	Class for AES-128 encryption with CBC mode and PKCS#7.

	This is a raw implementation of AES, without key stretching or IV
	management. Unless you need that, please use `encrypt` and `decrypt`.
	"""
	rounds_by_key_size = {16: 10, 24: 12, 32: 14}
	def __init__(self, master_key):
		"""
		Initializes the object with a given key.
		"""
		assert len(master_key) in AES.rounds_by_key_size
		self.n_rounds = AES.rounds_by_key_size[len(master_key)]
		self._key_matrices = self._expand_key(master_key)

	def _expand_key(self, master_key):
		"""
		Expands and returns a list of key matrices for the given master_key.
		"""
		# Initialize round keys with raw key material.
		key_columns = bytes2matrix(master_key)
		iteration_size = len(master_key) // 4

		# Each iteration has exactly as many columns as the key material.
		columns_per_iteration = len(key_columns)
		i = 1
		while len(key_columns) < (self.n_rounds + 1) * 4:
			# Copy previous word.
			word = list(key_columns[-1])

			# Perform schedule_core once every "row".
			if len(key_columns) % iteration_size == 0:
				# Circular shift.
				word.append(word.pop(0))
				# Map to S-BOX.
				word = [s_box[b] for b in word]
				# XOR with first byte of R-CON, since the others bytes of R-CON are 0.
				word[0] ^= r_con[i]
				i += 1
			elif len(master_key) == 32 and len(key_columns) % iteration_size == 4:
				# Run word through S-box in the fourth iteration when using a
				# 256-bit key.
				word = [s_box[b] for b in word]

			# XOR with equivalent word from previous iteration.
			word = xor_bytes(word, key_columns[-iteration_size])
			key_columns.append(word)

		# Group key words in 4x4 byte matrices.
		return [key_columns[4*i : 4*(i+1)] for i in range(len(key_columns) // 4)]

	def encrypt_block(self, plaintext):
		"""
		Encrypts a single block of 16 byte long plaintext.
		"""
		assert len(plaintext) == 16

		plain_state = bytes2matrix(plaintext)

		add_round_key(plain_state, self._key_matrices[0])

		for i in range(1, self.n_rounds):
			sub_bytes(plain_state)
			mix_columns(plain_state)
			add_round_key(plain_state, self._key_matrices[i])

		sub_bytes(plain_state)
		add_round_key(plain_state, self._key_matrices[-1])

		return matrix2bytes(plain_state)

	def decrypt_block(self, ciphertext):
		"""
		Decrypts a single block of 16 byte long ciphertext.
		"""
		assert len(ciphertext) == 16

		cipher_state = bytes2matrix(ciphertext)

		add_round_key(cipher_state, self._key_matrices[-1])
		inv_sub_bytes(cipher_state)

		for i in range(self.n_rounds - 1, 0, -1):
			add_round_key(cipher_state, self._key_matrices[i])
			inv_mix_columns(cipher_state)
			inv_sub_bytes(cipher_state)

		add_round_key(cipher_state, self._key_matrices[0])

		return matrix2bytes(cipher_state)

def encrypt (key, ptext):
	return AESnShifrRow(key).encrypt(ptext)

def check(plaintext, ciphertext, key):
	if encrypt(key, plaintext) == ciphertext:
		print('Key is correct!')


def toInt(byte_arr):
	return int.from_bytes(byte_arr, byteorder='big')

def printAsHexInt(byte_arr):
	print(hex(toInt(byte_arr)))

if __name__ == "__main__":
	plaintext = 0xcb7488bac2092786d915c713a05c5bcf.to_bytes(16, byteorder='big')
	key = 0x9246351a1af86adc5be32acdd45be2e4.to_bytes(16, byteorder='big')
	ciphertext = AESnShifrRow(key).encrypt_block(plaintext)

	print("plaintext")
	print(bytes2matrix(plaintext))
	print("key")
	print(bytes2matrix(key))
	print("ciphertext")
	print(bytes2matrix(ciphertext))

	bruteforcedKey = np.zeros(16, dtype=int)

	for i in range(4):

		pSlice = np.zeros(16, dtype=int)
		cExpectedSlice = np.zeros(16, dtype=int)
		for j in range(4):
			pSlice[j + 4*i] = plaintext[j + 4*i]
			cExpectedSlice[j + 4*i] = ciphertext[j + 4*i]
		
		cExpectedSliceInt = toInt(cExpectedSlice)
		
		print("Slice " + str(i))
		# print(pSlice)
		# print(cSlice)

		# bruteforcing key
		maxSliceSize = 1 << 32
		for x in range(maxSliceSize):
			keySlice = x << ((3-i) * 32)
			keySlice = keySlice.to_bytes(16, byteorder='big')
			cSlice = AESnShifrRow(keySlice).encrypt_block(pSlice)

			if toInt(cSlice) == cExpectedSliceInt:
				printAsHexInt(keySlice)
				for j in range(4):
					bruteforcedKey[j + 4*i] = keySlice[j + 4*i]
				break

check(plaintext, ciphertext, bruteforcedKey)
printAsHexInt(bruteforcedKey)