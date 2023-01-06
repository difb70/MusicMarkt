# MusicMarkt


MusicMarkt is an online store for items related to music, such as CDs, instruments and many others.
Besides these basic shopping functionalities MusicMarkt also has a reservation feature, and a scoreboard system regarding money spent by clients on certain artists or bands, which can give privileges regarding reservations.
The primary focus of this application is its *security*.


## General Information

This application is composed by four main components : 
 - *Web Application*
 - *Database*
 - *Client*
 - *Router*


### Built With
#### Database 
The technology used for the database was PostgreSQL.
- [PostgreSQL](https://www.postgresql.org/) - Relational Database Management System

#### Web Application
Implemented using Flask a python web framework. The communication with the database is done through a custom API created using `psycopg2` python library. The database API creates a high level interface with the database.
- [Python3](https://www.python.org/) - Programming language 
- [Flask](https://flask.palletsprojects.com/en/2.2.x/) - Web framework
- [Psycopg2](https://www.psycopg.org/docs/) - PostgreSQL communication library


## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

The MusicMarkt service is provided by three machines (application server, database and a router). All this machines are virtualized in the testing environment and are running an Ubuntu distribution.

There is some software that needs to be installed in each machine : 
- Database
    ```shell
    # install postgreSQL
    sudo apt update
    sudo apt install postgresql postgresql-contrib
    ```

- Application Server
    ```shell
    # install python modules
    pip install flask
    pip install rsa
    pip install psycopg2-binary
    ```


### Installing

Specific setup and installation steps for each machine are specified in following `README.md`:
- /server/README.md  - Instructions on how to setup the application server
- /client/README.md  - Instructions on how to setup the client mobile app 
- /database/README.md - Instructions on how to setup the database

The setup of the system must be done in the following order:
    1. Database
    2. Client
    3. Application Server

## Deployment

1. Setup firewall rules in the respective machines (this rules are stored in scripts inside the folder `/firewalls/`)
    ```shell
    # on the router
    ./firewalls/router.sh
    ./firewalls/save_firewall.sh

    # on the api
    ./firewalls/api.sh
    ./firewalls/save_firewall.sh

    # on the database
    ./firewalls/database.sh
    ./firewalls/save_firewall.sh
    ```
2. Make sure that the database is running and accessible from the application server
    ``` shell
    # on the database
    sudo service postgresql status
    ```
3. Run the client mobile app
    ``` shell
    # on the client
    python3 /client/mobileApp.py
    ```
4. Run the server
    ``` shell
    # on the application server
    cd /server/
    ./run.sh
    ```

## Additional Information
### Authors

* **Diogo Braz, 95557** - [difb70](https://github.com/difb70)
* **João Ramalho, 95599** - [WhoIsGinja](https://github.com/WhoIsGinja)
* **Tomás Tavares, 95680** - [Th0mz](https://github.com/Th0mz)
