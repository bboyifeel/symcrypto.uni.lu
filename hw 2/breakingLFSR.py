import sys
import numpy as np
import math

class LFSR(object):
	def __init__(self, n, taps):
		self.n = n

		self.taps = tuple(taps)
		assert self.taps[0] == 0
		assert 0 <= min(self.taps) <= max(self.taps) <= n - 1
		self.state = (0,) * n

	def init(self, state):
		assert len(state) == self.n
		self.state = tuple(state)

	def init_random(self):
		self.state = tuple(randint(0, 1) for _ in xrange(self.n))

	def clock(self):
		output = self.state[0]
		new_val = 0
		for t in self.taps:
			new_val ^= self.state[t]
		self.state = self.state[1:] + (new_val,)
		return output

	def filter(self, eq):
		"""Example:
		eq = [(0, 2), (4, 20), (3,), (7,)]
		corresponds to filter
		s0*s2 + s4*s20 + s3 + s7
		"""
		output = 0
		for monomial in eq:
			monomial_value = 1
			for varindex in monomial:
				monomial_value &= self.state[varindex]
			output ^= monomial_value
		return output

	def __str__(self):
		output = ""
		for i in reversed(xrange(0, self.n)):
			# reversed because we print S_0 to the right
			output += str(self.state[i])
		return output


def binaryStringToArray(strState):
	""" Converts string of type 1001101 into np array """
	arr = np.zeros(len(strState), int)
	for i in range(len(strState)):
		if strState[i] == "1":
			arr[i] = 1
		else:
			arr[i] = 0
	return arr


def powMatrix(matrix, exponent, mod):
	""" Square ad multipy algorithm for matrices
		(takes modulo every element) """
	prod = np.identity(np.size(matrix[0]), int)
	
	if exponent == 0:
		return np.identity(np.size(matrix[0]), int)

	matrix = np.copy(matrix)

	while exponent > 0:
		if exponent & 1 == 1:
			prod = np.dot(matrix, prod)
			prod = np.mod(prod, mod)

		matrix = np.dot(matrix, matrix)
		matrix = np.mod(matrix, mod)
		exponent /= 2

	return prod


def task_1_1_1():
	initialState = "11110101011001111011100000011010010001111001111011111000000001101111110000011001101000101010100010011101001110111011111001011001"
	initialState = binaryStringToArray(initialState)
	taps = [0, 1, 41, 45]
	lfsr = LFSR(128, taps)
	lfsr.init(initialState)
	print("Initial state: " + str(lfsr))

	cipherSize = 256
	keyStream = np.zeros(0, int)
	for i in range(cipherSize):
		keyBit = lfsr.clock()
		keyStream = np.append(keyStream, keyBit)
	print(keyStream)


def task_1_1_1_matrices():
	initialState = "10011010011111011101110010111001000101010100010110011000001111110110000000011111011110011110001001011000000111011110011010101111"
	initialState = binaryStringToArray(initialState)
	exponent = 256

	taps = np.zeros(len(initialState), int)
	taps[0]  = 1
	taps[1]  = 1
	taps[41] = 1
	taps[45] = 1
	taps = taps[::-1]
	taps = np.array([taps])

	A = np.identity(len(initialState), int)
	A = A[::-1]
	A = np.delete(A, 0, axis = 0)
	A = np.append(A, taps, axis = 0)
	A = A[::-1]

	keyStream = np.zeros(0, int)
	for i in range(exponent):
		AtoI = powMatrix(A, i, 2)
		finalState  = np.dot(AtoI, initialState)
		finalState  = np.mod(finalState, 2)
		keyStream = np.append(keyStream, finalState[len(initialState)-1])
	print(keyStream)


