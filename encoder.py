import time
import board
import analogio 
from lcd.lcd import LCD
from lcd.i2c_pcf8574_interface import I2CPCF8574Interface

i2c = board.I2C()
lcd = LCD(I2CPCF8574Interface(i2c, 0x3f), num_rows=2, num_cols=16)