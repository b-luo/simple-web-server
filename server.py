import socket

SERVER_HOST = '0.0.0.0'
SERVER_PORT = 8000

# Socket - OS abstraction for sending/getting bytes through a network
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Setting option SO_REUSEADDR prevents OSError caused by accessing
# server repeatedly
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((SERVER_HOST, SERVER_PORT))
# Enable server to accept connections
# Arg. is # unaccepted connections allowed
server_socket.listen(1)
print("Listening on port %s..." % SERVER_PORT)

while True:
    # Wait for client to connect & send request to server
    client_connection, client_address = server_socket.accept()
    request = client_connection.recv(1024).decode()
    print(request)

    # Parse HTTP headers - used to pass info. between client & server
    header = request.split('\n')
    filename = header[0].split()[1]
    
    if filename == '/':
        filename = 'index.html'

    try:
        with open(filename, 'r') as f:
            content = f.read()

        # Send HTTP formatted string
        response = "HTTP/1.0 200 OK\n\n" + content
    except FileNotFoundError:
        response = "HTTP/1.0 404 NOT FOUND\n\n<b>Page not found<b>"

    client_connection.sendall(response.encode())
    client_connection.close()

server_socket.close()

