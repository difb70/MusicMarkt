import socket
import ssl

SERVER_HOST = "localhost"
SERVER_PORT_TLS = 60000
SERVER_PORT_TCP = 60001

#########################################################
#
# Will create the TLS socket
#
#########################################################
def create_TLS_socket():

    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.load_verify_locations('../certificate_related/example.com.crt')

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    clientTLS = context.wrap_socket(sock, server_hostname=SERVER_HOST)

    return clientTLS


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
# Main
#
#########################################################
if __name__ == "__main__":

    clientTLS = create_TLS_socket()
    clientTCP = create_TCP_socket()

    clientTLS.connect((SERVER_HOST, SERVER_PORT_TLS))
    clientTCP.connect((SERVER_HOST, SERVER_PORT_TCP))

    while True:
        from time import sleep

        clientTLS.send("Hello World with TLS!".encode("utf-8"))
        sleep(1)
        clientTCP.send("Hello World with TCP!".encode("utf-8"))
        sleep(1)