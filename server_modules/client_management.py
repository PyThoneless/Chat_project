"""
Client management module for the chat server.

Handles cleanup of disconnected clients from the shared client list.
"""


def cleanup(dead_clients, client_list, lock):
    """
    Remove disconnected clients from the shared list and close their sockets.

    Args:
        dead_clients: List of client sockets that have disconnected.
        client_list: Shared list of connected client sockets.
        lock: Threading lock for thread-safe access to client_list.
    """
    with lock:
        for client in dead_clients:
            try:
                client_list.remove(client)
            except ValueError:
                pass
            else:
                client.close()

