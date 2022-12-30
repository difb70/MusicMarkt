#!/bin/sh
API="192.168.0.100"
API_PORT="5000"
DMZ="192.168.0.0/24"

DATABASE="192.168.1.1"
DB_PORT="5432"
INT_NET="192.168.1.0/24"

# clean previous configuration
sudo iptables -F
sudo iptables -t nat -F

# set all chains to a whitelisting stratagy
sudo iptables -P INPUT DROP
sudo iptables -P FORWARD ACCEPT
sudo iptables -P OUTPUT DROP

### external firewall rules ###

# External <--> API connection

sudo iptables -A FORWARD -d $API -p tcp --dport $API_PORT -m state --state NEW,ESTABLISHED,RELATED -j ACCEPT
# > route packets destined to the router on port 5000 to the API server
sudo iptables -t nat -A PREROUTING -i enp0s9 -p tcp -j DNAT --to-destination "${API}:${API_PORT}"

###############################


### internal firewall rules ###

# API <--> Database connection
sudo iptables -A FORWARD -s $API -d $DATABASE -p tcp --dport $DB_PORT -m state --state NEW,ESTABLISHED -j ACCEPT
sudo iptables -A FORWARD -s $DATABASE -d $API -p tcp --sport $DB_PORT -m state --state ESTABLISHED -j ACCEPT

##############################
