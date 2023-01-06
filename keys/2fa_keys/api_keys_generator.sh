openssl genrsa -out apiPrivate.pem 2048
openssl rsa -in apiPrivate.pem -outform PEM -RSAPublicKey_out -out apiPublic.pem