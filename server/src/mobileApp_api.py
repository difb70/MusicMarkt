import socket

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 65432

def verifyMessage(message):
    #TODO message should be decrypted here and also check for integrity and authenticity
    #TODO if everything checks out
    if message == "OK":
        return True
    else:
        return False

    #TODO if not
    #return False

def sendCode(code):

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((SERVER_HOST, SERVER_PORT))

        # TODO message should be encrypted (guarantees confidentiality, integrity and authenticity)
        message = code
        
        sock.sendall(message.encode('utf-8'))
        print("Sent: " + message)

        while True:
            data = sock.recv(1024)
            if not data:
                break

            message = data.decode('utf-8')
            print("Received: " + message)

            if (verifyMessage(message)):
                return True
            else:
                return False

                