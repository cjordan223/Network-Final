#!env python

# This is a simple tls server for CST311 Programming Assignment 4.
__author__ = "NeoWeb"
__credits__ = ["Nathan Nawrocki", "Tyler Thompson",
               "Matthew Perona", "Conner Jordan"]

import socket as s
import ssl
import logging

logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


class SimpleTlsServer:
    """
    This is a secure TCP server that listens on a specific port and IP address.
    It uses SSL/TLS for secure communication and converts received sentences to uppercase.

    Attributes:
    - server_port (int): The port on which the server listens for incoming connections.
    - server_ip (str): The IP address on which the server binds and waits for client connections.
    - cert_path (str): The file path to the server's SSL/TLS certificate.
    - key_path (str): The file path to the server's private key.
    - context (ssl.SSLContext): An SSL/TLS context for the server, used for secure communication.
    - serverSocket (socket.socket): The server socket for TCP communication over IPv4.

    This class represents a secure TCP server that can accept incoming client connections.
    It initializes with the provided configuration, including the port, IP address, certificate, and private key paths.
    The server uses SSL/TLS to ensure secure communication with clients.
    It listens for incoming connections, wraps them in SSL/TLS for encryption, and processes client messages.

    Methods:
    - start(self): Start the server by binding to the specified IP address and port and listening for incoming connections.
    """

    def __init__(self, server_port, server_ip, cert_path, key_path):
        """
        Initialize the SecureTCPServer with the provided configuration.

        Args:
        - server_port (int): The port on which the server listens for incoming connections.
        - server_ip (str): The IP address on which the server binds and waits for client connections.
        - cert_path (str): The file path to the server's SSL/TLS certificate.
        - key_path (str): The file path to the server's private key.

        This constructor sets up the server with the specified configuration, including the port and IP address
        for listening, as well as the paths to the SSL/TLS certificate and private key for secure communication.
        It also creates an SSL/TLS context and loads the server's certificate and key into it.
        """

        self.server_port = server_port
        self.server_ip = server_ip
        self.cert_path = cert_path
        self.key_path = key_path

        self.context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        try:
            self.context.load_cert_chain(self.cert_path, self.key_path)
            log.debug("Successfully loaded certificate and key.")
        except Exception as e:
            log.error(f"Failed to load certificate and key: {e}")

        self.serverSocket = s.socket(s.AF_INET, s.SOCK_STREAM)

    def start(self):
        """
        Start the server by binding to the specified IP address and port and listening for incoming connections.

        This method does the following:
        - Binds the server socket to a specific IP address and port.
        - Listens for incoming connections with a backlog of 5.
        - Enters a listening loop to accept incoming connections.
        - Accepts incoming connections, creates a connection socket, and wraps it with SSL/TLS for secure communication.
        - Receives a sentence from the client, decodes it, and converts it to uppercase.
        - Encodes the uppercase sentence and sends it back to the client.
        - Closes the secure connection socket and the connection socket.
        """

        self.serverSocket.bind((self.server_ip, self.server_port))
        self.serverSocket.listen(5)
        log.info(f"The server is ready to receive on port {self.server_port}")

        while True:
            connectionSocket, addr = self.serverSocket.accept()
            secureConnSocket = self.context.wrap_socket(
                connectionSocket, server_side=True)
            sentence = secureConnSocket.recv(1024).decode()
            capitalizedSentence = sentence.upper()
            secureConnSocket.send(capitalizedSentence.encode())
            secureConnSocket.close()
            connectionSocket.close()


if __name__ == "__main__":
    # Server configuration
    server_port = 12000
    server_ip = '10.0.1.2'
    cert_path = '/etc/ssl/demoCA/newcerts/webserver-cert.pem'
    key_path = '/etc/ssl/demoCA/private/webserver-key.pem'

    # Create and start the server
    server = SimpleTlsServer(server_port, server_ip, cert_path, key_path)
    server.start()
