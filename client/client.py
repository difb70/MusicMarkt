import socket
import ssl
import sys

sys.path.append("TCP")
sys.path.append("TLS")

from interfaces import *
from commandsTCP import *
from commandsTLS import *


#########################################################
#
# Main
#
#########################################################
if __name__ == "__main__":

    #clientTLS = create_TLS_socket()

    #clientTLS.connect((SERVER_HOST, SERVER_PORT_TLS))

    command = initial_interface(False)

    while True:

        if command == 1:
            status = 1
            
            while True:
                username, password = login_interface(status)
                status = login_TCP(username, password)
                if status == 1:
                    break
            break

        elif command == 2:
            username, password, email = register_interface()
            register_TCP(username, password, email)
            break

        else:
            command = initial_interface(True)

    while True:
        from time import sleep

        clientTLS.send("Hello World with TLS!".encode("utf-8"))
        sleep(1)