"""
TLS Certificate Generator for the Chat Project.

Generates a self-signed TLS certificate for the server and copies
the public certificate to the client directory.
"""

import shutil
import subprocess
from pathlib import Path


# Project base directory
BASE_DIR = Path(__file__).parent

# Certificate directories
SERVER_CERT_DIR = BASE_DIR / "server_cert"
CLIENT_CERT_DIR = BASE_DIR / "client_cert"

# TLS files
SERVER_CERT = SERVER_CERT_DIR / "server.crt"
SERVER_KEY = SERVER_CERT_DIR / "server.key"


def generate_certificate(name_ip):
    """
    Generate a self-signed TLS certificate using OpenSSL.

    Args:
        name_ip: The server hostname or IP address (used as CN).

    Returns:
        True if generation succeeded, False otherwise.
    """
    # Create directories
    SERVER_CERT_DIR.mkdir(exist_ok=True)
    CLIENT_CERT_DIR.mkdir(exist_ok=True)

    # Check if certificates already exist
    if SERVER_CERT.exists() and SERVER_KEY.exists():
        print("Certificates already exist.")
        return

    print("Generating TLS certificate...")

    command = [
        "openssl",
        "req",
        "-x509",
        "-newkey",
        "rsa:2048",
        "-keyout",
        str(SERVER_KEY),
        "-out",
        str(SERVER_CERT),
        "-days",
        "365",
        "-nodes",
        "-subj",
        "/CN=" + name_ip
    ]

    try:
        subprocess.run(command, check=True)
    except FileNotFoundError:
        print("Error: OpenSSL is not installed.")
        print("Install OpenSSL and run generate_cert.py again.")
        return False
    except subprocess.CalledProcessError:
        print("Error during certificate generation.")
        return False

    print("Server certificate created.")
    return True


def copy_certificate_to_client():
    """
    Copy the server's public certificate to the client directory.
    """
    destination = CLIENT_CERT_DIR / "server.crt"

    shutil.copy(SERVER_CERT, destination)

    print("Certificate copied to the client folder.")


if __name__ == "__main__":
    name_ip = input("What is the server address: ").strip()

    if not name_ip:
        print("Error: no server address provided.")
        input("ENTER to close")
        exit()

    generate_certificate(name_ip)

    if SERVER_CERT.exists():
        copy_certificate_to_client()

    print("\nDone.")
    input("ENTER to close")

