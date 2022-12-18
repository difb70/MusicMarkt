def process_TCP_message(serverTCP):
    while True:
            connection, client_address = serverTCP.accept()
            while True:
                data = connection.recv(1024)
                if not data:
                    break
                print(f"Received: {data.decode('utf-8')}")
                print("From: " + client_address[0])