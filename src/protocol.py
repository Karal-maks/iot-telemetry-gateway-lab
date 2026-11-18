import json
import struct

MAX_FRAME = 1_000_000

def send_msg(sock, obj):
    """Send one JSON message: 4-byte big-endian length, then the JSON body."""
    data = json.dumps(obj).encode("utf-8")
    sock.sendall(struct.pack("!I", len(data)) + data)

def recv_exact(sock, n):
    """TCP is a byte stream: keep reading until exactly n bytes arrive."""
    buf = b""
    while len(buf) < n:
        chunk = sock.recv(n - len(buf))
        if not chunk:
            return None          # peer closed the connection
        buf += chunk
    return buf

def recv_msg(sock):
    header = recv_exact(sock, 4)
    if header is None:
        return None
    (length,) = struct.unpack("!I", header)
    if length > MAX_FRAME:
        raise ValueError(f"frame too large: {length}")
    body = recv_exact(sock, length)
    if body is None:
        return None
    return json.loads(body.decode("utf-8"))