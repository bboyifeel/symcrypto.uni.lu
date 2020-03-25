import sys
import numpy as np

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


def stateStringToArray(strState):
	arr = np.zeros(len(strState), int)
	for i in range(len(strState)):
		if strState[i] == "1":
			arr[i] = 1
		else:
			arr[i] = 0
	return arr


def powMatrix(matrix, exponent, mod):
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
	initialState = stateStringToArray(initialState)
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
	initialState = stateStringToArray(initialState)
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


task_1_1_1()