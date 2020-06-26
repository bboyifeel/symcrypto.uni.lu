
################################################################################
# University of Luxembourg
# Laboratory of Algorithmics, Cryptology and Security (LACS)
#
# Side-channel attacks practical work
#
# Copyright (C) 2015 University of Luxembourg
################################################################################

"""
This module abstracts the target board (Arduino UNO). It can be used
as a module to be imported in other applications or as stand-alone
program to quickly test the communication between the PC and the arduino.
"""

from __future__ import print_function
import sys
import time
import platform
import serial

# Try to detect OS, so that we can use the correct serial port
if platform.system() == 'Windows':
	# Usually COM3 (COM1 & 2 are reserved)
	portName = 'COM3'
else:
	portName = '/dev/ttyACM0'

# Opcodes. Actually only one is defined
OP_ENCRYPT = 0x01

# Status codes
ST_READY = b'>'
ST_ERROR = b'?'

# Utility functions
def intToBytes(x:int):
	""" Convert a 16-byte integers into an array of 16 bytes (characters). 
	The least significant byte will have index 0 in the array

	Args:
		x : 16-byte integer

	Returns:
		array of 16 characters
	"""
	return x.to_bytes(16, 'little')

def bytesToInt(b):
	""" Converts an array on bytes (characters) into an integer. The last significant byte
	has index 0

	Args:
		b : array of characters

	Returns:
		corresponding unsigned int
	"""
	return int.from_bytes(b, 'little')
		
# Board driver
class Driver(object):
	"""
	Typical usage of the Driver class is illustrated below and in the __main__ section

		driver = Driver()
		p = 0x0
		c = driver.encrypt(p)
		print("p = 0x{0:032x}, c = 0x{1:032x}".format(p, c))
		driver.close()
	"""

	def __init__(self):
		""" Creates a Driver object and initiates communication with the arduino board.
		The driver will try to read the 10 first characters from the uart buffer until
		it finds the synchronization marker (i.e. ST_READY).
		"""
		self.port = serial.Serial(port = portName, baudrate = 38400, timeout = 1)
		time.sleep(1)
		for i in range(20):
			m = self.port.read(1)
			if m == ST_READY:
				break
		else:
			print("-- Synchronization error. Aborting...")
			sys.exit(-1)

	def close(self):
		""" Closes the communication between the PC and the arduino board
		The communication is no more possible after close() has been executed. A new
		Driver object must be created first.
		"""
		self.port.close()

	def encrypt(self, data):
		""" Encrypts data with AES-128 configured with hidden key.

		Args:
			data: integer (up to 128 bit)

		Returns:
			integer (up to 128 bit) containing the ciphertext
		"""
		req = bytes([OP_ENCRYPT])+ intToBytes(data)
		self.port.write(req)
		ciphertext = bytesToInt(self.port.read(16))
		return ciphertext


if __name__ == "__main__":
	driver = Driver()
	p = 0x0
	c = driver.encrypt(p)
	print("p = 0x{0:032x}, c = 0x{1:032x}".format(p, c))
	driver.close()
