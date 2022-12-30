# clean previous configuration
sudo iptables -F

# api can only send and receive
# packets never forward them
sudo iptables -P INPUT ACCEPT
sudo iptables -P FORWARD DROP
sudo iptables -P OUTPUT ACCEPT
