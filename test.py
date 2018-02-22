import RPi.GPIO as ada
import socket

s = socket.socket()
host = '192.168.4.1'
port = 6677
s.bind((host,port))

print '{} is the version type.' .format(ada.VERSION)

ada.setmode(ada.BCM)
count = 0
ada.setup(24, ada.IN, pull_up_down=ada.PUD_DOWN)
def my_callback(channel):
    global count
    count += 1
    print '{} is the current count' .format(count)

ada.add_event_detect(24, ada.RISING, callback=my_callback, bouncetime=200)

while True:
  s.listen(1)
  c, addr = s.accept()
  print('Got connection from', addr)
  c.send(str(count))
  c.close()

ada.cleanup()

print 'test'
