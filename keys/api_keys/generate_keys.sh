#!/bin/sh
rm -fr *.pem
rm -fr *.srl
rm -fr *.csr

echo "generating https cetificate ..."
openssl genrsa -out api_server.key.pem 4096
openssl req -new -config configuration/api.cnf -key api_server.key.pem -out api_server.csr
openssl x509 -req -days 365 -in api_server.csr -CA ../ca_keys/ca.cert.pem -CAkey ../ca_keys/ca.key.pem -out api_server.cert.pem

