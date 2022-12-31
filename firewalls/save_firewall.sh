# FOR IPv4
sudo sh -c 'iptables-save > /etc/iptables/rules.v4'
# FOR IPv6
sudo sh -c 'ip6tables-save > /etc/iptables/rules.v6'
