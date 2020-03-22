import sys
import numpy as np

def powMatrix(matrix, exponent, mod):
	if exponent == 0:
		return matrix

	prod = np.identity(np.size(matrix[0]), int)

	while exponent > 0:
		if exponent & 1 == 1:
			prod = np.dot(matrix, prod)
			prod = np.mod(prod, mod)

		matrix = np.dot(matrix, matrix)
		matrix = np.mod(matrix, mod)

		exponent /= 2

	return prod

exponent = pow(2, 64) + 25
print(exponent)

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