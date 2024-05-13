import pyoprf
from hashlib import sha1
import numpy as np
import socket
from roast.roast import SessionContext, verify
from fastecdsa.point import Point
from fastecdsa.curve import secp256k1
import time

#This is the service provider verifying a client's (prover) participation

#reading oprf result from file
file1 = open("oprf_result.txt", "rb")
stored_y = file1.read()
file1.close()

#reading and creating signature from file
def read_sig(filename):
	with open("sig.txt", "r") as file:
		x_str = file.readline().strip().split(": ")[1]  # Remove "X: " prefix
		y_str = file.readline().strip().split(": ")[1]  # Remove "Y: " prefix
		s_str = file.readline().strip().split(", ")[1][:-1]
	x = int(x_str, 16)
	y = int(y_str, 16)
	R = Point(x,y, secp256k1)
	s = int(s_str)
	return R,s

sig = read_sig("sig.txt")
#print("sig: ", str(sig))

#reading vk from file
with open("vk.txt", "r") as file:
    x_str = file.readline().strip().split(": ")[1]  # Remove "X: " prefix
    y_str = file.readline().strip().split(": ")[1]  # Remove "Y: " prefix
#print(vk)
x = int(x_str, 16)
y = int(y_str, 16)

vk = Point(x,y, secp256k1)

model = np.genfromtxt("result.txt")
hash_model = sha1(model)
ctx = SessionContext(vk, None, bytes(model), None, None, None, None)
#print(ctx)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host=socket.gethostname()
port=12345

server_socket.bind((host,port))

server_socket.listen(5)

start = time.time()
while True:
	client_socket, addr = server_socket.accept()
	print('Connected to prover')
#receive hash of the model
	data = client_socket.recv(1024).decode()
#abort if hash of owned and received models are not equal
	if data != hash_model.hexdigest():
		print("No model match")
		client_socket.close()
		break
	else :
		print("Proceeding to proof of participation")

	#send continue and send alpha to the prover
	#client_socket.send("Continue".encode())
	r, alpha = pyoprf.blind(str(vk))
	client_socket.send(str(alpha).encode())
	#print("alpha sent: ", alpha)
	#print("continue and alpha sent")

	#receive beta from the prover
	beta = client_socket.recv(1024)
	#print("received message: ", beta)

	#verify signature
	ver = verify(ctx,sig)
	if not ver:
		break
	print("Signature verified successfully")
	#get oprf result and check that it equals stored hash
	N = pyoprf.unblind(r,beta)
	y = pyoprf.finalize(str(vk), N)
	if y == stored_y:
		print("OPRF result matches")
	else :
		break
	client_socket.close()
	break
end = time.time()
ln = ","+str(end-start)+"\n"
file = open("generate.csv", "a")
file.write(ln)
file.close()
