"""
Chat Client - Terminal-based chat application.

Connects to a TLS/SSL-secured chat server, authenticates with a password,
and allows the user to send/receive messages in real time.
"""

import socket
import threading
import time
from prompt_toolkit import PromptSession
from prompt_toolkit.patch_stdout import patch_stdout
import ssl


MAX_DATA_SIZE = 1024


def receive_and_display(sock, print_lock):
    """
    Background thread: continuously receive messages from the server
    and display them to the user.

    Args:
        sock: The connected socket.
        print_lock: Threading lock to synchronize console output.
    """
    print("Correct")
    print()
    while True:
        try:
            received_text = sock.recv(MAX_DATA_SIZE)
        except Exception:
            with patch_stdout():
                print()
                print("Chat closed ...")
            break
        if received_text:
            with print_lock:
                with patch_stdout():
                    print(received_text.decode())


# --- User Input ---
username = input("Type a username: ")

HOST_IP = input("What is the server address: ")
HOST_PORT = input("What is the port: ")
session = PromptSession()

print(""" Tip: Type "exit" to leave the chat""")
print()

# --- TLS/SSL Context ---
context = ssl.create_default_context()
try:
    context.load_verify_locations("client_cert/server.crt")
except FileNotFoundError:
    print("Error: the client_cert folder does not exist.")
    print("Run generate_cert.py to obtain it.")
    input("Press ENTER to exit")
    exit()
except ssl.SSLError:
    print("Error with the SSL certificate.")
    print("Delete the client_cert folder and re-run generate_cert.py")
    input("Press ENTER to exit")
    exit()

# --- Connection Loop ---
while True:
    sock = socket.socket()
    try:
        sock.connect((HOST_IP, int(HOST_PORT)))
    except ConnectionRefusedError:
        print("ERROR: Connection failed. Reconnecting...")
        sock.close()
        time.sleep(3)
    else:
        try:
            sock = context.wrap_socket(
                sock,
                server_hostname=HOST_IP
            )
        except ssl.SSLError:
            print("TLS error: certificate rejected.")
            print("Check the server address and your certificate.")
            sock.close()
            input("Press ENTER to close the client.")
            exit()
        else:
            print("Successfully connected to the server:", HOST_IP)
        break

# --- Authentication ---
password = input("Enter password: ")
try:
    sock.sendall(password.encode())
except Exception:
    sock.close()
    print("An error occurred")
    exit()
else:
    try:
        result = sock.recv(MAX_DATA_SIZE)
    except Exception:
        print("An error occurred")
    else:
        result = result.decode()
        if result == "Wrong password":
            print("Wrong password")
            print("Press ENTER to exit")
            input()
            exit()

# --- Start Receiver Thread ---
print_lock = threading.Lock()

thread = threading.Thread(
    target=receive_and_display,
    args=(sock, print_lock),
    daemon=True
)
thread.start()

# --- Main Input Loop ---
while True:
    time.sleep(0.5)
    text_to_send = session.prompt("You: ")
    if text_to_send == "exit":
        with patch_stdout():
            print()
            print("Discussion ended")
        sock.close()
        break
    text_to_send = username + " :" + text_to_send
    try:
        sock.sendall(text_to_send.encode())
    except Exception:
        with patch_stdout():
            print()
            print("Conversation closed due to a server error.")
        sock.close()
        break

