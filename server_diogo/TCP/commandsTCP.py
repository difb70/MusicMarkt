def process_login(request):
    
    if (len(request) != 3):
        return "LGN NOK\n"
    
    username = request[1]
    password = request[2]
    
    # TODO Access DB

    # TODO If there is a user, return OK
    response = "LGN OK\n"

    # TODO If there isn't, return NOK
    # response = "LGN NOK"

    return response
