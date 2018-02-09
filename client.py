import socket

s = socket.socket()
host = ''
port = 12345
s.connect((host,port))
print(s.recv(1024))
s.close()
