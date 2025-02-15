'''
Driver for the CST820 touch controller
(c) 2024 Olav Schettler
License: MIT
'''

import board
from adafruit_bus_device.i2c_device import I2CDevice
import adafruit_cst8xx

class CST820(adafruit_cst8xx.Adafruit_CST8XX):
    def __init__(self):
        self._i2c = I2CDevice(board.I2C(), 0x15)
        self._debug = False
        self._irq_pin = None

EVENTS = adafruit_cst8xx.EVENTS
