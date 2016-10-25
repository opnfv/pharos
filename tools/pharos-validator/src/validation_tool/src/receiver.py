##############################################################################
# Copyright (c) 2015 Todd Gaunt and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import socket
import threading
import logging

from pharosvalidator.util import read_msg

def start(nodecount, port, q):
    """Start a server to retrieve the files from the nodes. Server will run
    indefinetely until the parent process ends"""
    logging.basicConfig(level=0)
    logger = logging.getLogger(__name__)

    address = "" # Empty means act as a server on all available interfaces

    logger.info("Bringing up receiver server...")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((address, port))
    sock.listen(nodecount) # Max connections is the amount of nodes

    while True:
        # Receive a descriptor for the client socket, cl stands for client
        (clsock, claddress) = sock.accept()
        logger.info("Received client connection...")
        client_thread = threading.Thread(target=_server_accept_thread, \
                args=(clsock, claddress, q), daemon=True)
        # Start a new thread to read the new client socket connection
        client_thread.start()

    socket.close()
    logger.info("Bringing down receiver server...")

def _server_accept_thread(clsock, claddress, q):
    """Read from the socket into the queue, then close the connection"""
    logger = logging.getLogger(__name__)
    q.put(read_msg(clsock))
    logger.info("Retreived message from socket")
    clsock.close()
