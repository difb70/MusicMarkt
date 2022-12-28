openssl genrsa -out clientPrivate.pem 2048
openssl rsa -in clientPrivate.pem -outform PEM -pubout -out clientPublic.pem