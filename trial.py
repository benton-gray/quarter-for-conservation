import RPi.GPIO as GPIO
import Pi7SegPy as Pi7Seg
import PiShiftPy as shift
import ProjectClass as Conservation
import client as cli
#import server as server
#import map_network as net 
import time
import os

#globals and setup for interrupt
project0 = Conservation.Project()
project1 = Conservation.Project()
project2 = Conservation.Project()
project3 = Conservation.Project()
currentInterruptChannel = 0
listOfProjects = []
storedNumberFileName = "storedNumber.txt"
number = 1
flag = False
#segmentData=18,22
#segmentClock=15,27
#segmentLatch=14,17
#end globals for interrupt

def setup_gpio():
  #global segmentClock
  #global segmentLatch
  #global segmentData
  GPIO.setwarnings(True)
  GPIO.setmode(GPIO.BCM)
  
  for i in range(len(listOfProjects)):
      GPIO.setup(listOfProjects[i].segmentData,GPIO.OUT)
      GPIO.setup(listOfProjects[i].segmentClock,GPIO.OUT)
      GPIO.setup(listOfProjects[i].segmentLatch,GPIO.OUT)
      GPIO.output(listOfProjects[i].segmentData,GPIO.LOW)
      GPIO.output(listOfProjects[i].segmentClock,GPIO.LOW)
      GPIO.output(listOfProjects[i].segmentLatch,GPIO.LOW)
      GPIO.setup(listOfProjects[i].firstInterrupt,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
      GPIO.setup(listOfProjects[i].secondInterrupt,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
      GPIO.add_event_detect(listOfProjects[i].firstInterrupt, GPIO.FALLING, callback=my_callback,bouncetime=500)
      GPIO.add_event_detect(listOfProjects[i].secondInterrupt, GPIO.FALLING, callback=my_callback,bouncetime=500)
      print("i is:" +str(i))
      
      '''
  GPIO.setup(segmentClock,GPIO.OUT)
  GPIO.setup(segmentData,GPIO.OUT)
  GPIO.setup(segmentLatch,GPIO.OUT)
  GPIO.output(segmentClock,GPIO.LOW)
  GPIO.output(segmentData,GPIO.LOW)
  GPIO.output(segmentLatch,GPIO.LOW)
  GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
  '''
  
def setupProjectObjects():
    global listOfProjects
    '''
    This function sets all the variables and gpio used by each project
    segmentData = 0
    segmentClock = 0
    segmentLatch = 0
    projectInterrupts = array(0,0)
    storedNumberFileName = ""
    '''
    #project0 = pc.Project()
    #latch,clock,data
    project0.init(2,3,4,"project0",14,15,0)
    #project1 = pc.Project()
    project1.init(17,27,22,"project1",23,24,0)
    project2.init(10,9,11,"project2",25,8,0)
    project3.init(5,6,13,"project3",16,20,0)
    #this list is used in the setup_gpio function to initiate appropriate pins
    listOfProjects.append(project0)
    listOfProjects.append(project1)
    listOfProjects.append(project2)
    listOfProjects.append(project3)
    '''
    project0.segmentLatch = 3
    project0.segmentClock = 5
    project0.segmentSerial = 7
    project0.projectInterrupts.append(14)
    project0.projectInterrupts.append()
    '''

def my_callback(channel):
  '''
  Callback function to detect interrupts from sensors
  '''
  #rint("channel:" + str(channel))
  global flag
  global currentInterruptChannel
  
  currentInterruptChannel = channel
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

def LED_NUMBER(project):
  '''
  Increments number and outputs to 7 segment dipslay
  '''
  #global number
  shift.write_all(0)
  project.currentNumber = project.currentNumber + 1
  Pi7Seg.show(list(map(int, str(project.currentNumber))))
  print(project.storedNumberFileName + "  " + str(project.currentNumber));
  print("got after increment")
#this function will be ran to obtain the previously stored count from a file on bootup
def setAllStoredCount():
    global storedNumberFileName
    global number
    for i in range(len(listOfProjects)):
        if os.path.exists(listOfProjects[i].storedNumberFileName):
            with open(listOfProjects[i].storedNumberFileName, 'r') as file:
                #for line in file:
                    #x = line.strip('')
                    #print(x)
                    #print(type(int(x)))
                    #listOfProjects[i].currentNumber = int(x)
                    
                try:
                    #print("the number is : " + file.readline())
                    x = file.readline().strip('')
                    #print(x)
                    listOfProjects[i].currentNumber = int(x)
                        #listOfProjects[i].currentNumber = int(listOfProjects[i].currentNumber)
                except Exception as e:
                    print(e)
        else :
        #file doesn't exist, make the file here and initialize it to be
        #the number 1
            with open(listOfProjects[i].storedNumberFileName, 'w') as file:
                try:
                    file.write("0")
                except:
                    print("Can't write internal number. Maybe you have no file permission")
            listOfProjects[i].currentNumber = 0
            #number = 1
            #print("file doesnt exist")
def writeCurrentNumberToFile():
    for i in range(len(listOfProjects)):
        if os.path.exists(listOfProjects[i].storedNumberFileName):
            with open(listOfProjects[i].storedNumberFileName, 'w') as file:
                #for line in file:
                    #x = line.strip('')
                    #print(x)
                    #print(type(int(x)))
                    #listOfProjects[i].currentNumber = int(x)
                    
                try:
                    file.write(str(listOfProjects[i].currentNumber))
                    #print(x)
                    #listOfProjects[i].currentNumber = int(x)
                        #listOfProjects[i].currentNumber = int(listOfProjects[i].currentNumber)
                except Exception as e:
                    print(e)
        else :
        #file doesn't exist, make the file here and initialize it to be
        #the number 1
            with open(listOfProjects[i].storedNumberFileName, 'w') as file:
                try:
                    file.write("0")
                except:
                    print("Can't write internal number. Maybe you have no file permission")
    

def main():
  '''
  Start of Execution
  '''
  count = 0
  print("went into main")
  global flag
  #global number
  global currentInterruptChannel
  setupProjectObjects()
  setup_gpio()
  setAllStoredCount()
  print("just setup gpio")
  #GPIO.add_event_detect(23, GPIO.FALLING, callback=my_callback,bouncetime=500)
  #Pi7Seg.init(project0.segmentData, project0.segmentClock, project0.segmentLatch, 7, 7, common_cathode_type=False)
  print("2")
  #TODO: CLEAR ALL DISPLAYS USING write_all for every single display on the first run
  #shift.write_all(0)
  #END TODO
  print("3")
  while True:

    if(count == 800000):
      writeCurrentNumberToFile()
      serv_num = cli.get_number('Gorillaz Giraffes')
      print(serv_num)
      gorillaz = int(serv_num[0])
      giraffes = int(serv_num[1])
      if(project0.currentNumber < gorillaz):
        project0.currentNumber = gorillaz
        print(project0.currentNumber)
        flag = True
      if(project1.currentNumber < giraffes):
        project1.currentNumber = giraffes
        print(project1.currentNumber)
        flag = True
      count = 0
      print("4z")

    if flag:
      #we want to turn off the flag right away or else it's uselss to do theinterrupt this way
      flag = False
      
      if(currentInterruptChannel == 14 or currentInterruptChannel == 15):
        Pi7Seg.init(project0.segmentData, project0.segmentClock, project0.segmentLatch, 7, 7, common_cathode_type=False)
        LED_NUMBER(project0)
        cli.send_number('Gorillaz ' + str(project0.currentNumber))
      elif(currentInterruptChannel == 23 or currentInterruptChannel == 24):
        Pi7Seg.init(project1.segmentData, project1.segmentClock, project1.segmentLatch, 7, 7, common_cathode_type=False)
        LED_NUMBER(project1)
        cli.send_number('Giraffes ' + str(project1.currentNumber))
      elif(currentInterruptChannel == 25 or currentInterruptChannel == 8):
        Pi7Seg.init(project2.segmentData, project2.segmentClock, project2.segmentLatch, 7, 7, common_cathode_type=False)
        LED_NUMBER(project2)
      elif(currentInterruptChannel == 16 or currentInterruptChannel == 20):
        Pi7Seg.init(project3.segmentData, project3.segmentClock, project3.segmentLatch, 7, 7, common_cathode_type=False)
        LED_NUMBER(project3)
    
    count = count + 1

      
    #server.serv()

if __name__ == "__main__":
  try:
    print("went here")
    #setupProjectObjects()
    main()
  except Exception as e:
    print(e)
    GPIO.cleanup()
    #server.close()
else:
  exit
