import socket

s = socket.socket()
host = '0.0.0.0'
port = 12345
s.bind((host,port))

s.listen(5)
while True:
  c, addr = s.accept()
  print('Got connection from', addr)
  c.send('Thank you for connecting')
  c.close()
