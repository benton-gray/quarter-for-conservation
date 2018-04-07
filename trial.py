import RPi.GPIO as GPIO
import time
import Pi7SegPy as Pi7Seg
import PiShiftPy as shift
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
segmentData=18
segmentClock=15
segmentLatch=14
#setting up the PWM for powering the sensor at 1.7V
#end setup for PWM
GPIO.setup(segmentClock,GPIO.OUT)
GPIO.setup(segmentData,GPIO.OUT)
GPIO.setup(segmentLatch,GPIO.OUT)
GPIO.output(segmentClock,GPIO.LOW)
GPIO.output(segmentData,GPIO.LOW)
GPIO.output(segmentLatch,GPIO.LOW)
number= 1

#Interrupt Code for the two sensors
#GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
#GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#globals and setup for interrupt
x = 0
flag = 0
#end globals for interrupt

def my_callback(channel):
  LED_NUMBER()

GPIO.add_event_detect(23, GPIO.FALLING, callback=my_callback,bouncetime=500)
#GPIO.add_event_detect(27, GPIO.FALLING, callback=my_callback,bouncetime=500)
#End interrupt Code for Sensor


Pi7Seg.init(segmentData, segmentClock, segmentLatch, 2, 2, common_cathode_type=False)
#flush transients from shift registers
shift.write_all(0)
#end flush transients

def loop(number):
  showNumber(float(number)) #Test Pattern

#TODO: Need to fix bug here, we want to display the numbers as 01 02 03
# instead of 10 11 etc
def showNumber(value):
  number = abs(value) #Remove negative signs and any decimals
  print(value)
  if number>=10:
    remainder = number % 10
    postNumber(remainder, False)
    number = int(number/10)
    postNumber(number, False)
  else:
    postNumber(number, False)
    #postNumber("0", False)

  #Latch the current segment data
  GPIO.output(segmentLatch,GPIO.LOW)
  GPIO.output(segmentLatch,GPIO.HIGH) #Register moves storage register on the rising edge of RCK

#Given a number, or - shifts it out to the display
def postNumber(number, decimal):
  segments=bytes()
  a=1<<0
  b=1<<6
  c=1<<5
  d=1<<4
  e=1<<3
  f=1<<1
  g=1<<2
  dp=1<<7
  if number == 1: segments = b | c
  elif number == 2: segments = a | b | d | e | g 
  elif number == 3: segments = a | b | c | d | g
  elif number == 4: segments = b | c | f | g
  elif number == 5: segments = a | c | d | f | g
  elif number == 6: segments = a | c | d | e | f | g
  elif number == 7: segments = a | b | c
  elif number == 8: segments = a | b | c | d | e | f | g
  elif number == 9: segments = a | b | c | d | f | g
  elif number == 0: segments = a | b | c | d | e | f 
  elif number == ' ': segments = 0
  elif number == 'c': segments = g | e | d
  elif number == '-': segments = g
  else : segments = 0

 ##mistake likely here   
 #   if ((decimal segments) |= dp ):
    #print(number)
    #print(segments)
  y=0
  while(y<8):
    GPIO.output(segmentClock,GPIO.LOW)
    GPIO.output(segmentData,segments & 1 << (7-y))
    GPIO.output(segmentClock,GPIO.HIGH)   
    y += 1

def LED_NUMBER():        
  global number
  #BOTTLENECK: writing all bits to 0 before printing new number
  #TODO: Need to figure out if there is a way to write the numbers without writing all digits to 0.
  shift.write_all(0)
  #END BOTTLENECK
  #BOTTLENECK: Converting number to list of numbers since that's what the function expects
  Pi7Seg.show(list(map(int, str(number))))
  #END BOTTLENECK
  number = number + 1
    
#while True:
#    number = number + 1
#    print (number)
#    loop(number)
#    time.sleep(1)
#    if number>=99:
#        number = 0


#GPIO.cleanup()
