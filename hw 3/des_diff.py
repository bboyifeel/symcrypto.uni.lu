"""subtask 1"""
x = 0x25
delta_in = 0x01
delta_out = 0x06


S = [[14,  4, 13,  1,  2, 15, 11,  8,  3, 10,  6, 12,  5,  9,  0,  7],
	 [ 0, 15,  7,  4, 14,  2, 13,  1, 10,  6, 12, 11,  9,  5,  3,  8],
	 [ 4,  1, 14,  8, 13,  6,  2, 11, 15, 12,  9,  7,  3, 10,  5,  0],
	 [15, 12,  8,  2,  4,  9,  1,  7,  5, 11,  3, 14, 10,  0,  6, 13]]


def fi(x, k):
	x ^= k

	y = (x & int('011110',2)) >> 1
	r = (x & int('100000',2)) >> 4 ^ (x & 1)

	return S[r][y]

def subtask_1():
	kmax = 1 << 6
	for k in range(kmax):
		if (fi(x,k) ^ fi(x^delta_in, k)) == delta_out:
			print(hex(k))

"""subtask 2"""

def calc_deltas(ciphertext_diff):
	delta_1 = 0x04000000
	delta_2 = 0x405c0000

	delta_6 = ciphertext_diff >> 32
	delta_4 = ciphertext_diff & ((1 << 32) - 1)

	delta_5 = delta_6 ^ delta_2
	delta_3 = delta_4 ^ delta_1

	print("delta_1: " + str(hex(delta_1)))
	print("delta_2: " + str(hex(delta_2)))
	print("delta_3: " + str(hex(delta_3)))
	print("delta_4: " + str(hex(delta_4)))
	print("delta_5: " + str(hex(delta_5)))
	print("delta_6: " + str(hex(delta_6)))

	print("[f] delta_2 to delta_3: " + str(hex(delta_2)) + " -> " + str(hex(delta_3)))
	print("[f] delta_4 to delta_5: " + str(hex(delta_4)) + " -> " + str(hex(delta_5)))


def subtask_2():
	p1 = 0xf136991ac246bdc7
	c1 = 0x953f1ad872392f41

	p1star = 0xb16a991ac646bdc7
	c1star = 0x2bec91cdf678be07

	# print(hex(p1^p1star))
	# print(hex(c1^c1star))

	print("deltas for c1 and c1*")
	calc_deltas(c1^c1star)

	p2 = 0xe37ab19adfaddc95
	c2 = 0xf7489e506f3f9529

	p2star = 0xa326b19adbaddc95
	c2star = 0xcfa1d97cebff856b

	# print(hex(p2^p2star))
	# print(hex(c2^c2star))

	print("deltas for c2 and c2*")
	calc_deltas(c2^c2star)


if __name__ == "__main__":
	subtask_2()