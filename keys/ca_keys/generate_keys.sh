#!/bin/sh
rm -fr *.key
rm -fr *.srl
rm -fr *.csr
rm -fr *.crt

echo "generating root CA ..."
sudo openssl req -new -nodes -text -config configuration/ca.cnf \
    -out root_ca.csr -keyout root_ca.key
sudo chmod og-rwx root_ca.key
sudo openssl x509 -req -in root_ca.csr -text -days 365 \
    -signkey root_ca.key -out root_ca.crt
