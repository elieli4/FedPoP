#import pyoprf
from hashlib import sha1
import numpy as np
import socket

# This is the client proving its participation to the service provider.

file1 = open("beta.txt", "r")
beta=file1.read()
file1.close()

file2 = open("tsig.txt", "r")
sig = file2.read()
file2.close()

model = np.genfromtxt("result.txt")
hash_model=sha1(model)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = socket.gethostname()
port = 12345

client_socket.connect((host,port))

#send hash of the model to the verifier
hs = hash_model.hexdigest()
client_socket.send(hs.encode())

resp = client_socket.recv(1024).decode()
if resp!="continue":
	client_socket.close()

client_socket.send(beta.encode())

client_socket.close()
