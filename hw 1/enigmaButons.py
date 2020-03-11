#!/usr/bin/python

import logging

KLEN = 3 # length of the key
# Identity permutation
I = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

class EnigmaButons():
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

	def isInvolution(self, np, nc):
		for i in range(len(np)):
			pos = np.find(nc[i])
			if pos != -1:
				if np[i] != nc[pos]:
					return False
		return True
					

	def checkInvolution(self, np, nc, spacePos):
		lnp = np[:spacePos]
		rnp = np[spacePos:]
		lnc = nc[:spacePos]
		rnc = nc[spacePos:]

		print lnp + " " + rnp
		print lnc + " " + rnc

		isInvolution = self.isInvolution(lnp, lnc)
		if isInvolution:
			isInvolution = self.isInvolution(rnp, rnc)
		print "isInvolution: " + str(isInvolution)
		print "_____"


	def bruteforce(self):
		if (len(self.plaintext) != len(self.ciphertext)):
			print "plaintext size != ciphertext size"
			return 0
		for initialState in range(26):  # initial state of the right-most rotor
			state = initialState
			print self.toLetter(state)
			
			np = list()
			nc = list()

			for c in self.plaintext:
				state = (state + 1) % 26
				c = (c + state) % 26
				c = self.R3[c]
				c = (c - state + 26) % 26
				np.append(c)

			state = initialState # initial state of the right-most rotor
			for c in self.ciphertext:
				state = (state + 1) % 26
				c = (c + state) % 26
				c = self.R3[c]
				c = (c - state + 26) % 26
				nc.append(c)

			np_letters = self.toLetters(np)
			nc_letters = self.toLetters(nc)

			spacePos = (self.toNumber("V") - initialState + 26) % 26
			if spacePos == 0:
				spacePos = 26

			self.checkInvolution(np_letters, nc_letters, spacePos)


if __name__ == '__main__':
	plaintext = "FORAREASONEVERYTHINGHAPPENS"
	ciphertext = "WTWGYPBQJRXANMXMUPRCYPZZVLT"

	e = EnigmaButons(plaintext, ciphertext)
	e.bruteforce()