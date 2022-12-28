import socket
import rsa
from cryptography.fernet import Fernet

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 65432

# encrypt server -> client : privAPI -> pubClient
# decrypt client -> server : privAPI -> pubClient

def encryptPublicClient(msg, publicKey):
    return rsa.encrypt(msg.encode('utf-8'), publicKey)

def decryptPrivateAPI(cyphertext, privateKey):
    try:
        return rsa.decrypt(cyphertext, privateKey).decode('utf-8')
    except:
        return False

def load_secret_key():

    return open("client_keys/secretKey.key", "rb").read()



def verifyMessage(message, privateKey, sharedKey):
    #TODO message should be decrypted here and also check for integrity and authenticity
    #TODO if everything checks out

    #TODO integrity

    #shared key decryption
    key_fernet_alg = Fernet(sharedKey)
    decryptedSecret = key_fernet_alg.decrypt(message)

    responseEncrypted = decryptedSecret.decode('utf-8')

    response = decryptPrivateAPI(responseEncrypted, privateKey)

    if(response == False):
        return False

    if response == "OK":
        return True
    else:
        return False

    #TODO if not
    #return False


def sendCode(code):

    with open("api_keys/apiPrivate.pem", "rb") as f:
        apiPrivateKey = rsa.PrivateKey.load_pkcs1(f.read())

    with open("client_keys/clientPublic.pem", "rb") as f:
        clientPublicKey = rsa.PublicKey.load_pkcs1(f.read())

    secretKey = load_secret_key()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((SERVER_HOST, SERVER_PORT))

        # TODO message should be encrypted (guarantees confidentiality, integrity and authenticity)

        #TODO integrity

        messageToEncrypt = code

        encprytedPublic = encryptPublicClient(messageToEncrypt, clientPublicKey)

        key_fernet = Fernet(secretKey)
        encryptedResponse = key_fernet.encrypt(encprytedPublic.encode('utf-8'))
        
        sock.sendall(encryptedResponse)
        print("Sent: " + message)

        while True:
            data = sock.recv(1024)
            if not data:
                break
            
            #TODO decrypt received stuff
            message = data
            print("Received: " + message.decode('utf-8'))

            if (verifyMessage(message, apiPrivateKey, clientPublicKey)):
                return True
            else:
                return False

                