from processTCPMessage import *


#########################################################
#
# Login
#
#########################################################
def login_TCP(username, password):
    message = "LGN " + username + " " + password + "\n"
    response = process_TCP_message(message)

    if response == "LGN OK\n":
        return 1
    elif response == "LGN NOK\n":
        return 0
    elif response == "ERR":
        return -1

#########################################################
#
# Register
#
#########################################################
def register_TCP(username, password, email):
    message = "RGS " + username + " " + password + " " + email + "\n"
    response = process_TCP_message(message)