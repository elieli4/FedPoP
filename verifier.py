import pyoprf
from hashlib import sha1
import numpy as np
import socket

#This is the service provider verifying a client's (prover) participation


model = np.genfromtxt("result.txt")
hash_model = sha1(model)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host=socket.gethostname()
port=12345

server_socket.bind((host,port))

server_socket.listen(5)

while True:
	client_socket, addr = server_socket.accept()
	print('connected to prover')
	data = client_socket.recv(1024).decode()
	if data == hash_model.hexdigest():
		print("match")
	client_socket.close()
