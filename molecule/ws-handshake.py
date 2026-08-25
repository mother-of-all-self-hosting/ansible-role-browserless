# SPDX-FileCopyrightText: 2026 Slavi Pantaleev
#
# SPDX-License-Identifier: AGPL-3.0-or-later

"""Performs a WebSocket handshake and prints the HTTP status code it got back.

Usage: ws-handshake.py <host> <port> <path>

Browserless hands out Chrome DevTools Protocol sessions over WebSocket
(`ws://.../chromium`), which is the surface the services that a playbook wires
up to it actually use. Nothing in ansible-core speaks WebSocket, and the
Molecule test images carry no curl, so this does the (very small) opening
handshake by hand: what matters for the assertions is only whether the server
answers `101 Switching Protocols` or turns the request away with `401`.
"""

import base64
import os
import socket
import sys

host, port, path = sys.argv[1], int(sys.argv[2]), sys.argv[3]

request = (
    f"GET {path} HTTP/1.1\r\n"
    f"Host: {host}:{port}\r\n"
    "Upgrade: websocket\r\n"
    "Connection: Upgrade\r\n"
    f"Sec-WebSocket-Key: {base64.b64encode(os.urandom(16)).decode()}\r\n"
    "Sec-WebSocket-Version: 13\r\n"
    "\r\n"
)

connection = socket.create_connection((host, port), timeout=30)

try:
    connection.sendall(request.encode())
    status_line = connection.recv(4096).decode("latin-1").split("\r\n", 1)[0]
finally:
    connection.close()

# e.g. "HTTP/1.1 101 Switching Protocols" -> "101"
print(status_line.split(" ")[1])
