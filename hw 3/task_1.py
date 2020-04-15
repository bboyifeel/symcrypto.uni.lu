from aes import *
import numpy as np


def printInHex(arr):
	print(' '.join([hex(i) for i in arr]))

def subtask_1():
	a = [0x12, 0xa0, 0xd7, 0xb4]
	for i in range(12):
		a.append(0)

	a = bytes2matrix(a)
	print("a: ")
	printInHex(a[0])

	sub_bytes(a)
	mix_columns(a)
	
	b = a
	print("b: ")
	printInHex(b[0])

	# d - delta
	d = [0xd9, 0x14, 0x4f, 0x40]
	print("d: ")
	printInHex(d)

	bstar = b
	bstar[0] = np.bitwise_xor(bstar[0], d)
	print("bstar: ")
	printInHex(bstar[0])

	inv_mix_columns(bstar)
	inv_sub_bytes(bstar)

	astar = bstar
	print("astar: ")
	printInHex(astar[0])

if __name__ == "__main__":
	subtask_1()