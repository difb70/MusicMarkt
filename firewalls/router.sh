# clean previous configuration
sudo iptables -F

# set default policy of forward chain to be accept
# final version will be drop (just allowing the connections
# specified by the rules)
sudo iptables -P INPUT DROP
sudo iptables -P FORWARD ACCEPT
sudo iptables -P OUTPUT DROP

# external firewall rules

# internal firewall rules


# internet access
sudo iptables -t nat -F
sudo iptables -t nat -A POSTROUTING  -o enp0s9 -j MASQUERADE
