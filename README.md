# IoT Telemetry Gateway Lab

A simulated IoT network lab built in Python. It runs entirely on localhost (no physical devices) and is analyzed with Wireshark. The goal is to practice TCP/IP fundamentals, protocol design and IoT messaging (MQTT).

## Status

| Phase | Description | Status |
| :--- | :--- | :--- |
| 1 | TCP server and client with a length-prefixed message protocol, multi-client support | Done |
| 2 | UDP telemetry with sequence numbers, packet loss and latency measurement | Planned |
| 3 | MQTT publishers and a gateway subscriber (Mosquitto broker), QoS 0 vs 1 | Planned |
| 4 | Wireshark analysis of TCP and MQTT traffic | Planned |

## Phase 1: TCP with message framing

TCP is a byte stream and has no message boundaries, so one `send()` on one side can arrive as several `recv()` chunks on the other. Each message is therefore framed as a 4-byte big-endian length followed by a JSON body (UTF-8).

`recv_exact()` keeps reading until exactly the requested number of bytes has arrived. A maximum frame size is enforced so a bad length field cannot make the server wait for a huge message.

The server handles each client in its own thread and replies to every message with an acknowledgement containing the sequence number. The client measures the round-trip time of each message.

## Files

- `src/protocol.py`: framing functions (`send_msg`, `recv_exact`, `recv_msg`)
- `src/tcp_server.py`: multi-client threaded TCP server on 127.0.0.1:9000
- `src/tcp_client.py`: sends N messages and prints the round-trip time of each
- `captures/`: Wireshark captures
- `docs/`: screenshots

## Run

Requires Python 3.9 or newer. No external packages.

Start the server in one terminal:

    python src/tcp_server.py

Run a client in another terminal (optional argument: number of messages):

    python src/tcp_client.py 5

Run several clients at once to test concurrent connections.

## Limitations

- Everything runs on localhost, so there is no real network latency, loss or reordering.
- One thread per client is fine for a lab but would not scale to thousands of connections.
- No authentication or encryption (no TLS).

## Planned

- UDP sender and receiver with sequence numbers to measure loss, reordering and latency, compared against TCP.
- MQTT telemetry through a Mosquitto broker, with a QoS 0 vs QoS 1 comparison in Wireshark.
- Reuse of the fault-telemetry JSON format from my [FOC + TinyML project](https://github.com/Karal-maks/embedded-rtos-tinyml) as the sensor payload.