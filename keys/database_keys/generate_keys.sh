#!/bin/sh
rm -fr *.pem
rm -fr *.srl
rm -fr *.csr

echo "generating database server certificate ..."
openssl genrsa -out db_server.key.pem 4096
openssl req -new -config configuration/db.cnf -key db_server.key.pem -out db_server.csr
# self sign
openssl x509 -req -days 365 -in db_server.csr -signkey db_server.key.pem -out db_server.cert.pem
echo 01 > db_server.cert.srl


echo "generating database client certificate ..."
openssl genrsa -out db_client.key.pem 4096
openssl req -new -config configuration/api.cnf -key db_client.key.pem -out db_client.csr
openssl x509 -req -days 365 -in db_client.csr -CA ../ca_keys/ca.cert.pem -CAkey ../ca_keys/ca.key.pem -out db_client.cert.pem
