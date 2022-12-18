import os

def print_MusicMarkt():
    print("----------------------------------------------------------------")
    print("                         MusicMarkt                             ")
    print("----------------------------------------------------------------\n")


#########################################################
#
# Initial interface
#
#########################################################
def initial_interface(error):

    if error == False:
        print("\n")
    print("----------------------------------------------------------------")
    print("                   Welcome to MusicMarkt                        ")
    print("----------------------------------------------------------------\n")
    
    if error == False:
        print("Please, select one of the following options:\n")
    
    else:
        print("Insert a valid command:\n")
    
    print("1. Login")
    print("2. Register\n")
    command = input(">> ")

    try:
        command = int(command)
    except ValueError:
        command = 3

    os.system('clear')

    return command


#########################################################
#
# Login interface
#
#########################################################
def login_interface(status):
    print_MusicMarkt()
    
    if status == 0:
       print("Invalid username/password, please try again\n")
    elif status == -1:
        print("Something went wrong, try again\n")

    username = input("username: ")
    password = input("password: ")
    os.system('clear')

    return (username, password)



#########################################################
#
# Register interface
#
#########################################################
def register_interface():
    print_MusicMarkt()
    username = input("username: ")
    password = input("password: ")
    email = input("email: ")
    os.system('clear')

    return (username, password, email)