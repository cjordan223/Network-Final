#!env python

# This is a chat server for CST311 Programming Assignment 4.
# It handles SSL/TLS connections from clients, processes messages, and sends responses.
__author__ = "NeoWeb"
__credits__ = ["Nathan Nawrocki", "Tyler Thompson",
               "Matthew Perona", "Conner Jordan"]

# Import necessary libraries
import socket as s
import ssl
import logging
import threading

# Set up logging for debugging
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

# Server configuration
server_port = 12000
server_ip = '10.0.2.2'  # Difference: Defines ip of h4

# Lists to store client data and connections and order of client connections
clients_data = []
clients_connections = []
clients_order_of_connection = []

# Lock for thread safety
data_lock = threading.Lock()

# Difference: Loads paths to chat server certificate and private key
cert_path = '/etc/ssl/demoCA/newcerts/chatserver-cert.pem'
key_path = '/etc/ssl/demoCA/private/chatserver-key.pem'

# Difference: Create an SSL/TLS context for the server
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
try:
    context.load_cert_chain(cert_path, key_path)
    log.debug("Successfully loaded certificate and key.")
except Exception as e:
    log.error(f"Failed to load certificate and key: {e}")


def process_messages():
    """
    Process and send messages to clients.

    This function performs the following tasks:
    - Determines the order of message reception between two clients.
    - Formats the response message based on the order of message reception.
    - Sends the formatted response to all connected clients.
    - Clears the data and connections lists for the next pair of clients.

    Note: This function assumes that two messages have been received from clients before processing.

    """
    # Extract information about the two clients
    first_client, second_client = clients_order_of_connection
    first_message_address, first_message_content = clients_data[0]
    second_message_address, second_message_content = clients_data[1]

    # Determine the response format based on the order of message reception
    if first_client == first_message_address:
        response = "X: '{}', Y: '{}'".format(
            first_message_content, second_message_content)
    else:
        response = "Y: '{}', X: '{}'".format(
            first_message_content, second_message_content)

    # Send the response to all connected clients
    for conn in clients_connections:
        conn.send(response.encode())

    # Clear the data and connections lists for the next pair of clients
    clients_data.clear()
    clients_connections.clear()
    clients_order_of_connection.clear()


def connection_handler(secure_conn_socket, address):
    """
    Handle client connections.

    This function performs the following tasks:
    - Successfully completes the SSL handshake with the client.
    - Receives messages from the client via the secure connection.
    - Decodes and logs the received message along with the client's address.
    - Securely stores the received message along with the client's address using thread safety.
    - If two messages are received, it calls the process_messages() function to send responses.

    Args:
    - secure_conn_socket (ssl.SSLSocket): The SSL/TLS-wrapped connection socket.
    - address (tuple): The address (IP and port) of the client.

    Note: Any SSL/TLS handshake errors or general exceptions encountered during the process are logged.

    """
    try:
        log.debug("SSL handshake succeeded.")

        query = secure_conn_socket.recv(1024)
        query_decoded = query.decode()
        log.info(f"Received query text {query_decoded} from address {address}")

        with data_lock:
            clients_data.append((address, query_decoded))
            if len(clients_data) == 2:
                process_messages()
    except ssl.SSLError as e:
        log.error(f"SSL Error during handshake: {e}")
    except Exception as e:
        log.error(f"Error handling connection: {e}")


def main():
    """
    Main function to set up the server.

    This function performs the following steps:
    - Creates a server socket and configures it.
    - Binds the server socket to the specified IP address and port.
    - Listens for incoming client connections with a backlog of 2.
    - Accepts incoming connections, wraps them with SSL/TLS for secure communication, and spawns threads
      to handle each client connection.
    - Continuously listens for client connections and handles them in separate threads.

    Note: The server can handle up to 2 client connections simultaneously.

    When the server is no longer needed, it should be closed to release the resources.

    """
    server_socket = s.socket(s.AF_INET, s.SOCK_STREAM)
    server_socket.setsockopt(s.SOL_SOCKET, s.SO_REUSEADDR, 1)
    # Difference: Binds to h4 ip
    server_socket.bind((server_ip, server_port))
    server_socket.listen(2)
    log.info(f"The server is ready to receive on port {server_port}")

    try:
        while True:
            connection_socket, address = server_socket.accept()
            log.info(f"Connected to client at {address}")
            clients_order_of_connection.append(address)
            # Difference: Wraps client sockets with TLS
            secure_conn_socket = context.wrap_socket(
                connection_socket, server_side=True)

            clients_connections.append(secure_conn_socket)

            if len(clients_connections) == 2:
                for conn in clients_connections:
                    client_thread_instance = threading.Thread(
                        target=connection_handler, args=(conn, conn.getpeername()))
                    client_thread_instance.start()
    finally:
        server_socket.close()


if __name__ == "__main__":
    main()
