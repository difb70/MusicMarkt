import socket
import rsa
import hmac
import hashlib
from cryptography.fernet import Fernet

HOST = "127.0.0.1"
PORT = 65432

def encryptPublicAPI(msg, publicKey):
    return rsa.encrypt(msg.encode('utf-8'), publicKey)

def decryptPrivateClient(cyphertext, privateKey):
    try:
        return rsa.decrypt(cyphertext, privateKey)
    except:
        return False

def loadSecretKey():

    return open("client_keys/secretKey.key", "rb").read()

def hash_hmac(key, message):
    hash_object = hmac.new(key.encode(), message.encode(), hashlib.sha256)

    hmac_value = hash_object.digest()

    return hmac_value

def check_hash(key, messageBytes, hash):
    hash_object = hmac.new(key.encode(), messageBytes, hashlib.sha256)

    hmac_value = hash_object.digest()

    if(hmac_value == hash):
        return True
    else:
        return False


def verifyMessage(message, privateKey, sharedKey, secret_hash):

    #separate the encypted stuff from the hash
    hashed = message[-32:]
    messageEncrypted = message[:-32]

    #shared key decryption
    key_fernet_alg = Fernet(sharedKey)
    decryptedSecret = key_fernet_alg.decrypt(messageEncrypted)

    responseEncrypted = decryptedSecret
    
    decryptedPrivate = decryptPrivateClient(responseEncrypted, privateKey)

    if(decryptedPrivate == False):
        return False

    hashes_match = check_hash(secret_hash, decryptedPrivate, hashed)

    if(hashes_match):
        print("2FA code: " + decryptedPrivate.decode('utf-8'))

        return True
    else:
        print("ERROR: problems with the communication channel")

        return False



with open("client_keys/clientPrivate.pem", "rb") as f:
    clientPrivateKey = rsa.PrivateKey.load_pkcs1(f.read())

with open("client_keys/apiPublic.pem", "rb") as f:
    apiPublicKey = rsa.PublicKey.load_pkcs1(f.read())

secretKey = loadSecretKey()

secret_hash = "A09-alameda"

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

                    message = verifyMessage(data, clientPrivateKey, secretKey, secret_hash)
                    
                    if (message != False):
                        response = "OK"
                    else:
                        response = "NOK"

                    hash_to_send = hash_hmac(secret_hash, response)

                    encryptedPublicResponse = encryptPublicAPI(response, apiPublicKey)

                    key_fernet = Fernet(secretKey)
                    encryptedResponse = key_fernet.encrypt(encryptedPublicResponse)

                    encryptedResponse = encryptedResponse + hash_to_send

                    conn.sendall(encryptedResponse)
        except socket.timeout:
            print("Code: " + response)
            sock.settimeout(None)
            codeReceived = False
            