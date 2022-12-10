# SIRS

### This on Router
. _iptables -t nat -A PREROUTING -p tcp -i enp0s3 --dport 5000 -j DNAT --to-destination 192.168.0.100:5000_\
. _iptables -A FORWARD -p tcp -d 192.168.0.100 --dport 5000 -m state --state NEW,ESTABLISHED,RELATED -j ACCEPT_


### This on AppServer
. _export FLASK_APP=app_\
. _export FLASK_DEBUG=1_\
. _python3 -m flask run --host=192.168.0.100_


### This on VirtualBox
. _add the following port forwarding rule to the router NAT Network_\
. _&emsp; Rule 2 &emsp; TCP &emsp; 127.0.0.1 &emsp; 5000 &emsp; 10.0.2.15 &emsp; 5000_


### This on Browser (localhost)
. _127.0.0.1:5000_
