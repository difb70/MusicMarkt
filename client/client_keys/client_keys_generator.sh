openssl genrsa -out clientPrivate.pem 2048
openssl rsa -in clientPrivate.pem -outform PEM -RSAPublicKey_out -out clientPublic.pem