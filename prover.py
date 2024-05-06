#import pyoprf
from hashlib import sha1
import numpy as np
import socket

# This is the client proving its participation to the service provider.

model = np.genfromtxt("result.txt")
hash_model=sha1(model)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = socket.gethostname()
port = 12345

client_socket.connect((host,port))

hs = hash_model.hexdigest()
client_socket.send(hs.encode())

client_socket.close()
