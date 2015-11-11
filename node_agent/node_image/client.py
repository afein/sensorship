import socket

address = '0.0.0.0'
#address = '192.168.99.100'
port = 32768 

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((address, port))
s.send('asdf')
s.close()

port = 32769

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((address, port))
s.send('qwer')
s.close()
