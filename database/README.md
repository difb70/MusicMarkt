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

6. Make the database available for LAN devices
```shell
\q
exit
sudo nano /etc/postgresql/12/main/postgresql.conf
# uncomment listen_addresses and make it equal "192.168.1.1 (local ipv4)"
# verify that the property ssl is uncommented and with value on

sudo nano /etc/postgresql/12/main/postgresql/pg_hba.conf
# add the following line : 
# host    musicmarkt      <user-name>           192.168.0.0/24          md5 clientcert=verify-full
```

---
