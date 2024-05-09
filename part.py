from multiprocessing import Process, Queue
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR, IPPROTO_TCP, TCP_NODELAY

import logging
import sys
import time

from roast.roast import pre_round, sign_round
from roast.transport import send_obj, recv_obj
from roast.participant import *

MAX_NONCE_QUEUE = 32


logging.basicConfig(level=logging.CRITICAL)

if len(sys.argv) != 2:
    print(f'usage: {sys.argv[0]} <port>')
    sys.exit(1)

nonce_queue = Queue(MAX_NONCE_QUEUE)
Process(target=compute_nonce_loop, args=[nonce_queue], daemon=True).start()

port = int(sys.argv[1])
addr = ('0.0.0.0', port)

sock = socket(AF_INET, SOCK_STREAM)
sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, True)
sock.setsockopt(IPPROTO_TCP, TCP_NODELAY, True)
sock.bind(addr)
sock.listen()

while True:
    logging.debug(f'Listening for incoming connections on {addr}')

    connection, src = sock.accept()
    logging.debug('Accepted connection from {src}')

    try:
        handle_requests(connection, nonce_queue)
    except ConnectionResetError as e:
        print(e)
