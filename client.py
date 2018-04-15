import socket

host = '192.168.4.1'
port = 6677

def new_sock(host, port):
  s = socket.socket()
  s.connect((host,port))
  return s


def send_number(i):
  s = new_sock(host,port)
  s.send('{}' .format(i).encode())
  s.close()
  
def get_number(i):
  s = new_sock(host,port)
  s.send('{}' .format(i).encode())
  number = s.recv(1024)
  s.close()
  return [ number.split()[0], number.split()[1] ]
