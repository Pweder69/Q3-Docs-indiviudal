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
    elif x < 26:
        return "cold"
    else:
        return "nice"
while True:
    val = (((sens.value * 3.3/65535)*1000)-500)/10
    lcd.set_cursor_pos(0,0)

    lcd.print( tempOut(val))
    lcd.set_cursor_pos(1,0)
    lcd.print(f"temp in C: {round(val,2)}")
    time.sleep(.5)
    lcd.clear()
    
    print(round(val,2))