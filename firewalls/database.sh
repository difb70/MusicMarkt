# clean previous configuration
sudo iptables -F

# database can only send and receive
# packets never forward them
sudo iptables -P INPUT ACCEPT
sudo iptables -P FORWARD DROP
sudo iptables -P OUTPUT ACCEPT
