import socket
import sys

sys.path.append("../")

from connection_settings import *

#########################################################
#
# Will create the TCP socket
#
#########################################################
def create_TCP_socket():

    clientTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    return clientTCP


#########################################################
#
# Will send and receive a message over the TCP socket
#
#########################################################
def process_TCP_message(message):

    clientTCP = create_TCP_socket()
    clientTCP.connect((SERVER_HOST, SERVER_PORT_TCP))

    # TODO Encrypt message here before sending
    clientTCP.send(message.encode("utf-8"))

    response = clientTCP.recv(8)
    # TODO Decrypt message here before reading it
    
    if not response:
        return "ERR"

    response = response.decode('utf-8')

    return response