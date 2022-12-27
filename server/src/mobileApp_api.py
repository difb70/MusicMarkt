import socket
import rsa

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 65432

# encrypt server -> client : privAPI -> pubClient
# decrypt client -> server : privAPI -> pubClient

def encryptPrivateAPI(msg, privateKey):
    return rsa.encrypt(msg.enconde('ascii'), privateKey)

def encryptPublicClient(msg, publicKey):
    return rsa.encrypt(msg.enconde('ascii'), publicKey)

# KprivAPI(KpubClient(M))

def decryptPrivateAPI(cyphertext, privateKey):
    try:
        return rsa.decrypt(cyphertext, privateKey).decode('ascii')
    except:
        return False

def decryptPublicClient(cyphertext, publicKey):
    try:
        return rsa.decrypt(cyphertext, publicKey).decode('ascii')
    except:
        return False


def verifyMessage(message, privateKey, publicKey):
    #TODO message should be decrypted here and also check for integrity and authenticity
    #TODO if everything checks out

    decryptedPrivate = decryptPrivateAPI(message, privateKey)

    if(decryptedPrivate == False):
        return False

    response = decryptPublicClient(decryptedPrivate, publicKey)

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

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((SERVER_HOST, SERVER_PORT))

        # TODO message should be encrypted (guarantees confidentiality, integrity and authenticity)


        messageToEncrypt = code

        encpryptedPrivately = encryptPrivateAPI(messageToEncrypt, apiPrivateKey)

        message = encryptPublicClient(encpryptedPrivately, clientPublicKey)
        
        sock.sendall(message)
        print("Sent: " + message)

        while True:
            data = sock.recv(1024)
            if not data:
                break

            message = data.decode('utf-8')
            print("Received: " + message)

            if (verifyMessage(message, apiPrivateKey, clientPublicKey)):
                return True
            else:
                return False

                