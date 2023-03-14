import time
import board
import analogio 
from lcd.lcd import LCD
from lcd.i2c_pcf8574_interface import I2CPCF8574Interface

i2c = board.I2C()
lcd = LCD(I2CPCF8574Interface(i2c, 0x3f), num_rows=2, num_cols=16)

sens = analogio.AnalogIn(board.A0)

def tempOut(x):
    if x >27:
        return "hot"
    elif x < 20:
        return "cold"
    else:
        return "nice"
while True:
    val = (((sens.value/19859.0909091)*1000)-500)/10
    lcd.print( tempOut(val))
    lcd.print(str(val))
    time.sleep(.5)
    lcd.clear()
    
    
    print(round(val))