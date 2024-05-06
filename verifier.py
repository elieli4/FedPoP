import pyoprf
from hashlib import sha1
import numpy as np
import socket

#This is the service provider verifying a client's (prover) participation

#test reading vk from file
file1 = open("vk.txt","r")
vk = file1.read()
#print(X)
file1.close()

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
#receive hash of the model
	data = client_socket.recv(1024).decode()
#abort if hash of owned and received models are not equal
	if data != hash_model.hexdigest():
		print("no model match")
		client_socket.close()
		break
	else :
		print("Proceeding to proof of participation")
		client_socket.send("Continue".encode())
	beta = client_socket.recv(1024).decode()
	N = pyoprf.unblind(r,beta)
	y = pyoprf.finalize(vk, N)
	assert y = stored_y
	client_socket.close()
