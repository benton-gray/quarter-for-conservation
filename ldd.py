'''
 Controlling large 7-segment displays
 By: Nathan Seidle
 SparkFun Electronics
 Date: February 25th, 2015
 License: This code is public domain but you buy me a beer if you use this and we meet someday (Beerware license).

 The large 7 segment displays can be controlled easily with a TPIC6C594 IC. This code demonstrates how to control
 one display.

 Here's how to hook up the Arduino pins to the Large Digit Driver
 
 Arduino pin 6 -> CLK (Green on the 6-pin cable)
 5 -> LAT (Blue)
 7 -> SER on the IN side (Yellow)
 5V -> 5V (Orange)
 Power Arduino with 12V and connect to Vin -> 12V (Red)
 GND -> GND (Black)

 There are two connectors on the Large Digit Driver. 'IN' is the input side that should be connected to
 your microcontroller (the Arduino). 'OUT' is the output side that should be connected to the 'IN' of addtional
 digits.
 
 Each display will use about 150mA with all segments and decimal point on.
'''
import time as t
#define a  1<<0
#define b  1<<6
#define c  1<<5
#define d  1<<4
#define e  1<<3
#define f  1<<1
#define g  1<<2
#define dp 1<<7


''' GPIO declarations
-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
'''

import RPi.GPIO as ada
ada.setmode(ada.BOARD)

red=3
oj=5
yellow=7

chan_list = [red,oj,yellow]

ada.setup(red,ada.OUT)
ada.setup(oj,ada.OUT)
ada.setup(yellow,ada.OUT)

'''
-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
'''

ada.output(chan_list,ada.LOW)

x = 0
try:
  while(True):
    print 'x is {}' .format(x)

    ada.output(yellow,ada.LOW)
    ada.output(yellow,ada.HIGH)
    t.sleep(1) 
    x += 1
except:
  ada.cleanup(chan_list)
  print ''

'''Given a number, or '-', shifts it out to the display'''
def postNumber(number):
  '''    -  A
       / / F/B
        -  G
       / / E/C
        -. D/DP
  '''

  segments = ''
  if number == 1:
    segments = b | c 
  elif number == 2:
    segments = a | b | d | e | g
  '''
    case 3: segments = a | b | c | d | g; break;
    case 4: segments = f | g | b | c; break;
    case 5: segments = a | f | g | c | d; break;
    case 6: segments = a | f | g | e | c | d; break;
    case 7: segments = a | b | c; break;
    case 8: segments = a | b | c | d | e | f | g; break;
    case 9: segments = a | b | c | d | f | g; break;
    case 0: segments = a | b | c | d | e | f; break;
    case ' ': segments = 0; break;
    case 'c': segments = g | e | d; break;
    case '-': segments = g; break;
  '''
  
  x = 0
  '''Clock these bits out to the drivers'''
  while x < 8:
    ada.output(oj,ada.LOW)
    if (segments & 1 << (7-x)) == 1:
      ada.output(red,ada.HIGH)
    else:
      ada.output(red,ada.LOW)
    ada.output(oj,ada.HIGH) 
    '''Data transfers to the register on the rising edge of SRCK'''
    x += 1


