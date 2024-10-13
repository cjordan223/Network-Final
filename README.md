# TLS Chat and Web Server with Mininet (Legacy)

## Overview
This project simulates a secure network environment using TLS (Transport Layer Security) for both a chat server and a web server. It leverages Mininet to create a virtual network and uses certificates to secure communication between clients and servers. The key components include server and client scripts that perform SSL handshakes to ensure secure, authenticated sessions.

## Project Structure
- `PA4_tls_chat_client_Team5.py`: Chat client that connects to the chat server using TLS.
- `PA4_tls_chat_server_Team5.py`: Chat server with TLS-based secure communication.
- `PA4_tls_web_server_Team5.py`: Web server using TLS for secure communication.
- `generate_certs.sh`: Script to generate certificates for the web and chat servers.
- `legacy_network.py`: Script to simulate the network environment in Mininet.
- `SETUP.md`: Instructions for setting up the certificates and network environment.

## Setup Instructions

### Step 1: Prepare CA Certificates
1. Set up your CA  
2. Use the `generate_certs.sh` script to generate certificates for the web and chat servers.

### Step 2: Generate Server Certificates
1. Navigate to the directory:  
   ```bash
   cd ~/CST331/cst311-fall2023-assignments/PA4/src
