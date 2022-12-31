import socket
import rsa
from cryptography.fernet import Fernet

HOST = "127.0.0.1"
PORT = 65432

# encrypt client -> server : privClient -> pubAPI
# decrypt server -> client : privClient -> pubAPI

# encriptar com a publica do outro, e depois com o secret

def encryptPublicAPI(msg, publicKey):
    return rsa.encrypt(msg.encode('utf-8'), publicKey)

def decryptPrivateClient(cyphertext, privateKey):
    try:
        return rsa.decrypt(cyphertext, privateKey).decode('utf-8')
    except:
        return False

def loadSecretKey():

    return open("client_keys/secretKey.key", "rb").read()



def verifyMessage(message, privateKey, sharedKey):
    #TODO message should be decrypted here and also check for integrity and authenticity
    #TODO if everything checks out

    #shared key decryption
    key_fernet_alg = Fernet(sharedKey)
    decryptedSecret = key_fernet_alg.decrypt(message)

    responseEncrypted = decryptedSecret
    
    decryptedPrivate = decryptPrivateClient(responseEncrypted, privateKey)

    if(decryptedPrivate == False):
        return False

    #TODO check integrity

    print(decryptedPrivate)
    
    return True



with open("client_keys/clientPrivate.pem", "rb") as f:
    clientPrivateKey = rsa.PrivateKey.load_pkcs1(f.read())

with open("client_keys/apiPublic.pem", "rb") as f:
    apiPublicKey = rsa.PublicKey.load_pkcs1(f.read())

secretKey = loadSecretKey()

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
                    
                    decoded = data.decode('utf-8')

                    #verifymessage, decrypt and print message received by the server

                    message = verifyMessage(data, clientPrivateKey, secretKey)
                    message = True
                    
                    if (message != False):
                        response = "OK"
                    else:
                        response = "NOK"
                    
                    # TODO response should be encrypted (guarantees confidentiality, integrity and authenticity)

                    #TODO integrity

                    encryptedPublicResponse = encryptPublicAPI(response, apiPublicKey)

                    key_fernet = Fernet(secretKey)
                    encryptedResponse = key_fernet.encrypt(encryptedPublicResponse)

                    conn.sendall(encryptedResponse)
        except socket.timeout:
            print("Code: " + response)
            sock.settimeout(None)
            codeReceived = False
            