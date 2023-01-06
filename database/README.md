# Database : 
The chosen database was PostgreSQL, because the group had already some experience with it and given how easy it is to setup

### Setup :
1. Download postgres into your machine

```shell
sudo apt update
sudo apt install postgresql postgresql-contrib
```

2. Switch user for postgres

```shell
sudo su postgres
```

3.  Open an interactive shell to the PostgreSQL service
```shell
psql
```

4. Create a new user and the MusicMarkt database
```shell
# create user
CREATE USER <user-name> WITH PASSWORD <password>;

# create database
CREATE DATABASE musicmarkt
```

5. Create and populate tables 
```shell
# change to musicmarkt database
\c musicmarkt

\i setup.sql
\i populate.sql
```


#### Setup SSL
1. Enable and configure SLL connections on `postgresql.conf` file
``` python
# uncomment listen_addresses and make it equal "192.168.1.1 (local ipv4)"
listen_addresses = '192.168.1.1'
# (...)

# configure ssl properties 
# - SSL -
ssl = on
ssl_ca_file = '/etc/postgresql/12/main/root_ca.crt'
ssl_cert_file = '/etc/postgresql/12/main/database.crt'
#ssl_crl_file = ''
ssl_key_file = '/etc/postgresql/12/main/database.key'
```

2. Generate the database certificates
```shell
# generate root CA certificate and key if not already generated
./musicmarkt/keys/ca_keys/generate_keys.sh

# generate database certificate and key
./musicmarkt/keys/database_keys/generate_keys.sh

# copy the generated files to the postgres directory
sudo cp ~/musicmarkt/keys/database_keys/database.crt \
        /etc/postgresql/12/main/
sudo cp ~/musicmarkt/keys/database_keys/database.key \
        /etc/postgresql/12/main/
sudo cp ~/musicmarkt/keys/ca_keys/root_ca.crt \
        /etc/postgresql/12/main/

# set the ownership of database.key to postgres user and group
sudo chown postgres:postgres /etc/postgresql/12/main/database.key

```

3. Add a rule to `pg_hba.conf` that defines in which conditions the user can access the *musicmarkt* database 
```
host    musicmarkt      <user-name>           192.168.0.0/24          md5 clientcert=verify-full

# this rule allows the access to musicmarkt database if : 
    - the user credentials are supplied correctly
    - client is accessing it from the 192.168.0.0/24 subnet
    - client supplies a certificate signed by our root CA
```

---
