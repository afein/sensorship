import socket

#address = '127.0.0.1'
address = '192.168.99.100'
port = 32774 

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((address, port))
s.send('asdf')
s.close()

port = 32775 

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((address, port))
s.send('qwer')
s.close()