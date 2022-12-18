from commandsTCP import *

def process_TCP_message(serverTCP):
    while True:
            connection, client_address = serverTCP.accept()
            request = connection.recv(1024)
            if not request:
                break
            request = request.decode('utf-8')

            print("Received: " + request)

            request = request.split()

            command = request[0]
            
            if command == "LGN":
                
                response = process_login(request)
                print("Sent: " + response + "\n" + "\n")
                connection.send(response.encode("utf-8"))
