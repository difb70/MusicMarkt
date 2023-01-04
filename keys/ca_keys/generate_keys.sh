#!/bin/sh
rm -fr *.pem
rm -fr *.srl
rm -fr *.csr

echo "generating root CA ..."
openssl genrsa -out ca.key.pem 4096
openssl req -new -nodes -config configuration/ca.cnf -key ca.key.pem -out ca.csr
openssl x509 -req -days 365 -in ca.csr -signkey ca.key.pem -out ca.cert.pem
echo 01 > ca.cert.srl
