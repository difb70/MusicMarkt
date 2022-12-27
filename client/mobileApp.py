import socket
import rsa

HOST = "127.0.0.1"
PORT = 65432

# encrypt client -> server : privClient -> pubAPI
# decrypt server -> client : privClient -> pubAPI

#fazer uma signature para cada

#pode ser util para mensagens que sabe se que sao sempre iguais
#signature = rsa.sign(message.encode(), private_key, "SHA-256")

def encryptPrivateClient(msg, privateKey):
    return rsa.encrypt(msg.enconde('utf-8'), privateKey)

def encryptPublicAPI(msg, publicKey):
    return rsa.encrypt(msg.enconde('utf-8'), publicKey)

# KprivClient(KpubAPI(M))

def decryptPrivateClient(cyphertext, privateKey):
    try:
        return rsa.decrypt(cyphertext, privateKey).decode('utf-8')
    except:
        return False

def decryptPublicAPI(cyphertext, publicKey):
    try:
        return rsa.decrypt(cyphertext, publicKey).decode('utf-8')
    except:
        return False



def verifyMessage(message, privateKey, publicKey):
    #TODO message should be decrypted here and also check for integrity and authenticity
    #TODO if everything checks out
    
    decryptedPrivate = decryptPrivateClient(message, privateKey)

    if(decryptedPrivate == False):
        return False

    response = decryptPublicAPI(decryptedPrivate, publicKey)

    if(response == False):
        return False
    
    return response



with open("client_keys/clientPrivate.pem", "rb") as f:
    clientPrivateKey = rsa.PrivateKey.load_pkcs1(f.read())

with open("api_keys/apiPublic.pem", "rb") as f:
    apiPublicKey = rsa.PublicKey.load_pkcs1(f.read())

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
                    
                    message = verifyMessage(data, clientPrivateKey, apiPublicKey)
                    
                    if (message != False):
                        response = "OK"
                    else:
                        response = "NOK"
                    
                    # TODO response should be encrypted (guarantees confidentiality, integrity and authenticity)

                    encryptedPrivateResponse = encryptedPrivateResponse(response, clientPrivateKey)
                    encryptedResponse = encryptPublicAPI(encryptedPrivateResponse, apiPublicKey)

                    conn.sendall(encryptedResponse)
        except socket.timeout:
            print("Code: " + message)
            sock.settimeout(None)
            codeReceived = False
            