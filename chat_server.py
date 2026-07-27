"""
Chat Server - Main entry point.

A multi-client TCP chat server with TLS/SSL encryption.
Listens for incoming connections, authenticates clients,
and broadcasts messages to all connected clients.
"""

import socket
import threading
from server_modules.client_handler import handle_client
import ssl


# --- Configuration ---
password = input("Set the server password: ")

client_list = []

lock = threading.Lock()

HOST_IP = "0.0.0.0"
HOST_PORT = 32000
MAX_DATA_SIZE = 1024
MAX_CLIENT = 10

# --- TLS/SSL Context Setup ---
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)

try:
    context.load_cert_chain(
        "server_cert/server.crt",
        "server_cert/server.key"
    )
except FileNotFoundError:
    print("Error: server.crt and server.key do not exist.")
    print("Please run generate_cert.py first.")
    print()
    input("Press ENTER to close the server")
    exit()
except ssl.SSLError:
    print("Error with the TLS certificate.")
    print("Delete the server_cert and client_cert folders, then run generate_cert.py")
    input("Press ENTER to close the server")
    exit()

# --- Server Socket ---
s = socket.socket()
s.bind((HOST_IP, HOST_PORT))
s.listen()

# --- Main Loop ---
while True:
    if not len(client_list) > MAX_CLIENT:
        print("Waiting for connection on:", HOST_IP, HOST_PORT)
        connection_socket, client_address = s.accept()
        try:
            secure_socket = context.wrap_socket(
                connection_socket,
                server_side=True
            )
            print("SSL connection established")
            thread = threading.Thread(
                target=handle_client,
                args=(secure_socket, password, client_list, lock, MAX_DATA_SIZE),
                daemon=True
            )
            thread.start()
        except ssl.SSLError:
            print("TLS handshake error with a client")
            connection_socket.close()

