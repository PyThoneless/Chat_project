"""
Client handler module for the chat server.

Handles an individual client connection: authentication, message reception,
and message broadcasting to all other connected clients.
"""

from server_modules.authentication import verify
from server_modules.client_management import cleanup


def handle_client(client_socket, password, client_list, lock, max_data_size):
    """
    Manage a single client connection.

    Authenticates the client, then listens for incoming messages and
    broadcasts them to all other connected clients.

    Args:
        client_socket: The SSL-wrapped client socket.
        password: The server's configured password.
        client_list: Shared list of connected client sockets.
        lock: Threading lock for thread-safe access to client_list.
        max_data_size: Maximum data size to receive.
    """
    if not verify(client_socket, password, client_list, lock, max_data_size):
        return

    while True:
        dead_clients = []
        try:
            received_data = client_socket.recv(max_data_size)
        except OSError:
            dead_clients.append(client_socket)
            break
        else:
            if received_data and not received_data.decode().lower() == "exit":
                with lock:
                    client_copy = client_list.copy()
                for client in client_copy:
                    if client != client_socket:
                        try:
                            client.sendall(received_data)
                        except OSError:
                            dead_clients.append(client)
            elif len(received_data.decode()) > 1000:
                try:
                    client_socket.sendall("Message too large".encode())
                except OSError:
                    dead_clients.append(client_socket)
            else:
                dead_clients.append(client_socket)
                break

        cleanup(dead_clients, client_list, lock)

    cleanup(dead_clients, client_list, lock)

