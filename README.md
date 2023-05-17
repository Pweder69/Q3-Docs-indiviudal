
# Temp sensor
## Description and Code
In this assignment, we were supposed to change the output of an LCD by using a temp sensor.

```python 
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
```
The code is relatively simple the only part that offers some confusion is the the calculation     
__(sens.value * 3.3/65535)*1000)-500)/10__ 

Sens val is the input from the temp sensor, that value is multiplied by 3.3 to get the "reference voltage" and then divided by the max value of a 16-bit unassigned int because we are handling the output of an Analog pin which \ outputs an unassigned 16-bit int. The reason we do all this is to get the voltage from the analog pin and dividing by 65535 gets us the relative amount of voltage to 1. The heavy work is done as we now have a voltage value the rest of the equation is applied as we turn volts to millivolts subtract 500 and divide by 10 to get our degrees in C.

## Evidence 

<video src="https://user-images.githubusercontent.com/113122312/227981461-31610f53-0d8f-4e05-8ba5-c9bb21450ada.MOV" data-canonical-src="https://user-images.githubusercontent.com/113122312/227981461-31610f53-0d8f-4e05-8ba5-c9bb21450ada.MOV" controls="controls" muted="muted" class="d-block rounded-bottom-2 border-top width-fit" style="max-height:640px; min-height: 200px">

  </video>



![](https://user-images.githubusercontent.com/113122312/227987295-7a60463d-3927-4f7f-bf9d-911642b45de6.PNG)

From [Jinho](https://github.com/Jpark27614/CircuitPython)

## Reflection 
I feel like this assignment had its troubles with figuring out the calculation but managing the actual value was easy and outputting to an LCD was only copy paste from previous assignments. I liked the idea of making us figure out these calculations and it was fun but not too hard if you understand what the documentation on the Adafruit website means. Generally, i would say this was a good reintroduction to LCDs and very basic logic. But the most important part was understanding and not copying the equation :)

# Rotary encoder
## Description and code explination
 In this assignment, we were tasked with creating a sort of menu system for an LCD using a list or tuple.
``` python
import rotaryio
import time
import board
from lcd.lcd import LCD
from lcd.i2c_pcf8574_interface import I2CPCF8574Interface
import digitalio
import neopixel

dot = neopixel.NeoPixel(board.NEOPIXEL, 1)
dot.brightness = 0.5 

i2c = board.I2C()
lcd = LCD(I2CPCF8574Interface(i2c, 0x3f), num_rows=2, num_cols=16)


enc = rotaryio.IncrementalEncoder(board.D9, board.D8,2)
last_position = None

encBtn = digitalio.DigitalInOut(board.D7)
encbtn = digitalio.Direction.INPUT
encbtn  = digitalio.Pull.UP

global prevState

def btnControl(buttonVal ,out):
    global prevState
    if buttonVal and buttonVal != prevState:
        prevState = True
        if out == 0:
            dot.fill((255,0,0))
        elif out == 1:
                dot.fill((255,255,0))
        else:
                dot.fill((0,255,0))
    elif  not buttonVal:
        prevState = False
     
        

def retEnc(x):
    array = ["stop","caution","go"] 
    output = x%3
    btnControl(encBtn.value,output)
    return array[output]




while True:
    lcd.print(retEnc(enc.position))
    time.sleep(.05)
    lcd.clear()
    print(f"{retEnc(enc.position)} {enc.position} {encBtn.value}")

# CHONKER OF A CODE
```
The 2 Main functions of this code are "retEnc" and "BtnControl". Mainly focus on retEnc because BtnControl is only a debounce function that manages a button and has been documented many times [before](https://github.com/Pweder69/RobotArm/blob/master/README.md). This function is one of my favorites because it's very short and in my opinion very clever. First I will explain the modulo operator as represented in Python as the percent symbol __%__. what it does is it divides 2 numbers and spits out the remainder __(ex... 5%3 = 2 bc remainder of 5/3 = 2)__ We use this on the value outputted by the encoder as it will output the same sequence regardless of the size of the value, conveniently this value is the same as the index of the list of the items we must cycle. so we can just input the modulo of the encoder value to the index of the list another bonus is that it works even with negative numbers and reverses the order as well. Note that it's very easy to scale the cycle of items by just increasing the list and modulo for the future. 

## Evidence 
<video src="https://user-images.githubusercontent.com/113122312/228878419-eeb6ee13-e4dc-4017-8130-15ca412da687.mov" data-canonical-src="https://user-images.githubusercontent.com/113122312/228878419-eeb6ee13-e4dc-4017-8130-15ca412da687.mov" controls="controls" muted="muted" class="d-block rounded-bottom-2 border-top width-fit" style="max-height:640px; min-height: 200px">

  </video>

<img src="https://user-images.githubusercontent.com/113122312/228681141-60d64fc1-656b-46e3-b487-be3014dc983c.png" alt="Screenshot 2023-03-29 6 23 12 PM" style="max-width: 100%;">

<img src="https://user-images.githubusercontent.com/113122312/228682209-61f189f5-6434-4f74-980b-c6ba4c7f70ba.png" alt="Screenshot 2023-03-29 6 29 21 PM" style="max-width: 100%;">

From Jinho Park

## Reflection 
This assignment was very fun and surprisingly easy as with all code it seems easy if you have the experience to know tools like modulo and can make your life very easy instead of just copying someone or making a complex logic tree for all cases of the encoder sequence. renewing on debounce functions was also nice 

# Photo-Interrupter
## Description and Code

For this assignment, we are supposed to use monatomic time and sleep and the task is to print out when we get interrupted.

``` python
import time
import digitalio
import board

photoI = digitalio.DigitalInOut(board.D7)
photoI.direction = digitalio.Direction.INPUT
photoI.pull = digitalio.Pull.UP

last_photoI = True
last_update = -4

photoICrosses = 0

while True:
    if time.monotonic()-last_update > 4:
        print(f"The number of crosses is {photoICrosses}")
        last_update = time.monotonic()
    
    if last_photoI != photoI.value and not photoI.value:
        photoICrosses += 1
    last_photoI = photoI.value
```
From [river]()

## Evidence
<img src="https://user-images.githubusercontent.com/113122312/228711571-9069fe6d-12e7-4f94-989c-8a6d32102e1e.png" alt="Screenshot 2023-03-29 10 21 44 PM" style="max-width: 100%;">

<img src="https://user-images.githubusercontent.com/113122312/228884183-8e19d09a-aec4-444f-8eee-c57cb055fed5.jpg" alt="Inkedphotoint05" style="max-width: 100%;">

From [river](https://github.com/rivques/CircuitPython)

# Reflection 
This assignment was annoying not because it is hard but because the photointeruppters don't work 90% of the time. The code was simple to understand as just a debounce and interrupt counter and the assignment was only difficult to the extent of figuring out why photointeruppters don't work how they should but after that, it was very easy.
