#! /usr/bin/env python2

import unittest
import numpy as np


def calculatePearsonCoefficient(x, y):
	# copy-paste your function definition for calculatePearsonCoefficient()
	# instead of this stub
	

class TestCalculatePearsonCoefficient(unittest.TestCase):

	def test_pearson_equal(self):
		x = np.arange(8)
		y = x
		self.assertEqual(calculatePearsonCoefficient(x, y), 1.0)

	def test_pearson_opposite(self):
		x = np.arange(8)
		y = -1*x
		self.assertEqual(calculatePearsonCoefficient(x, y), -1.0)

	def test_pearson_uncorrelated(self):
		x = np.arange(8)
		y = np.array([186, 218, 15, 225, 1, 226, 118, 102])
		self.assertEqual(calculatePearsonCoefficient(x, y), -0.21459959410742252)

if __name__ == '__main__':
	suite = unittest.TestLoader().loadTestsFromTestCase(TestCalculatePearsonCoefficient)
	unittest.TextTestRunner(verbosity = 2).run(suite)
