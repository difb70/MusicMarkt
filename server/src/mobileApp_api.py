import socket
import rsa
import hmac
import hashlib
from cryptography.fernet import Fernet

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 65432

secret_hash = "A09-alameda"


def encryptPublicClient(msg, publicKey):
    return rsa.encrypt(msg.encode('utf-8'), publicKey)

def decryptPrivateAPI(cyphertext, privateKey):
    try:
        return rsa.decrypt(cyphertext, privateKey)
    except:
        return False

def load_secret_key():

    return open("src/keys/api_keys/secretKey.key", "rb").read()

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

    hashed = message[-32:]
    messageEncrypted = message[:-32]

    #shared key decryption
    key_fernet_alg = Fernet(sharedKey)

    try:
        decryptedSecret = key_fernet_alg.decrypt(messageEncrypted)
    except:
        return False

    responseEncrypted = decryptedSecret

    response = decryptPrivateAPI(responseEncrypted, privateKey)

    if(response == False):
        return False

    hashes_match = check_hash(secret_hash, response, hashed)
    
    if(not(hashes_match)):
        return False

    if response.decode('utf-8') == "OK":
        return True
    else:
        return False


def sendCode(code):

    with open("src/keys/api_keys/apiPrivate.pem", "rb") as f:
        apiPrivateKey = rsa.PrivateKey.load_pkcs1(f.read())

    with open("src/keys/api_keys/clientPublic.pem", "rb") as f:
        clientPublicKey = rsa.PublicKey.load_pkcs1(f.read())

    secretKey = load_secret_key()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((SERVER_HOST, SERVER_PORT))

        prints = code

        messageToEncrypt = code

        hash_to_send = hash_hmac(secret_hash, code)

        encryptedPublicResponse = encryptPublicClient(messageToEncrypt, clientPublicKey)

        key_fernet = Fernet(secretKey)
        encryptedResponse = key_fernet.encrypt(encryptedPublicResponse)

        encryptedResponse = encryptedResponse + hash_to_send

        sock.sendall(encryptedResponse)
        print("Sent: " + prints)

        while True:
            data = sock.recv(1024)
            if not data:
                break

            verification = verifyMessage(data, apiPrivateKey, secretKey, secret_hash)
            
            print(verification)

            if (verification == True):
                return True
            else:
                return False

                