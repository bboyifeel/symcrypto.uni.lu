
################################################################################
# University of Luxembourg
# Laboratory of Algorithmics, Cryptology and Security (LACS)
#
# Side-channel attacks practical work
#
# Copyright (C) 2015 University of Luxembourg
################################################################################

from __future__ import print_function
import sys
import time
from ctypes import *
from dwfconstants import *

"""This module abstracts the Analog Discovery oscilloscope. It depends on the
python SDK provided by Digilent Inc and provides high-level functions to
configure and get measurements in a simpler way.
"""

# Analog Discovery State
STATE_READY     = 0
STATE_CONFIG    = 4
STATE_PREFILL   = 5
STATE_ARMED     = 1
STATE_WAIT      = 7
STATE_TRIGGERED = 3
STATE_RUNNING   = 3
STATE_DONE      = 2


class Discovery(object):
	""" Abstraction for Analog Discovery Oscilloscope.

	Attributes:
		version(str)  : device version string
		dwf(DLL)      : link to DLL
		hdwf(int)     : device handle
		nChannels     : number of analog channels
		offsetMin     : minimum value for channel offset
		offsetMax     : maximum value for channel offset
		offsetSteps   : number of steps for channel offset
		fsMin         : minimum sampling frequency
		fsMax         : maximum sampling frequency
		nBits         : amplitude resolution
		bufferSizeMin : minimum buffer size
		bufferSizeMax : maximum buffer size

	Typical usage::

		import matplotlib.pyplot as plt
		import discovery

		scope = discovery.Discovery()
		scope.enableChannel(0)
		scope.enableChannel(1)
		scope.setOffset(0, 0.0)
		scope.setOffset(1, 0.0)
		scope.setMode('normal')
		scope.setTriggerEdge(1, 1.0, 'rising')
		time.sleep(1)
		scope.run()
		...
		while not scope.isReady():
			time.sleep(0.1)
		samples = scope.getSamples[0:128]
		plt.plot(samples)
		plt.show()
	"""

	def __init__(self):
		""" Initiate communication with the oscilloscope, then reset it, and
		configure it with reasonable defaults values:

		- max buffer size
		- 5V range on all channels
		- max sampling frequency
		- single mode acquisition (i.e. does not automatically restart)
		- buffer filling starts at the trigger position (i.e. no pre-fill)
		"""
		# Get driver
		if sys.platform.startswith("win"):
			self.dwf = cdll.dwf
		else:
			self.dwf = cdll.LoadLibrary("libdwf.so")
		# Get version
		version = create_string_buffer(16)
		self.dwf.FDwfGetVersion(version)
		self.version = version.value
		# Open device
		self.hdwf = c_int()
		self.dwf.FDwfDeviceOpen(c_int(-1), byref(self.hdwf))
		if self.hdwf.value == hdwfNone.value:
			print("-- ERROR: can not open device. Exiting...")
			sys.exit(-1)
		# Reset device
		self.dwf.FDwfAnalogInReset(self.hdwf)
		# Get number of channels
		pcChannel = c_int()
		self.dwf.FDwfAnalogInChannelCount(self.hdwf, byref(pcChannel))
		self.nChannels = pcChannel.value
		# Get device offset info
		pvoltsMin = c_double()
		pvoltsMax = c_double()
		pnSteps = c_double()
		self.dwf.FDwfAnalogInChannelOffsetInfo(self.hdwf, byref(pvoltsMin), byref(pvoltsMax), byref(pnSteps))
		self.offsetMin = pvoltsMin.value
		self.offsetMax = pvoltsMax.value
		self.offsetSteps = pnSteps.value
		# Get device frequency info
		phzMin = c_double()
		phzMax = c_double()
		self.dwf.FDwfAnalogInFrequencyInfo(self.hdwf, byref(phzMin), byref(phzMax))
		self.fsMin = phzMin.value
		self.fsMax = phzMax.value
		self.dwf.FDwfAnalogInFrequencySet(self.hdwf, c_double(self.fsMax))
		# Get device amplitude resolution
		pnBits = c_int()
		self.dwf.FDwfAnalogInBitsInfo(self.hdwf, byref(pnBits))
		self.nBits = pnBits.value
		# Get Buffer size
		pnSizeMin = c_int()
		pnSizeMax = c_int()
		self.dwf.FDwfAnalogInBufferSizeInfo(self.hdwf, byref(pnSizeMin), byref(pnSizeMax))
		self.bufferSizeMin = pnSizeMin.value
		self.bufferSizeMax = pnSizeMax.value
		self.dwf.FDwfAnalogInBufferSizeSet(self.hdwf, pnSizeMax)
		# set 5V amplitude range
		for channel in range(self.nChannels):
			self.dwf.FDwfAnalogInChannelRangeSet(self.hdwf, c_int(channel), c_double(5.0))
		# fill the buffer once triggered and then stop
		self.dwf.FDwfAnalogInAcquisitionModeSet(self.hdwf, acqmodeSingle)
		# buffer starts filling from trigger (i.e. no prefill)
		self.dwf.FDwfAnalogInTriggerPositionSet(self.hdwf, c_double(40.0e-6))

	def close(self):
		""" Close communication with the device. """
		self.dwf.FDwfDeviceCloseAll()

	def enableChannel(self, channel):
		""" Enable the channel (i.e. channel will be sampled)

		Args:
			channel(int): channel index. Must be between 0 and nChannels - 1
		"""
		if channel < 0 or channel >= self.nChannels:
			print("-- ERROR: channel must be in 0..{0}. Exiting...".format(self.nChannels - 1))
			sys.exit(-1)
		self.dwf.FDwfAnalogInChannelEnableSet(self.hdwf, c_int(channel), c_bool(True))

	def disableChannel(self, channel):
		""" Disable the channel (i.e. channel will not be sampled)

		Args:
			channel(int): channel index. Must be between 0 and nChannels - 1
		"""
		if channel < 0 or channel >= self.nChannels:
			print("-- ERROR: channel must be in 0..{0}. Exiting...".format(self.nChannels - 1))
			sys.exit(-1)
		self.dwf.FDwfAnalogInChannelEnableSet(self.hdwf, c_int(channel), c_bool(False))

	def isChannelEnabled(self, channel):
		""" Check the state of a channel

		Args:
			channel(int): channel index. Must be between 0 and nChannels - 1

		Returns:
			True is channel is enabled, False otherwise.
		"""
		if channel < 0 or channel >= self.nChannels:
			print("-- ERROR: channel must be in 0..{0}. Exiting...".format(self.nChannels - 1))
			sys.exit(-1)
		status = c_bool()
		self.dwf.FDwfAnalogInChannelEnableGet(self.hdwf, c_int(channel), byref(status))
		return status.value

	def setOffset(self, channel, offset):
		""" Configures the offset for a channel

		Args:
			channel(int): channel index. Must be between 0 and nChannels - 1
			offset(float): offset voltage level. Must be between offsetMin and offsetMax
		"""
		if channel < 0 or channel >= self.nChannels:
			print("-- ERROR: channel must be in 0..{0}. Exiting...".format(self.nChannels - 1))
			sys.exit(-1)
		if offset < self.offsetMin or offset > self.offsetMax:
			print("-- ERROR: offset must be in {0}..{1}. Exiting...".format(self.offsetMin, self.offsetMax))
		self.dwf.FDwfAnalogInChannelOffsetSet(self.hdwf, c_int(channel), c_double(offset))

	def getOffset(self, channel):
		""" Get the configured offset for the specified channel

		Args:
			channel(int): channel index. Must be between 0 and nChannels - 1

		Returns:
			offset(float): offset voltage level
		"""
		if channel < 0 or channel >= self.nChannels:
			print("-- ERROR: channel must be in 0..{0}. Exiting...".format(self.nChannels - 1))
			sys.exit(-1)
		pvoltOffset = c_double()
		self.dwf.FDwfAnalogInChannelOffsetGet(self.hdwf, c_int(channel), byref(pvoltOffset))
		return pvoltOffset.value

	def setTriggerEdge(self, channel, level, edge):
		""" Configure the trigger as edge-sensitive

		Args:
			channel(int): channel index. Must be between 0 and nChannels - 1
			level(float): voltage level that must be crossed to qualify a valid edge
			edge(str): must be 'rising' for rising edge and 'falling' for falling edge
		"""
		if channel < 0 or channel >= self.nChannels:
			print("-- ERROR: channel must be in 0..{0}. Exiting...".format(self.nChannels - 1))
			sys.exit(-1)
		self.dwf.FDwfAnalogInTriggerChannelSet(self.hdwf, c_int(channel))
		self.dwf.FDwfAnalogInTriggerTypeSet(self.hdwf, trigtypeEdge)
		self.dwf.FDwfAnalogInTriggerLevelSet(self.hdwf, c_double(level))
		if edge == 'rising':
			self.dwf.FDwfAnalogInTriggerConditionSet(self.hdwf, trigcondRisingPositive)
		elif edge == 'falling':
			self.dwf.FDwfAnalogInTriggerConditionSet(self.hdwf, trigcondFallingNegative)
		else:
			printf("-- ERROR: edge must be either 'rising' or 'falling'. Exiting...")
			sys.exit(-1)

	def setMode(self, mode):
		""" Configure acquisition mode

		Args:
			mode(str): "normal" for normal trigger, "auto" for no trigger.
		"""
		if mode == 'normal':
			self.dwf.FDwfAnalogInTriggerAutoTimeoutSet(self.hdwf, c_double(0))
			self.dwf.FDwfAnalogInTriggerSourceSet(self.hdwf, trigsrcDetectorAnalogIn)
		elif mode == 'auto':
			self.dwf.FDwfAnalogInTriggerSourceSet(self.hdwf, trigsrcNone)
		else:
			print("-- ERROR: mode must be either 'normal' or 'auto'. Exiting...")
			sys.exit(-1)

	def configure(self):
		""" Basic scope configuration:
			- channels 0 and 1 are enabled
			- offset 0.0 V on both channels
			- "normal" acquisition mode
			- trigger on rising edge on channel 1, level at 1.0 V
		"""
		self.enableChannel(0)
		self.enableChannel(1)
		self.setOffset(0, 0.0)
		self.setOffset(1, 0.0)
		self.setMode('normal')
		self.setTriggerEdge(1, 1.0, 'rising')
		time.sleep(1)

	def run(self):
		""" Start an acquisition. If acquisition mode is "normal", then the
		device waits for a trigger condition. Otherwise, it starts immediatly
		to sample points.
		"""
		self.dwf.FDwfAnalogInConfigure(self.hdwf, c_bool(False), c_bool(True))

	def isReady(self):
		""" Give acquisition status.

		Returns:
			True if acquisition is done (i.e. buffer has been filled) and False
			otherwise (i.e. acquisition is either in progress or the oscilloscope
			is still waiting for a trigger condition).
		"""
		status = c_byte()
		self.dwf.FDwfAnalogInStatus(self.hdwf, c_int(1), byref(status))
		if status.value == STATE_DONE:
			return True
		else:
			return False

	def getSamples(self, channel):
		""" Download samples from the device. Should only be called after run() and
		isReady() == True.

		Args:
			channel(int): channel index. Must be between 0 and nChannels - 1

		Returns:
			an array of bufferSizeMax integers.
		"""
		if channel < 0 or channel >= self.nChannels:
			print("-- ERROR: channel must be in 0..{0}. Exiting...".format(self.nChannels - 1))
			sys.exit(-1)
		cSamples = (c_double*self.bufferSizeMax)()
		self.dwf.FDwfAnalogInStatusData(self.hdwf, c_int(channel), cSamples, self.bufferSizeMax)
		samples = list(cSamples)
		return samples
