import socket
import ssl
import os
import signal
from processTLSMessage import *
from processTCPMessage import *

HOST = "localhost"
PORT_TLS = 60000
PORT_TCP = 60001

serverTLS = None
serverTCP = None

#########################################################
#
# Will close the TLS and TCP sockets and respective 
# processes
#
#########################################################
def handler(signum, frame):

    global serverTLS
    global serverTCP

    serverTLS.close()
    serverTCP.close()
    os.kill(0, signal.SIGTERM)
    os.kill(1, signal.SIGTERM)


#########################################################
#
# Will create the TLS socket
#
#########################################################
def create_TLS_socket():

    global serverTLS

    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain('../certificate_related/example.com.crt', '../certificate_related/example.com.key')
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST, PORT_TLS))
    sock.listen(5)
    serverTLS = context.wrap_socket(sock, server_side=True)


#########################################################
#
# Will create the TCP socket
#
#########################################################
def create_TCP_socket():

    global serverTCP
   
    serverTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverTCP.bind((HOST, PORT_TCP))
    serverTCP.listen(5)


#########################################################
#
# Main
#
#########################################################
if __name__ == "__main__":

    create_TLS_socket()
    create_TCP_socket()
    
    signal.signal(signal.SIGINT, handler)

    processTLS = os.fork()

    if processTLS:
        process_TLS_message(serverTLS)
    
    else:
        process_TCP_message(serverTCP)
