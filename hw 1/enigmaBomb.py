#!/usr/bin/python

import logging

KLEN = 3 # length of the key
# Identity permutation
I = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

class EnigmaBomb():
	def toNumber(self, letter):
		return I.index(letter)

	def toNumbers(self, letters):
		numbers = [self.toNumber(c) for c in letters]
		return numbers

	def toLetter(self, number):
		return I[number]

	def toLetters(self, numbers):
		letters = "".join(([self.toLetter(n) for n in numbers]))
		return letters

	# to the initial position of rotor I (left-most rotor, i.e. the closest to the reflector)
	# R3 is the right-most rotor (closest to the plugboard/keyboard)
	def __init__(self, plaintext, ciphertext):
		# TP stands for turn point
		self.R1_ = "EKMFLGDQVZNTOWYHXUSPAIBRCJ" # Rotor I
		self.R2_ = "AJDKSIRUXBLHWTMCQGZNPYFVOE" # Rotor II
		self.R3_ = "BDFHJLCPRTXVZNYEIWGAKMUSQO" # Rotor III
		self.B_   = "YRUHQSLDPXNGOKMIEBFZCWVJAT" # B is the reflector

		self.R1 = self.toNumbers(self.R1_)
		self.R2 = self.toNumbers(self.R2_)
		self.R3 = self.toNumbers(self.R3_)
		self.B = self.toNumbers(self.B_)

		self.plaintext_ = plaintext
		self.ciphertext_ = ciphertext
		self.plaintext = self.toNumbers(self.plaintext_)
		self.ciphertext = self.toNumbers(self.ciphertext_)
		return None

	def bruteforce(self):
		for i in range(26):
			for j in range(26):
				for k in range(26):
					for l in range(26):
						# cycle 1 UE (R1, R6)
						# cycle 2 ECT (R2, R4, R11)
						# cycle 3 CU (R7, R8)


if __name__ == '__main__':
	plaintext = "UEPTIUCCQSTIOV"
	ciphertext = "ECFCWEUURFEKZL"

	e = EnigmaBomb(plaintext, ciphertext)
	e.bruteforce()