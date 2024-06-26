import pyoprf
from hashlib import sha1
import numpy as np
import socket

# This is the client proving its participation to the service provider.

file1 = open("oprf_k.txt", "rb")
oprf_k=file1.read()
file1.close()

file2 = open("sig.txt", "r")
sig = file2.read()
file2.close()

model = np.genfromtxt("result.txt")
hash_model=sha1(model)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = socket.gethostname()
port = 12345

client_socket.connect((host,port))

snd=0
rcv=0
#send hash of the model to the verifier
hs = hash_model.hexdigest()
client_socket.send(hs.encode())
snd+=len(hs.encode())
#get "Continue response from the server"
#resp = client_socket.recv(1024).decode()
#print("Message received: ", resp)
alp = client_socket.recv(1024)
alpha = eval(alp.decode())
rcv+=len(alp)
#print("test")
#print("Message received: ", alpha)

#compute beta and send to verifier
beta = pyoprf.evaluate(oprf_k, alpha)
#print("beta: ", beta)
client_socket.send(beta)
#print("I sent beta")
snd+=len(beta)
print("Finished")
print("data sent: ", snd)
print("data received: ", rcv)
client_socket.close()
