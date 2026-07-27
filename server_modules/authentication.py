"""
Authentication module for the chat server.

Provides password verification for incoming client connections.
"""


def verify(client_socket, password, client_list, lock, max_data_size):
    """
    Verify the client's password against the server's configured password.

    Args:
        client_socket: The SSL-wrapped client socket.
        password: The server's configured password.
        client_list: Shared list of connected client sockets.
        lock: Threading lock for thread-safe access to client_list.
        max_data_size: Maximum data size to receive.

    Returns:
        True if authentication succeeded, False otherwise.
    """
    try:
        received_data = client_socket.recv(max_data_size)
    except OSError:
        client_socket.close()
        return False
    else:
        try:
            received_data = received_data.decode()
        except Exception:
            client_socket.close()
            return False

        if received_data == password:
            try:
                client_socket.sendall("Correct".encode())
            except Exception:
                client_socket.close()
                return False
            else:
                with lock:
                    client_list.append(client_socket)
                return True
        else:
            try:
                client_socket.sendall("Wrong".encode())
            except Exception:
                pass
            client_socket.close()
            return False

