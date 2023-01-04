import random

def generate_base64_string(length: int):
    
    return "%014x" % random.randrange(16 ** length)

def generate_secret_save():
    hash_string = generate_base64_string(14)

    hash_string = hash_string.encode('utf-8')

    with open('secretKey.txt', 'wb') as mykey:
            mykey.write(hash_string)

generate_secret_save()