import RPi.GPIO as GPIO
import Pi7SegPy as Pi7Seg
import PiShiftPy as shift
#import client as cli
import server as server
#import map_network as net 
import time

#globals and setup for interrupt
number = 1
flag = False
segmentData=18
segmentClock=15
segmentLatch=14
#end globals for interrupt

def setup_gpio():
  global segmentClock
  global segmentLatch
  global segmentData
  GPIO.setwarnings(True)
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(segmentClock,GPIO.OUT)
  GPIO.setup(segmentData,GPIO.OUT)
  GPIO.setup(segmentLatch,GPIO.OUT)
  GPIO.output(segmentClock,GPIO.LOW)
  GPIO.output(segmentData,GPIO.LOW)
  GPIO.output(segmentLatch,GPIO.LOW)
  GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def my_callback(channel):
  '''
  Callback function to detect interrupts from sensors
  '''
  global flag
  flag = True

def loop(number):
  '''
  Something
  '''
  showNumber(float(number)) #Test Pattern

def showNumber(value):
  '''
  Something
  '''
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

def postNumber(number, decimal):
  '''
  Given a number, or - shifts it out to the display
  '''
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
  '''
  Increments number and outputs to 7 segment dipslay
  '''
  global number
  shift.write_all(0)
  Pi7Seg.show(list(map(int, str(number))))
  number = number + 1


def main():
  '''
  Start of Execution
  '''
  global flag
  global number
  setup_gpio()
  GPIO.add_event_detect(23, GPIO.FALLING, callback=my_callback,bouncetime=500)
  Pi7Seg.init(segmentData, segmentClock, segmentLatch, 2, 2, common_cathode_type=False)
  shift.write_all(0)
  while True:
    if flag:
      LED_NUMBER()
      flag = False
    server.serv()

if __name__ == "__main__":
  try:
    main()
  except:
    GPIO.cleanup()
    server.close()
else:
  exit
