import socket

s = socket.socket()
host = '192.168.4.1'
port = 6677
s.bind((host,port))

s.listen(5)
try:
  while True:
    c, addr = s.accept()
    print('Got connection from', addr)
    c.send('Thank you for connecting')
    print(c.recv(1024))
except:
  c.close()
