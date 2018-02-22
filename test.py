import RPi.GPIO as ada
import socket

print '{} is the version type.' .format(ada.VERSION)

ada.setmode(ada.BCM)
count = 0
ada.setup(24, ada.IN)
def my_callback(channel):
    global count
    count += 1
    print '{} is the current count' .format(count)

ada.add_event_detect(24, ada.RISING, callback=my_callback, bouncetime=200)

'''while True:
  s.listen(1)
  c, addr = s.accept()
  print('Got connection from', addr)
  c.send(str(count))
  c.close()
'''
while True:
   pass 

ada.cleanup()

print 'test'
