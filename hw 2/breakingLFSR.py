import sys
import numpy as np

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

def breakingLFSR():
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
	initalState = np.ones(128, int)
	finalState  = np.dot(AtoThePower, initalState)
	finalState  = np.mod(finalState, 2)

	print(finalState)

def stateStringToArray(strState):
	arr = np.zeros(len(strState), int)
	for i in range(len(strState)):
		if strState[i] == "1":
			arr[i] = 1
		else:
			arr[i] = 0
	return arr

def generateLFSRStates():
	exponent = 256

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

	print(A)
	
	initalState = "10011010011111011101110010111001000101010100010110011000001111110110000000011111011110011110001001011000000111011110011010101111"
	initalState = stateStringToArray(initalState)

	keyStream = np.zeros(0, int)
	for i in range(exponent):
		AtoI = powMatrix(A, i, 2)
		finalState  = np.dot(AtoI, initalState)
		finalState  = np.mod(finalState, 2)
		keyStream = np.append(keyStream, finalState[127])

	print(keyStream)
		

breakingLFSR()