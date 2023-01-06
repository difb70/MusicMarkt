#!/bin/sh
API="192.168.0.100"
API_PORT="5000"
AUTH_PORT="65432"
DMZ="192.168.0.0/24"

DATABASE="192.168.1.1"
DB_PORT="5432"
INT_NET="192.168.1.0/24"

CLIENT="10.0.2.2"

# clean previous configuration
sudo iptables -F
sudo iptables -t nat -F

# set all chains to a whitelisting stratagy
sudo iptables -P INPUT DROP
sudo iptables -P FORWARD DROP
sudo iptables -P OUTPUT DROP

### external firewall rules ###

# External <--> API connection

sudo iptables -A FORWARD -p tcp -d $API --dport $API_PORT -m state --state NEW,ESTABLISHED,RELATED -j ACCEPT
sudo iptables -A FORWARD -p tcp -s $API --sport $API_PORT -m state --state ESTABLISHED,RELATED -j ACCEPT

sudo iptables -A FORWARD -p tcp -d $API --dport $AUTH_PORT -m state --state NEW,ESTABLISHED,RELATED -j ACCEPT
sudo iptables -A FORWARD -p tcp -s $API --sport $AUTH_PORT -m state --state NEW,ESTABLISHED,RELATED -j ACCEPT


# > route packets destined to the router on port 5000 to the API server
sudo iptables -t nat -A PREROUTING -d 10.0.2.9 -p tcp --dport $API_PORT -j DNAT --to-destination "${API}:${API_PORT}"
sudo iptables -t nat -A PREROUTING -s $API -p tcp --sport $AUTH_PORT --dport $AUTH_PORT -j DNAT --to-destination "${CLIENT}:${AUTH_PORT}"
###############################


### internal firewall rules ###

# API <--> Database connection
sudo iptables -A FORWARD -s $API -d $DATABASE -p tcp --dport $DB_PORT -m state --state NEW,ESTABLISHED -j ACCEPT
sudo iptables -A FORWARD -s $DATABASE -d $API -p tcp --sport $DB_PORT -m state --state ESTABLISHED -j ACCEPT

##############################
