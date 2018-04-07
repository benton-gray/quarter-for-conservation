import socket
s = socket.socket()
host = '192.168.4.11'
port = 6677
s.bind((host,port))
project_number = 0

def serv():
  s.listen(5)
  c, addr = s.accept()
  print('Got connection from', addr)
  c.send('Thank you for connecting')
  x = c.recv(512)  
  return x
 
def close():
  c.close()

