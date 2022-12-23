import socket

HOST = "127.0.0.1"
PORT = 65432

def verifyMessage(message):
    #TODO message should be decrypted here and also check for integrity and authenticity
    #TODO if everything checks out
    return True

    #TODO if not
    #return False


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.bind((HOST, PORT))
    sock.listen()
    codeReceived = False
    while True:
        if (codeReceived == True):
            sock.settimeout(5)
        try:
            conn, addr = sock.accept()
            codeReceived = True
            with conn:
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    
                    message = data.decode('utf-8')

                    if (verifyMessage(message)):
                        response = "OK"
                    else:
                        response = "NOK"
                    
                    # TODO response should be encrypted (guarantees confidentiality, integrity and authenticity)
                    conn.sendall(response.encode('utf-8'))
        except socket.timeout:
            print("Code: " + message)
            sock.settimeout(None)
            codeReceived = False
            