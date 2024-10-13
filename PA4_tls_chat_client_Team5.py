#!env python

# This is a chat client for CST311 Programming Assignment 4.
__author__ = "NeoWeb"
__credits__ = ["Nathan Nawrocki", "Tyler Thompson",
               "Matthew Perona", "Conner Jordan"]

import socket as s
import ssl
import logging

# Configure logging
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

# Define the server information
server_name = 'chat.webpa4.test'  # Server hostname
server_port = 12000  # Server port number
certfile = '/etc/ssl/demoCA/cacert.pem'  # Path to the CA certificate

# Create an SSL context with default settings and load the CA certificate
context = ssl.create_default_context()
context.load_verify_locations(certfile)


def main():
    """
    Main function to run the chat client.

    This function performs the following steps:
    1. Creates a regular TCP socket for the client.
    2. Wraps the regular socket with SSL/TLS using the server's hostname.
    3. Establishes a connection to the server.
    4. Enters a loop to send user input as messages to the server.
    5. Receives and displays responses from the server.
    6. Closes the connection when a response is received.

    """
    # Difference: Wraps client socket with TLS
    client_socket = s.socket(s.AF_INET, s.SOCK_STREAM)
    try:
        secure_socket = context.wrap_socket(
            client_socket, server_hostname=server_name)
        secure_socket.connect((server_name, server_port))
        log.debug("SSL handshake succeeded.")
    except Exception as e:
        log.exception(e)
        exit(8)

    # Get user input
    user_input = input('Input lowercase sentence:')

    # Send and receive data
    secure_socket.send(user_input.encode())
    server_response = secure_socket.recv(1024)
    server_response_decoded = server_response.decode()

    print('From Server:')
    print(server_response_decoded)

    # Close the socket after receiving server response
    if server_response_decoded:
        secure_socket.close()


if __name__ == "__main__":
    main()
