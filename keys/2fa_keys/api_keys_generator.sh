openssl genrsa -out apiPrivate.pem 2048
openssl rsa -in apiPrivate.pem -outform PEM -pubout -out apiPublic.pem