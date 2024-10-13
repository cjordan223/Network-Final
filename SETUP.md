## Setup
1. Make sure you setup up your CA from part 1 of [lab 6](https://docs.google.com/document/d/189BcpTGp5zxDigfOwO7a5AigFL4kNMbR4bujjAcyM9k/edit) (Up to step 18)
## Generate web server and chat server certs
1. `cd` into `mininet@mininet-vm:~/CST331/cst311-fall2023-assignments/PA4/src$`
2. Run `sudo chmod +x generate_certs.sh`
3. Run `sudo ./generate_certs.sh` 
4. Input `www.webpa4.test` for common name for web server
5. Input `chat.webpa4.test` for common name for chat server
6. It should look like this you will need your passphrase from your `cakey.pem` you made from lab 6. 
7. If you forgot your passphrase redo step 1 from setup.
```bash
mininet@mininet-vm:~/CST331/cst311-fall2023-assignments/PA4/src$ sudo ./generate_certs.sh
Enter the Common Name for the web server: www.webpa4.test
...........+++++
...........................+++++
Signature ok
subject=C = US, ST = California, L = Lompoc, O = CST311, OU = Networking, CN = www.webpa4.test
Getting CA Private Key
Enter pass phrase for /etc/ssl/demoCA/private/cakey.pem:
Enter the Common Name for the chat server: chat.webpa4.test
...........+++++
....+++++
Signature ok
subject=C = US, ST = California, L = Lompoc, O = CST311, OU = Networking, CN = chat.webpa4.test
Getting CA Private Key
Enter pass phrase for /etc/ssl/demoCA/private/cakey.pem:
Certificates generated successfully.
```
## Add the server host names 
1. Run `cd` to return to `mininet@mininet-vm:~$` 
2. Run `nano /etc/hosts` and 
3. Add `10.0.1.2        www.webpa4.test`
4. Add `10.0.2.2        chat.webpa4.test`
5. Hosts file should look like
```bash
127.0.0.1       localhost
127.0.1.1       mininet-vm
127.0.0.1       ca.csumb.test
10.0.0.2        www.cst311.test
10.0.1.2        www.webpa4.test
10.0.2.2        chat.webpa4.test
# The following lines are desirable for IPv6 capable hosts
::1     localhost ip6-localhost ip6-loopback
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
```
## Run the legacy_router.py
1. `cd` into `mininet@mininet-vm:~/CST331/cst311-fall2023-assignments/PA4/src$`
2. Run `sudo -E  python legacy_network.py`
3. This will create the network, start the `PA4_tls_web_server.py` on `h2` and `PA4_tls_chat_server_Team5.py` on `h4` in xterm.
4. It will also start the `PA4_tls_chat_client_Team5.py` on `h1` and `h3` in xterm.
3. It will also start wireshark on `s1`.
## Notes
To wget a running `PA4_tls_web_server_Team5.py` on a `h1` or `h3` xterm need to specify the CA cert like this `wget --ca-certificate=/etc/ssl/demoCA/cacert.pem https://www.webpa4.test:12000`

To capture wireshark run `sudo -E  python legacy_network.py` wireshark will open on `s1` capture `s1-eth1`. Then on the xterm of `h1` or `h3` run `python3 PA4_tls_chat_client_Team5.py`. You should see the trace in wireshark with the `Server Hello`.

`PA4_tls_web_server_Team5.py` runs on h2's ip and port and uses these certs you generated
```python
    server_port = 12000
    server_name = '10.0.1.2'
    cert_path = '/etc/ssl/demoCA/newcerts/webserver-cert.pem'
    key_path = '/etc/ssl/demoCA/private/webserver-key.pem'
```
`PA4_tls_chat_server_Team5.py` runs on h4's ip and port and uses these certs you generated
```python
    server_port = 12000
    server_name = '10.0.2.2'
    cert_path = '/etc/ssl/demoCA/newcerts/chatserver-cert.pem'
    key_path = '/etc/ssl/demoCA/private/chatserver-key.pem'
```
`PA4_tls_chat_client_Team5.py` connects on server name created by the CN you made for `chatserver-cert.pem` on the port server is ran on. It uses the CA rootcert to do a ssl handshake.
```python
    server_name = 'chat.webpa4.test' 
    server_port = 12000 
    certfile = '/etc/ssl/demoCA/cacert.pem'
```
