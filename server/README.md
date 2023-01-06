## API
The API server is the main component of this project. It's main purpose is to serve the webapp service and make the communication with the database.

### Setup

1. Enable packet forwarding form host machine to the virtual machine
a. On VirtualBox version 7 press `ctrl + h`
b. Goto the `NAT Networks > Port Forwarding` tab 
c. Add the following rule :
    ```
    # name   protocol    host ip   host port   guest ip    guest port
    Rule 1     TCP      127.0.0.1    5000      10.0.2.?       5000

    # the host ip to use can be found in the router  
    # machine running ifconfig, use the ip associated 
    # with the nat network interface 
    ```
    
2. Setup firewalls in all machines, but most importantly on the router
    ```shell
    # on the router
    /musicmarkt/firewalls/router.sh
    /musicmarkt/firewalls/save_firewall.sh

    # on the api
    /musicmarkt/firewalls/api.sh
    /musicmarkt/firewalls/save_firewall.sh

    # on the database
    /musicmarkt/firewalls/database.sh
    /musicmarkt/firewalls/save_firewall.sh
    ```

3. Generate keys and certificates for the API:
    ```shell
    # if the root CA where not already generated (the root CA certificate must be the same to sign all other certificates)
    ./musicmarkt/keys/ca_keys/generate_keys.sh

    # generate api key pair and associated certificate
    ./musicmarkt/keys/api_keys/generate_keys.sh
    ```

4. Generate database client keys and certificates : 
    ```shell
    # assuming that the root CA was already created
    # generate database client key pair and associated certificate
    ./musicmarkt/keys/api_keys/generate_keys.sh
    ```

<br>

---
### Run
```shell
cd /musicmarkt/server
./run.sh
```