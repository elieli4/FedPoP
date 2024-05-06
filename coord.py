import subprocess
import numpy

from dataclasses import dataclass, field
from multiprocessing import Process, Queue, Value
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR, IPPROTO_TCP, TCP_NODELAY
from typing import Any
from enum import Enum

import logging
import secrets
import sys
import time

from roast.shamir import split_secret
from roast.model import ActionType, CoordinatorModel
from roast.roast import share_val, verify
from roast.transport import send_obj, recv_obj

from roast import fastec
from coordSplitSetup import *
import pyoprf, pysodium

#setup
logging.basicConfig(level=logging.INFO)

if len(sys.argv) != 7:
    print(f'usage: {sys.argv[0]} <host> <start_port> <threshold> <total> <malicious> <attacker_level>')
    sys.exit(1)

host = sys.argv[1]
start_port = int(sys.argv[2])
t = int(sys.argv[3])
n = int(sys.argv[4])
m = int(sys.argv[5])
attacker_level = AttackerLevel(int(sys.argv[6]))
msg = numpy.genfromtxt('result.txt')
i_to_addr = {i + 1: (host, start_port + i) for i in range(n)}
 # This is insecure; in practice we'd use DKG, but since
    # key generation is not the focus of the ROAST protocol, we will
    # keep the implementation simple by having the coordinator
    # act as a centralized dealer
sk = 1 + secrets.randbelow(fastec.n - 1)
i_to_sk = split_secret(sk, t, n)

X = sk * fastec.G
i_to_X = {i: sk_i * fastec.G for i, sk_i in i_to_sk.items()}
i_to_cached_ctx = {i + 1: Queue() for i in range(n)}

actions = Queue()
outgoing = Queue()
coordinator = Coordinator(actions, outgoing, i_to_cached_ctx)
coordinator.setup(i_to_addr)

model = CoordinatorModel(X, i_to_X, t, n, msg)
attacker_strategy = AttackerStrategy(attacker_level, n, m)
coordinator.prerun(i_to_sk, model, attacker_strategy)
print("did key share")

#oprf setup

vk = str(sk)
oprf_k = pyoprf.keygen()
r, alpha = pyoprf.blind(vk) #find out how to get real VK
beta = pyoprf.evaluate(oprf_k, alpha)
N = pyoprf.unblind(r, beta)
y = pyoprf.finalize(vk, N)


# run the secure aggregation
print("Start Sec Agg")
subprocess.call(['sh', './run.sh'])
print("End Sec Agg")



#make t signature

elapsed, send_count, recv_count, sid = coordinator.run(i_to_sk, model, attacker_strategy)
print(t, n, m, attacker_level, elapsed, send_count, recv_count, sid, sep=',')
