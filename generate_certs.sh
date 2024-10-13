#!/bin/bash

# Your existing CA certificate and private key
CA_CERT="/etc/ssl/demoCA/cacert.pem"
CA_KEY="/etc/ssl/demoCA/private/cakey.pem"

# Directories to save the new certificates and private keys
CERTS_DIR="/etc/ssl/demoCA/newcerts"
PRIVATE_DIR="/etc/ssl/demoCA/private"

# Default attributes for Distinguished Name
COUNTRY="US"
STATE="California"
LOCALITY="Lompoc"
ORGANIZATION="CST311"
ORG_UNIT="Networking"

# Ask for the Common Name for the web server
read -p "Enter the Common Name for the web server: " WEB_SERVER_CN

# Generate a private key and CSR for the web server
openssl genpkey -algorithm RSA -out $PRIVATE_DIR/webserver-key.pem
openssl req -new -key $PRIVATE_DIR/webserver-key.pem -out $CERTS_DIR/webserver-csr.pem -subj "/C=$COUNTRY/ST=$STATE/L=$LOCALITY/O=$ORGANIZATION/OU=$ORG_UNIT/CN=$WEB_SERVER_CN"

# Sign the web server's CSR with the CA
openssl x509 -req -in $CERTS_DIR/webserver-csr.pem -CA $CA_CERT -CAkey $CA_KEY -CAcreateserial -out $CERTS_DIR/webserver-cert.pem -days 365

# Ask for the Common Name for the chat server
read -p "Enter the Common Name for the chat server: " CHAT_SERVER_CN

# Generate a private key and CSR for the chat server
openssl genpkey -algorithm RSA -out $PRIVATE_DIR/chatserver-key.pem
openssl req -new -key $PRIVATE_DIR/chatserver-key.pem -out $CERTS_DIR/chatserver-csr.pem -subj "/C=$COUNTRY/ST=$STATE/L=$LOCALITY/O=$ORGANIZATION/OU=$ORG_UNIT/CN=$CHAT_SERVER_CN"

# Sign the chat server's CSR with the CA
openssl x509 -req -in $CERTS_DIR/chatserver-csr.pem -CA $CA_CERT -CAkey $CA_KEY -CAcreateserial -out $CERTS_DIR/chatserver-cert.pem -days 365

echo "Certificates generated successfully."
