# 💬 Chat Server - TCP/IP Messaging Application

A **multi-client chat application** in Python using TCP sockets, **TLS encryption**, and multithreading. The server handles multiple clients simultaneously with password authentication and real-time message broadcasting.

---

## 📋 Table of Contents

- [Project Overview](#project-overview)
- [Project Structure](#project-structure)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation & Setup](#installation--setup)
  - [1. OpenSSL](#1-openssl)
  - [2. Localtonet (TCP tunnel)](#2-localtonet-tcp-tunnel)
  - [3. TLS Certificate Generation](#3-tls-certificate-generation)
  - [4. Start the Server](#4-start-the-server)
  - [5. Start a Client](#5-start-a-client)
- [Creating an Executable (.exe)](#creating-an-executable-exe)
- [Troubleshooting](#troubleshooting)
- [Detailed Operation](#detailed-operation)
- [Module Details](#module-details)
- [Limitations](#limitations)
- [Possible Improvements](#possible-improvements)
- [License](#license)

---

## 🖼️ Project Overview

This project implements a **centralized chat server** where multiple clients can connect, authenticate with a shared password, and exchange text messages in real time. All communications are **encrypted via TLS**. Each message sent by a client is broadcast to **all other connected clients** (not back to the sender).

---

## 📁 Project Structure

```
Chat_project/
├── chat_server.py                  # 🖧 Main server (entry point)
├── chat_client.py                  # 🖥️ Terminal client (user interface)
├── generate_cert.py                # 🔑 TLS certificate generator
├── README.md                       # 📄 This file
│
├── server_modules/                 # 📦 Server modules
│   ├── authentication.py           # 🔐 Password verification
│   ├── client_handler.py           # 🤝 Client connection handler (receive/broadcast)
│   └── client_management.py        # 🧹 Disconnected client cleanup
│
├── server_cert/                    # 🔒 Server certificates (KEEP SAFE)
│   ├── server.crt                  #   Public certificate
│   └── server.key                  #   ⚠️ Private key – DO NOT SHARE
│
└── client_cert/                    # 🔓 Client certificate
    └── server.crt                  #   Copy of the public certificate
```

---

## ✨ Features

| Feature | Description |
|---|---|
| 🔐 **Password Authentication** | A shared password is required to connect to the server |
| 👥 **Multi-client** | Up to **10 clients** connected simultaneously (configurable in `chat_server.py`) |
| 📡 **Real-time Broadcasting** | Messages are broadcast to all connected clients |
| 🧵 **Multithreading** | Each client is handled in a dedicated thread |
| 🔒 **Thread-safe Management** | Uses `Lock` to protect the shared client list |
| 🧹 **Automatic Cleanup** | Disconnected clients are automatically removed |
| 👤 **Usernames** | Each client chooses a username that prefixes their messages |
| 🔄 **Auto-reconnect** | The client attempts to reconnect if the server is unavailable |
| 🔐 **TLS/SSL Encryption** | Network communications between clients and server are encrypted with TLS |
| 🔑 **Automatic Certificate Generation** | `generate_cert.py` script creates and distributes certificates |
| ⌨️ **Enhanced CLI Interface** | Uses `prompt_toolkit` for a better input experience |

---

## 📦 Prerequisites

- **Python 3.10+**
- **pip** (Python package manager)
- **OpenSSL** (for generating TLS certificates)
- **Localtonet** (to expose the server over the Internet)

### Python Dependencies

```bash
pip install prompt_toolkit
```

> 💡 **On Linux/macOS**, use `pip3` instead.

---

# Installation & Setup

## 1. OpenSSL

OpenSSL is used to generate the TLS certificates required to encrypt communications between client and server.

### Installation (Windows)

Download **Win64 OpenSSL v3.6.3 Light** (This version was used to develop this project. A newer version of OpenSSL should also work.) ([official link](https://slproweb.com/products/Win32OpenSSL.html)):

```
Win64OpenSSL_Light-3_6_3.exe
```

During installation:

- Keep the default path:

```
C:\Program Files\OpenSSL-Win64
```

- For the OpenSSL DLL option, leave the default choice.

### Verify Installation

Open a **command prompt** (cmd) and type:

```bash
openssl version
```

You should see:

```
OpenSSL 3.6.3 ...
```

### If OpenSSL is not recognized

If you get:

```
'openssl' is not recognized as an internal or external command
```

add OpenSSL to the Windows PATH:

1. Search for **"Environment Variables"** in the Start menu (or press the Windows key)
2. Open **"Edit system environment variables"**
3. Go to **System variables** → **Path** → **Edit** → **New**
4. Add:

```
C:\Program Files\OpenSSL-Win64\bin
```

5. Close and reopen the terminal
6. Test again:

```bash
openssl version
```

---

## 2. Localtonet (TCP Tunnel)

The server uses **Localtonet** to create a TCP tunnel between the Internet and your local server. This allows remote clients to connect to your server even if you are behind a router or firewall.

Localtonet provides a **free quota** for testing this project.

### Install Localtonet

1. Download Localtonet from the **Microsoft Store** (Windows) or from [localtonet.com](https://localtonet.com)
2. Create an account at [localtonet.com](https://localtonet.com)
3. Open the Localtonet application
4. Go to the **Dashboard** of your account on the Localtonet website
5. Copy your **Auth Token**
6. Paste this token into the Localtonet application

### Create a TCP Tunnel

Follow this video tutorial to create a tunnel: [https://youtu.be/orgrqDL_pB4?si=_P5QO3oReonYmODf](https://youtu.be/orgrqDL_pB4?si=_P5QO3oReonYmODf)

⚠️ **When configuring the tunnel, make sure to select `TCP`.** Do not choose HTTP or HTTPS.

### Port Configuration

In the `chat_server.py` file, the default port is set:

```python
HOST_PORT = 32000
```

This port must match the **local port** configured in Localtonet:

| Localtonet | Code |
|---|---|
| `Local Port : 32000` | `HOST_PORT = 32000` |

If you change the port in the code, also change the port in Localtonet.

### Tunnel Address and Port

After creating and starting the tunnel, Localtonet displays an address similar to:

```
monchat.loclx.io:45678
```

This contains two pieces of information:

- **Server address**: `monchat.loclx.io`
- **Public port**: `45678`

> ⚠️ **Watch out for spaces!** When copying the address from Localtonet, make sure there are no spaces before or after the address or port. An invisible space can prevent the connection. If you copy from the Localtonet interface, paste it into a text editor first to check, then copy into the client.

In the client, you will need to enter:

```
Server address : monchat.loclx.io
Port : 45678
```

With the current Localtonet configuration, the tunnel address (`xxx.loclx.io`) usually stays the same between sessions. However, **the public port changes each time the tunnel is restarted** (by default).

---

## 3. TLS Certificate Generation

The project uses **TLS** to encrypt communications. The address entered in the client must be exactly the same as the one used when generating the certificate.

Run:

```bash
python generate_cert.py
```

The script will ask for the server address.

> ⚠️ **Important:** Enter the address **without leading or trailing spaces**. A space can invalidate the certificate and cause a TLS error during connection.

Enter the Localtonet tunnel address. Example:

```
2pmp9eagli.localto.net
```

The script will create:

```
server_cert/
├── server.crt        # Server public certificate
└── server.key        # 🔑 Private key – DO NOT SHARE
```

and copy the public certificate to:

```
client_cert/
└── server.crt
```

### Important Notes on TLS Files

| File | Role | Share? |
|---|---|---|
| `server.key` | Server private key | ❌ **Never** – Must stay only on the server |
| `server.crt` | Public certificate | ✅ Yes – Allows clients to verify the server's identity |

> ⚠️ **Never publish `server.key` on GitHub** or any other sharing service. Add this file to your `.gitignore`.

---

## 4. Start the Server

1. Make sure the **Localtonet tunnel** is active (the application must be open and the TCP tunnel started).
2. Make sure the **TLS certificates** have been generated (see step 3).
3. Start the server:

```bash
python chat_server.py
```

The server will ask you to set the **server password**:

```
Set the server password: ********
Waiting for connection on: 0.0.0.0 32000
```

- The server listens on **all interfaces** (`0.0.0.0`) on **port 32000**
- It uses TLS/SSL to encrypt incoming connections
- It waits for client connections
- The maximum number of clients is set by `MAX_CLIENT = 10` in `chat_server.py`. You can modify this value to allow more or fewer simultaneous connections.

> 🔑 The configured password must be shared with your clients so they can connect.

---

## 5. Start a Client

On each client machine, make sure the `client_cert/server.crt` file is present (this is done automatically after running `generate_cert.py`).

```bash
python chat_client.py
```

The client will ask for:

1. **Your username** (displayed before your messages)
2. **Server address** – the Localtonet tunnel address (e.g., `monchat.loclx.io`)
3. **Port** – the **public port** provided by Localtonet (e.g., `45678`)
4. **Password** – the password configured on the server

**Example session:**

```
Type a username: Alice
What is the server address: monchat.loclx.io
What is the port: 45678

 Tip: Type "exit" to leave the chat

Successfully connected to the server: monchat.loclx.io
Enter password: ********
Correct

You: Hello everyone!
Bob: Hey Alice, how are you?
You: Good, and you?
Bob: Very well, thanks!
```

> 🔐 The client automatically verifies the **TLS certificate** before allowing the connection. If the tunnel address changes, you must regenerate the certificates.

---

# Creating an Executable (.exe)

If you want to share the client **without requiring users to install Python**, you can create a `.exe` file with **PyInstaller**.

## Install PyInstaller

```bash
pip install pyinstaller
```

Verify the installation:

```bash
pyinstaller --version
```

## Create the client.exe File

Navigate to the folder containing `chat_client.py` and `client_cert/`, then run:

```bash
pyinstaller --onefile --add-data "client_cert;client_cert" chat_client.py
```

Explanation of options:

| Option | Description |
|---|---|
| `--onefile` | Creates a single `.exe` file |
| `--add-data "client_cert;client_cert"` | Includes the TLS certificate in the executable |

The result will be created in:

```
dist/
└── chat_client.exe
```

## Share the Program

1. Get `dist/chat_client.exe`
2. Place it in a `.zip` archive
3. Send this archive via Google Drive, OneDrive, etc.
4. Users do **not need to install Python** – they simply run `chat_client.exe`

> ⚠️ **Windows Defender Notice:** A `.exe` file created with PyInstaller may sometimes be flagged by Windows Defender or some antivirus software because the executable is new and has no digital signature. This does not mean the file is dangerous. Users should allow the application if they trust the source.

---

# Troubleshooting

## ⚠️ Space Issue When Copy-Pasting

If the client displays a connection error even though the address looks correct:

1. Check for **leading or trailing spaces** around the address or port
2. Paste the address into a text editor to visually inspect it
3. If you see a space, remove it and try again

> Tip: Type the address manually rather than copy-pasting from the Localtonet interface.

## TLS Certificate Error

If you get a TLS error:

- Does the address entered in the client match the one used when generating the certificate?
- Is the `client_cert/server.crt` file present?
- Is the Localtonet tunnel still using the same address?

**Solution:** If the tunnel address changes, regenerate the certificates:

```bash
python generate_cert.py
```

## Error "server.crt and server.key do not exist"

You haven't generated the certificates yet. Run:

```bash
python generate_cert.py
```

## Error "client_cert folder does not exist"

The public certificate wasn't copied to the client folder. Re-run `generate_cert.py` to create it.

## Connection Error

Check the following:

- Is Localtonet running and the TCP tunnel active?
- Does the port in Localtonet match the `HOST_PORT` in the server (`32000` by default)?
- Is the server started before clients try to connect?
- Is the Localtonet public port correct (it changes on every restart)?

## "Wrong password" Rejected

- Make sure the entered password exactly matches the one configured on the server
- Passwords are case-sensitive

---

# ⚡ Detailed Operation

## 🖧 Server Side

1. The server loads the TLS certificate (`server.crt`) and private key (`server.key`)
2. It creates a TCP socket, secures it with TLS, then listens on `0.0.0.0:32000`
3. For each new accepted connection, the server performs a **TLS handshake**
4. If the handshake succeeds, a thread is launched to run `handle_client()`
5. `handle_client()` first calls `verify()` to authenticate the client
6. If authentication succeeds, the client is added to the shared `client_list`
7. The thread then loops, listening for messages from the client:
   - If a message is received, it is broadcast to **all other clients**
   - If the client sends `"exit"`, they are cleanly disconnected
   - If the connection is lost, the socket is closed and removed from the list

## 🖥️ Client Side

1. The client loads the server's TLS certificate (`client_cert/server.crt`) as a trusted authority
2. It creates a TCP socket and attempts to connect to the server
3. Once connected, it performs a **TLS handshake**, verifying the server's certificate
4. If the certificate is valid, it sends the password for authentication
5. If the password is correct, a **receiver thread** is launched to listen for incoming messages
6. The **main thread** handles user input via `prompt_toolkit` and sends messages
7. If the user types `"exit"`, the connection is cleanly closed

## 🧵 Thread Architecture

```
┌─────────────────────────────────────────────────┐
│                   SERVER                        │
│                                                  │
│  Main thread:                                    │
│    Accepts connections                           │
│    Performs TLS handshake                        │
│    Launches one thread per client                │
│                                                 │
│  Thread Client A ──┐                            │
│  Thread Client B ──┤  Each thread:              │
│  Thread Client C ──┤  • Authenticates the client│
│  ...               │  • Receives messages       │
│                    │  • Broadcasts to others    │
│                    └─────────────────────────   │
└─────────────────────────────────────────────────┘
                        ▲
                        │ TCP + TLS
                        ▼
┌─────────────────────────────────────────────────┐
│                   CLIENT                         │
│                                                  │
│  Main thread:                                    │
│    User input & sending                          │
│                                                  │
│  Receiver thread (daemon):                       │
│    Receives & displays messages                  │
└─────────────────────────────────────────────────┘
```

---

# 🔧 Module Details

## `chat_server.py` — Server Entry Point

- Loads the TLS certificate and private key
- Configures the server password
- Initializes the secure listening socket (`0.0.0.0:32000`)
- Accepts connections with TLS handshake
- Limits clients to `MAX_CLIENT` (10)
- Launches a `handle_client` thread for each new connection

## `generate_cert.py` — TLS Certificate Generator

- Asks for the server address (Localtonet address)
- Generates a self-signed certificate via OpenSSL
- Creates the `server_cert/` and `client_cert/` directories
- Copies the public certificate to `client_cert/server.crt`

## `server_modules/authentication.py` — Authentication Module

Function **`verify(client_socket, password, client_list, lock, max_data_size)`**:

1. Receives the password from the client
2. Compares it with the configured server password
3. Sends `"Correct"` or `"Wrong"` based on the result
4. If correct, adds the socket to `client_list` (thread-safe via `lock`)
5. Returns `True` if authenticated, `False` otherwise

## `server_modules/client_handler.py` — Client Handler

Function **`handle_client(client_socket, password, client_list, lock, max_data_size)`**:

1. Calls `verify()` — if it fails, the thread stops
2. Message reception loop:
   - If a message is received, broadcasts it to all other clients
   - If the message is `"exit"`, disconnects the client
   - If the message exceeds 1000 characters, returns a `"Message too large"` error
3. Cleans up dead clients after each operation

## `server_modules/client_management.py` — Cleanup

Function **`cleanup(dead_clients, client_list, lock)`**:

- Removes all dead sockets from `client_list`
- Closes each removed socket
- Thread-safe operation using `lock`

---

# Limitations

| Limitation | Detail |
|---|---|
| 📏 **Message size** | Limited to **1024 bytes** (`MAX_DATA_SIZE`) |
| 🔢 **Long messages** | Messages over 1000 characters are rejected |
| 👥 **Max clients** | Limited to 10 (`MAX_CLIENT`) |
| 🔐 **Single password** | All clients share the same password (no individual user accounts) |
| 📁 **No history** | Messages are not persisted (in-memory only) |

---

# 🚀 Possible Improvements

- [x] **TLS/SSL Encryption** — Secure communications ✅
- [ ] **Chat rooms** — Separate rooms (public, password-protected private)
- [ ] **Graphical User Interface (GUI)** — Desktop app with Tkinter or PyQt
- [ ] **Web interface** — Web version with WebSockets
- [ ] **Private messages** — Direct communication between two clients
- [ ] **End-to-end encryption** — Encrypt messages client-side before sending so even the server cannot read them

> 💡 **All contributions are welcome!** Whether it's a bug fix, a suggestion for improvement, or a new feature, feel free to open an *issue* or a *pull request*. Every bit of help, no matter how small, is valuable for the evolution of this project.

---

# 📄 License

This project is provided for educational and learning purposes. You are free to use, modify, and distribute it.

### Publishing on GitHub

Before publishing the project on GitHub, follow these steps to avoid exposing sensitive files:

1. 🗑️ **Delete** `server_cert/server.key` — private key that must never be shared
2. 🗑️ **Delete** `server_cert/server.crt`
3. 🗑️ **Delete** the `client_cert/` folder
4. ▶️ **Run** `generate_cert.py` after each clone to regenerate the certificates

> ⚠️ **Never publish your private key (`server.key`)** on GitHub or any other sharing service.
---

*Project created as part of learning TCP/IP networking, TLS encryption, and multithreading in Python.*

