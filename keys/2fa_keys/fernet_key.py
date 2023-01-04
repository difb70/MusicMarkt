from cryptography.fernet import Fernet

def generate_key():
    key = Fernet.generate_key()

    return key


fernetKey = generate_key()

with open('secretKey.key', 'wb') as mykey:
            mykey.write(fernetKey)