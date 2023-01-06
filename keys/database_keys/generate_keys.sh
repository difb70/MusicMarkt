#!/bin/sh
rm -fr *.key
rm -fr *.crt
rm -fr *.csr

echo "generating database server certificate ..."
sudo openssl req -new -nodes -text -config configuration/db.cnf \
    -out database.csr -keyout database.key
sudo chmod og-rwx database.key
sudo chown postgres:postgres database.key
sudo openssl x509 -req -in database.csr -text -days 365 \
  -CA ../ca_keys/root_ca.crt -CAkey ../ca_keys/root_ca.key -CAcreateserial \
  -out database.crt

echo "generating database client certificate ..."
sudo openssl req -new -nodes -text -config configuration/api.cnf \
    -out client.csr -keyout client.key
sudo chmod og-rwx client.key
sudo openssl x509 -req -in client.csr -text -days 365 \
  -CA ../ca_keys/root_ca.crt -CAkey ../ca_keys/root_ca.key -CAcreateserial \
  -out client.crt