def task_1_1_2():
	exponent = pow(2, 64) + 25

	taps = np.zeros(128, int)
	taps[0]  = 1
	taps[1]  = 1
	taps[41] = 1
	taps[45] = 1
	taps = taps[::-1]
	taps = np.array([taps])

	A = np.identity(128, int)
	A = A[::-1]
	A = np.delete(A, 0, axis = 0)
	A = np.append(A, taps, axis = 0)
	A = A[::-1]

	AtoThePower = powMatrix(A, exponent, 2)
	initialState = np.ones(128, int)
	finalState  = np.dot(AtoThePower, initialState)
	finalState  = np.mod(finalState, 2)

	print(finalState)


def compareTwoArrays(first, second):
	""" Compares two arrays and 
		returs similarity persentage as int value"""

	assert len(first) == len(second)

	result = 0

	for i in range(len(first)):
		if first[i]==second[i]:
			result += 1

	result = 100 * result / len(first)

	return result


""" lamda to convert int into binary string of a size n """
get_bin = lambda x, n: format(x, 'b').zfill(n)


def x2(x0, x1, s):
	""" Reverse engineering for a given function """

	x2 = -1

	if(x0 == 0 and x1 == 0 and s == 0):
		x2 = 0
	elif (x0 == 0 and x1 == 0 and s == 0):
		x2 = 1
	elif (x0 == 1 and x1 == 1 and s == 1):
		x2 = 0
	elif (x0 == 1 and x1 == 1 and s == 0):
		x2 = 1

	return x2


def bruteforceGeffeLike():
	""" Correlation attack on Geffe-like stream cipher """

	# given output (ciphertext)
	geffesOutput = "11100000011100010000010000011000111111010010010011100111011011101101001111110101101000111111000101001110110010100100111100010101101110100101001100100011000010011001011100110011110011111010101001000101"
	geffesOutput = binaryStringToArray(geffesOutput)

	# bruteforcing L_0
	print("Bruteforcing LFSR 0")
	taps = [0, 1, 4, 7]
	lfsr0 = LFSR(16, taps)
	lfsr0Stream = 0

	for i in range(1, int(math.pow(2,16))):
		
		initialState = get_bin(i, 16)
		initialState = binaryStringToArray(initialState)
		keyStream    = np.zeros(0, int)
		lfsr0.init(initialState)

		for j in range(len(geffesOutput)):
			keyBit = lfsr0.clock()
			keyStream = np.append(keyStream, keyBit)
		
		percentage = compareTwoArrays(keyStream, geffesOutput)
		
		if (percentage < 35):
			lfsr0Stream = keyStream

			initialState = get_bin(i, 16)
			initialState = binaryStringToArray(initialState)
			lfsr0.init(initialState)

			print("Key " + str(i) + " - " + str(percentage) + "%")
			print("Initial state " + str(lfsr0))
			
	
	# bruteforcing L_1
	print("Bruteforcing LFSR 1")

	taps = [0, 1, 7, 11]
	lfsr1 = LFSR(16, taps)
	lfsr1Stream = 0
	
	for i in range(1, int(math.pow(2,16))):
		
		initialState = get_bin(i, 16)
		initialState = binaryStringToArray(initialState)
		keyStream    = np.zeros(0, int)
		lfsr1.init(initialState)

		for j in range(len(geffesOutput)):
			keyBit = lfsr1.clock()
			keyStream = np.append(keyStream, keyBit)
		
		percentage = compareTwoArrays(keyStream, geffesOutput)
		
		if (percentage > 70):
			lfsr1Stream = keyStream

			initialState = get_bin(i, 16)
			initialState = binaryStringToArray(initialState)
			lfsr1.init(initialState)
			
			print(str(i) + " - " + str(percentage) + "%")
			print(lfsr1)

	# Reverse engineering L_2
	lfsr2Stream = np.zeros(0, int)
	for i in range(len(geffesOutput)):
		lfsr2Stream = np.append(lfsr2Stream, x2(lfsr0Stream[i], lfsr1Stream[i], geffesOutput[i]))

	print(lfsr2Stream)

# main
bruteforceGeffeLike()