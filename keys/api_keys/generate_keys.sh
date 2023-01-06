#!/bin/sh
rm -fr *.key
rm -fr *.crt
rm -fr *.csr


echo "generating database server certificate ..."
sudo openssl req -new -nodes -text -config configuration/api.cnf \
    -out api.csr -keyout api.key
sudo chmod og-rwx api.key
sudo openssl x509 -req -in api.csr -text -days 365 \
  -CA ../ca_keys/root_ca.crt -CAkey ../ca_keys/root_ca.key -CAcreateserial \
  -out api.crt -extfile configuration/v3.ext
