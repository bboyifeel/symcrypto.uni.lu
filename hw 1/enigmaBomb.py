#!/usr/bin/python

import logging
from copy import deepcopy

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
	def __init__(self):
		# TP stands for turn point
		self.R1_ = "EKMFLGDQVZNTOWYHXUSPAIBRCJ" # Rotor I
		self.R2_ = "AJDKSIRUXBLHWTMCQGZNPYFVOE" # Rotor II
		self.R3_ = "BDFHJLCPRTXVZNYEIWGAKMUSQO" # Rotor III
		self.B_  = "YRUHQSLDPXNGOKMIEBFZCWVJAT" # B is the reflector

		self.R1 = self.toNumbers(self.R1_)
		self.R2 = self.toNumbers(self.R2_)
		self.R3 = self.toNumbers(self.R3_)
		self.B = self.toNumbers(self.B_)

		self.rev_R1 = [0 for i in range(26)]
		self.rev_R2 = [0 for i in range(26)]
		self.rev_R3 = [0 for i in range(26)]
		for i in range(26):
			self.rev_R1[self.R1[i]] = i
			self.rev_R2[self.R2[i]] = i
			self.rev_R3[self.R3[i]] = i

		self.rotors = [self.R1, self.R2, self.R3]
		self.rev_rotors = [self.rev_R1,self.rev_R2,self.rev_R3]
		return None

	def encrypt(self, l, initialState, offset):
		state = deepcopy(initialState)
		state[2] = (state[2] + offset) % 26
		c = l
		# ROTORS FORWARD
		for i in reversed(range(len(self.rotors))):
			c = (c + state[i]) % 26
			c = self.rotors[i][c]
			c = (c - state[i]) % 26

		# REFLECTOR
		c = self.B[c]

		# ROTORS BACKWARDS

		for i in range(len(self.rotors)):
			c = (c + state[i]) % 26
			c = self.rev_rotors[i][c]
			c = (c - state[i]) % 26

		return c

	def bruteforce(self):
		for l in range(26):
			for m in range(26):
				for n in range(26):
					state = [l, m, n]
					for letter in range(26):
						# DQ
						result = self.encrypt(letter, state, 1)
						result = self.encrypt(result, state, 6)

						if (result == letter):
							# DQOL through 12
							result = self.encrypt(letter, state, 1)
							result = self.encrypt(result, state, 2)
							result = self.encrypt(result, state, 4)
							result = self.encrypt(result, state, 11)
							result = self.encrypt(result, state, 6)
							
							if (result == letter):
								# DQOL through 11
								result = self.encrypt(letter, state, 1)
								result = self.encrypt(result, state, 2)
								result = self.encrypt(result, state, 8)
								result = self.encrypt(result, state, 7)
								result = self.encrypt(result, state, 4)
								result = self.encrypt(result, state, 11)
								result = self.encrypt(result, state, 6)								
							
								if (result == letter):
									print(self.toLetter(l) + self.toLetter(m) + self.toLetter(n) + " " + self.toLetter(letter))


if __name__ == '__main__':
	e = EnigmaBomb()
	e.bruteforce()