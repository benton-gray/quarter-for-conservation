import socket

host = '192.168.4.4'
port = 6677
i=0

def new_sock(host, port):
  s = socket.socket()
  s.connect((host,port))
  return s


while(i<10):
  s = new_sock(host,port)
  print(s.recv(512))
  s.send('{}' .format(i).encode())
  i = i + 1
  s.close()
