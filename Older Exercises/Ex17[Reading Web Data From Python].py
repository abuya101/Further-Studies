# Import the tools for network connections
import socket

# Create a TCP socket
mysock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server on port 80 (HTTP)
mysock.connect(('data.pr4e.org', 80))

# Request the assignment's file
# encode() converts the request text into bytes
cmd = 'GET http://data.pr4e.org/intro-short.txt HTTP/1.0\r\n\r\n'.encode()
mysock.sendall(cmd)

# Receive and print the response headers and file contents
while True:
    # Read up to 512 bytes at a time
    data = mysock.recv(512)

    # Stop when no more data is received
    if len(data) < 1:
        break

    # Convert bytes into text without adding extra newlines
    print(data.decode(), end='')

# Close the connection
mysock.close()